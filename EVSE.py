#!/usr/bin/python

# requirements 
import uuid
from simconst import *
from termcolor import colored

# EVSE (Electric Vehicle Supply Equipment)
class EVSE:

    # initializer
    def __init__(self):
        """Initializer of the class EVSE"""

        # debug print
        print colored("EVSE::init> ", "green", attrs=["bold"]) + " initializing EVSE"
        
        # setting initial parameters
        self.storage_soc = EVSE_STORAGE_CAPACITY
        self.storage_capacity = EVSE_STORAGE_CAPACITY
        self.charging = False


    # recharge with sun
    def recharge_storage_with_sun(self, time_instant):
        """Recharges the local storage using the sunlight"""

        # debug print
        print colored("EVSE::recharge_with_sun> ", "green", attrs=["bold"]) + " recharging the storage using the sunlight",

        # determine the hour of the day
        # time_instant is the second being simulated
        # Here the corresponding hour is calculated
        # to determine how powerful is the sun light
        hour = int(float(time_instant) / 3600) % 24
        self.storage_soc = min(self.storage_soc + float(SUN_POWER[hour]) / 3600, EVSE_STORAGE_CAPACITY)
        print "(%s)" % round(100 * float(self.storage_soc) / self.storage_capacity, 2)        


    # recharge with the network
    def recharge_storage_with_net(self):
        """Recharges the local storage using the network"""

        # debug print
        print colored("EVSE::recharge_with_net> ", "green", attrs=["bold"]) + " recharging the storage using the network",

        # determine the new charge
        self.storage_soc = min(self.storage_soc + float(3) / 3600, EVSE_STORAGE_CAPACITY)
        print "(%s)" % round(100 * float(self.storage_soc) / self.storage_capacity, 2)
        
        
    # recharge vehicle
    def recharge_vehicle(self):
        """This method is used to recharge an EV. If the capacity of the
        local storage is > 0, then the storage is used, otherwise the EV
        is recharged using the network. The transferred charge is returned"""

        if self.storage_soc > 0:

            # debug print
            print colored("EVSE::recharge_vehicle> ", "green", attrs=["bold"]) + " recharging a vehicle using the local storage"
             
            # calculate the amount of energy to be transferred
            # using the local storage
            charge = float(EVSE_STORAGE_POWER) / 3600
            self.storage_soc = max(0, self.storage_soc - charge)

        else:
            
            # debug print
            print colored("EVSE::recharge_vehicle> ", "green", attrs=["bold"]) + " recharging a vehicle using the network"
             
            # calculate the amount of energy to be transferred
            # using the network
            charge = float(EVSE_NETWORK_POWER) / 3600

        print charge
        return charge
