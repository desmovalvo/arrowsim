#!/usr/bin/python

# requirements 
import uuid
from output_helper import *


# EV (Electric Vehicle)
class EV:

    # initializer
    def __init__(self, soc, capacity, debug):
        """Initializer of the class EV"""

        # create an output helper
        self.oh = OutputHelper("magenta", "EV")

        # assign an UUID to the vehicle
        self.uuid = str(uuid.uuid4())
       
        # read parameters
        # - soc is the initial state of charge (should be comprised between 0 and 5)
        # - capacity is the capacity of the battery (should be ~20)
        self.soc = soc
        self.debug = debug
        self.capacity = capacity

        # debug print
        self.oh.out("init", "initializing EV %s" % (self.uuid))


    # is full?
    def full(self):
        """This method returns True if the EV is fully charged,
        False otherwise"""
        
        if self.soc == self.capacity:

            if self.debug:
                self.oh.out("full?", "recharge of EV %s completed!" % (self.uuid))
            return True

        else:
            if self.debug:
                percentage = round(100 * self.soc / self.capacity, 1)
                self.oh.out("full?", "recharge of EV %s NOT YET completed (%s %%)!" % (self.uuid, percentage))
            return False


    # recharge
    def recharge(self, amount):
        """Method to recharge the EV"""

        # debug print
        if self.debug:
            self.oh.out("recharge", "recharging EV %s of %s kWh" % (self.uuid, round(amount, 5)))

        # setting the new value
        self.soc = min(self.soc + amount, self.capacity)
