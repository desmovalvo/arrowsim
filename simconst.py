#!/usr/bin/python

# EV_CAPACITY represents the maximum amount of charge for an Electric Vehicle (EV)
# The unit of measure is: kWh
EV_CAPACITY = 20

# EVSE_NETWORK_POWER is the power of the Electric Vehicle Supply Equipment (EVSE)
# when charging a vehicle from the network. Unit of measure: kW
EVSE_NETWORK_POWER = 3

# EVSE_STORAGE_POWER is the power of the EVSE when charging a vehicle from the
# local storage. Unit of measure: kW
EVSE_STORAGE_POWER = 150

# EVSE_STORAGE_CAPACITY is the capacity of the local storage of the EVSE.
# The unit of measure is kWh.
EVSE_STORAGE_CAPACITY = 60

# SUN_POWER is the amount of power provided by the sun in a given hour
# of the day.
SUN_POWER = [0, 0, 0, 0, 0, 0, 1, 1.3, 1.67, 2, 2.5, 3, 3, 
             3, 3, 2.5, 2, 1.67, 1.3, 1, 0, 0, 0, 0]
