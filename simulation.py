#!/usr/bin/python

# requirements
from output_helper import *
from Statistics import *
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
    def __init__(self, days, car_freq, policy, sleep, debug):
        """Simulation initializer"""

        # create an output helper
        self.oh = OutputHelper("blue", "Simulation")

        # debug print
        self.oh.out("init", "initializing simulation")

        # read the parameters
        # - number of days to be simulated
        # - number of cars per day to be simulated
        # - policy is the policy used to recharge the storage
        # - debug is used to turn on or off the verbosity
        # - sleep is used to slow down the simulation
        self.days = int(days)
        self.car_freq = int(car_freq)
        self.policy = policy
        self.debug = debug
        self.sleep = sleep

        # set other parameters
        self.charging = False
        self.seconds = self.days * 24 * 60 * 60 
        self.current_second = 0
        self.current_car = -1
        self.total_cars = self.car_freq * self.days
        self.arrival_times = []
        for i in xrange(self.total_cars):
            self.arrival_times.append(self.seconds / self.total_cars * i)

        # create a stat object
        self.stat = Statistics()

        # initialize the column
        # NOTE: only one column must be simulated
        self.oh.out("init", "creating an EVSE")
        self.column = EVSE(policy, self.debug) 

        # initialize cars
        self.oh.out("init", "creating %s EVs" % str(self.car_freq * self.days))
        self.cars = []
        for i in xrange(self.total_cars):
            # create an EV
            soc = random.randint(0, 6)        
            self.cars.append(EV(soc, EV_CAPACITY, self.debug))


    # run
    def run(self):
        """Method to run the simulation"""
        
        # debug print
        self.oh.out("run", "running the simulation")

        # cycles over the time seconds
        for sec in xrange(self.seconds):
            
            # debug print 
            self.oh.out("run", "simulating second %s of %s" % (sec, self.seconds))
            time.sleep(self.sleep)
            
            # simulate the second!
            self.current_second = sec

            ################################
            #
            # a new vehicles arrives
            #
            ################################
            
            if sec in self.arrival_times:
            
                # recharge the storage using the sunlight
                c, s = self.column.recharge_storage_with_sun(sec)
                self.stat.energy_from_sun += c

                # a new vehicle starts his recharge,
                # so extract the vehicle from the list
                self.current_car += 1
                
                # set the charging status to True
                self.charging = True

                # recharge the car                
                c, s, net = self.column.recharge_vehicle()
                self.cars[self.current_car].recharge(c)

                # if the network must be used, all the energy
                # retrieved from the network goes to the EV,
                # none in the storage, so it should not be
                # recharged.
                if net:
                    self.stat.energy_from_net += c
                else:
                    c, s = self.column.recharge_storage_with_net()
                    self.stat.energy_from_net += c                    
                                    
                # if after this recharge the battery is full
                # then we set the charging status to False
                if self.cars[self.current_car].full():
                    
                    # the recharge is completed
                    self.charging = False
                    
                    # re-enable the recharge from storage
                    self.column.recharge_from_storage = True

            ################################
            #
            # a vehicle is already charging
            #
            ################################

            elif self.charging:

                # recharge the storage using the sunlight
                c, s = self.column.recharge_storage_with_sun(sec)
                self.stat.energy_from_sun += c

                # recharge the car
                c, s, net = self.column.recharge_vehicle()
                self.cars[self.current_car].recharge(c)

                # if the network must be used, all the energy
                # retrieved from the network goes to the EV,
                # none in the storage, so it should not be
                # recharged.
                if net:
                    self.stat.energy_from_net += c
                else:
                    c, s = self.column.recharge_storage_with_net()
                    self.stat.energy_from_net += c          

                # if after this recharge the battery is full
                # then we set the charging status to False
                if self.cars[self.current_car].full():

                    # the recharge is completed
                    self.charging = False
                    
                    # re-enable the recharge from storage
                    self.column.recharge_from_storage = True
                
            ################################
            #
            # no vehicle in charge
            #
            ################################

            else:

                # recharge the storage using the sunlight
                c, s = self.column.recharge_storage_with_sun(sec)
                self.stat.energy_from_sun += c
                
                # recharge the storage using the network
                c, s = self.column.recharge_storage_with_net()
                self.stat.energy_from_net += c

            # add the new soc
            if sec % SAMPLING_FREQUENCE == 0:
                self.stat.soc.append(self.column.storage_soc)

        
        # return the output of a simulation
        return self.stat

# main
if __name__ == "__main__":

    # creating an output helper
    oh = OutputHelper("blue", "Main")

    # read command line arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:c:p:vs:", ["days=", "carfreq=", "policy=", "verbose", "sleep="])
    except getopt.GetoptError as err:
        oh.out("main", "Try this:", True)
        oh.out("main", "$ python simulation.py --days=NUM_OF_DAYS --carfreq=CAR_FREQUENCY --policy=ALWAYS|NEVER|SMART", True)
        sys.exit(2)

    # Init
    carfreq_list = [1]
    days = 1
    policy = 0
    debug = False
    sleep = float(0)

    # parse command line parameters
    for opt, arg in opts:
        if opt in ("-c", "--carfreq"):
            carfreq_list = map(int, arg.split("%"))
        elif opt in ("-d", "--days"):
            days = int(arg)
        elif opt in ("-s", "--sleep"):
            sleep = float(arg)
        elif opt in ("-p", "--policy"):
            try:
                policy = POLICY[arg.upper()]
            except:
                oh.out("main", "Policy must be ALWAYS, NEVER or SMART", True)
        elif opt in ("-v", "--verbose"):
            debug = True
        else:
            assert False, "unhandled option"

    # initialize a stat collector
    sc = StatisticsCollector()

    # iterate over the carfrequencies to be simulated
    # start the simulation
    for carfreq in carfreq_list:
        s = Simulation(days, carfreq, policy, sleep, debug)
        try:
            res = s.run()
            sc.add_simulation(carfreq, res)
        except KeyboardInterrupt:
            oh.out("main", "CTRL-C pressed, bye!")

    # plot the charts
    sc.plot_soc_graph()
    sc.plot_energy_from_net_graph()
    
