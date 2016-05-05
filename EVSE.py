#!/usr/bin/python

# requirements 
import uuid
from simconst import *
from output_helper import *


# EVSE (Electric Vehicle Supply Equipment)
class EVSE:

    # initializer
    def __init__(self, policy, debug):
        """Initializer of the class EVSE"""
        
        # creating an output helper
        self.oh = OutputHelper("green", "EVSE")

        # debug print
        self.oh.out("init", "initializing EVSE")
        
        # setting initial parameters
        self.storage_soc = EVSE_STORAGE_CAPACITY
        self.storage_capacity = EVSE_STORAGE_CAPACITY
        self.recharge_from_storage = True
        self.charging = False
        self.policy = policy
        self.debug = debug


    # recharge with sun
    def recharge_storage_with_sun(self, time_instant):
        """Recharges the local storage using the sunlight"""

        # save the old charge
        oc = self.storage_soc

        # debug print
        if self.debug:
            self.oh.out("recharge_with_sun", "recharging the storage using the sunlight")

        # determine the hour of the day
        # time_instant is the second being simulated
        # Here the corresponding hour is calculated
        # to determine how powerful is the sun light
        hour = int(float(time_instant) / 3600) % 24
        self.storage_soc = min(self.storage_soc + float(SUN_POWER[hour]) / 3600, EVSE_STORAGE_CAPACITY)

        # debug print
        if self.debug:
            percentage = round(100 * float(self.storage_soc) / self.storage_capacity, 2)
            self.oh.out("recharge_with_sun", "current charge %s %%" % percentage)     

        # return the energy gathered and the new soc
        return self.storage_soc - oc, self.storage_soc


    # recharge with the network
    def recharge_storage_with_net(self):
        """Recharges the local storage using the network"""

        if self.policy == 0:
        
            # save the old charge
            oc = self.storage_soc
            
            # debug print
            if self.debug:
                self.oh.out("recharge_with_net", "recharging the storage using the network")

            # determine the new charge
            self.storage_soc = min(self.storage_soc + float(3) / 3600, EVSE_STORAGE_CAPACITY)
            
            # debug print
            percentage = round(100 * float(self.storage_soc) / self.storage_capacity, 2)
            if self.debug:
                self.oh.out("recharge_with_net", "current charge %s %%" % percentage)    

            # return the energy gathered and the new soc
            return self.storage_soc - oc, self.storage_soc
            
        elif self.policy == 1:

            # no network energy used
            return 0, self.storage_soc
            
            
        
        
    # recharge vehicle
    def recharge_vehicle(self):
        """This method is used to recharge an EV. If the capacity of the
        local storage is > 0, then the storage is used, otherwise the EV
        is recharged using the network. The transferred charge is returned"""

        if self.storage_soc > 0 and self.recharge_from_storage:

            # debug print
            if self.debug:
                self.oh.out("recharge_vehicle", "recharging a vehicle using the local storage")
             
            # calculate the amount of energy to be transferred
            # using the local storage
            charge = float(EVSE_STORAGE_POWER) / 3600
            self.storage_soc = max(0, self.storage_soc - charge)

            # return the energy provided, the new soc, False since
            # the storage has been used            
            return charge, self.storage_soc, False

        else:
            
            # debug print
            if self.debug:
                self.out.oh("recharge_vehicle", "recharging a vehicle using the network")
             
            # calculate the amount of energy to be transferred
            # using the network
            charge = float(EVSE_NETWORK_POWER) / 3600

            # disable the recharge from the storage 
            # until this vehicle ends its recharge
            self.recharge_from_storage = False
            
            # return the energy provided, the new soc, True since the network
            # has been used
            return charge, self.storage_soc, True
