#!/usr/bin/python

# requirements
from termcolor import colored
from simconst import *
from EVSE import *
from EV import *
import random
import getopt
import time
import sys

# simulation
class Simulation:

    # initializer
    def __init__(self, days, car_freq):
        """Simulation initializer"""

        # debug print
        print colored("Simulation::__init__> ", "blue", attrs=["bold"]) + "initializing simulation"

        # read the parameters
        # - number of days to be simulated
        # - number of cars per day to be simulated
        self.days = int(days)
        self.car_freq = int(car_freq)
    
        # set other parameters
        self.charging = False
        self.seconds = self.days * 24 * 60 * 60 
        self.current_second = 0
        self.current_car = -1
        self.total_cars = self.car_freq * self.days
        self.arrival_times = []
        for i in xrange(self.total_cars):
            self.arrival_times.append(self.seconds / self.total_cars * i)

        # initialize the column
        # NOTE: only one column must be simulated
        print colored("Simulation::__init__> ", "blue", attrs=["bold"]) + "creating an EVSE"
        self.column = EVSE() 

        # initialize cars
        print colored("Simulation::__init__> ", "blue", attrs=["bold"]) + "creating %s EVs" % str(self.car_freq * self.days)
        self.cars = []
        for i in xrange(self.total_cars):
            # create an EV
            soc = random.randint(0, 6)        
            self.cars.append(EV(soc, EV_CAPACITY))


    # run
    def run(self):
        """Method to run the simulation"""
        
        # debug print
        print colored("Simulation::run> ", "blue", attrs=["bold"]) + "running the simulation"

        # cycles over the time seconds
        for sec in xrange(self.seconds):
            
            # debug print 
            print colored("Simulation::run> ", "blue", attrs=["bold"]) + "simulating second %s of %s" % (sec, self.seconds)
            time.sleep(0.005)
            
            # simulate the second!
            self.current_second = sec

            # recharge the storage using the sunlight
            self.column.recharge_storage_with_sun(sec)

            # recharge the storage using the network
            self.column.recharge_storage_with_net()

            # check if a new vehicles arrives
            if sec in self.arrival_times:
            
                # a new vehicle starts his recharge,
                # so extract the vehicle from the list
                self.current_car += 1
                
                # set the charging status to True
                self.charging = True

                # recharge the car                
                charge = self.column.recharge_vehicle()
                self.cars[self.current_car].recharge(charge)

                # if after this recharge the battery is full
                # then we set the charging status to False
                if self.cars[self.current_car].full():
                    self.charging = False

            # or if a vehicle is charging
            elif self.charging:

                # recharge the car
                charge = self.column.recharge_vehicle()
                self.cars[self.current_car].recharge(charge)

                # if after this recharge the battery is full
                # then we set the charging status to False
                if self.cars[self.current_car].full():
                    self.charging = False
                

# main
if __name__ == "__main__":

    # read command line arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:c:", ["days=", "carfreq="])
    except getopt.GetoptError as err:
        print "Try this:"
        print "$ python simulation.py --days=NUM_OF_DAYS --carfreq=CAR_FREQUENCY"
        sys.exit(2)

    # Init
    carfreq = 1
    days = 1

    # parse command line parameters
    for opt, arg in opts:
        if opt in ("-c", "--carfreq"):
            carfreq = int(arg)
        elif opt in ("-d", "--days"):
            days = int(arg)
        else:
            assert False, "unhandled option"

    # start the simulation
    s = Simulation(days, carfreq)
    try:
        s.run()
    except KeyboardInterrupt:
        print "CTRL-C pressed, bye!"
