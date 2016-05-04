#!/usr/bin/python

# requirements 
import uuid
from termcolor import colored

# EV (Electric Vehicle)
class EV:

    # initializer
    def __init__(self, soc, capacity):
        """Initializer of the class EV"""
        
        # assign an UUID to the vehicle
        self.uuid = str(uuid.uuid4())

        # debug print
        print colored("EV::init> ", "magenta", attrs=["bold"]) + " initializing EV %s" % (self.uuid)
        
        # read parameters
        # - soc is the initial state of charge (should be comprised between 0 and 5)
        # - capacity is the capacity of the battery (should be ~20)
        self.soc = soc
        self.capacity = capacity


    # is full?
    def full(self):
        """This method returns True if the EV is fully charged,
        False otherwise"""
        
        if self.soc == self.capacity:
            print colored("EV::full> ", "magenta", attrs=["bold"]) + " recharge of EV %s completed!" % (self.uuid)
            return True
        else:
            print colored("EV::full> ", "magenta", attrs=["bold"]) + " recharge of EV %s NOT YET completed (%s)!" % (self.uuid, round(100 * self.soc / self.capacity, 1))
            return False


    # recharge
    def recharge(self, amount):
        """Method to recharge the EV"""

        # debug print
        print colored("EV::recharge> ", "magenta", attrs=["bold"]) + " Recharging EV %s of %s kWh" % (self.uuid, round(amount, 5))

        # setting the new value
        self.soc = min(self.soc + amount, self.capacity)
