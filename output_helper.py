#!/usr/bin/python

# requirements
from termcolor import *

# output helper class
class OutputHelper:

    # constructor for the output helper class
    def __init__(self, color, class_name):
        
        """This is the constructor for the output helper class.
        An output helper should be created for each object"""

        # setting class attributes
        self.color = color
        self.alarm_color = "red"
        self.class_name = class_name


    # out
    def out(self, method, text, alarm=False):
        
        """This method is used to wrap the call to 
        colored (method of the textcolor library"""
    
        heading = "%s::%s> " % (self.class_name, method)

        if alarm:
            print colored(heading, self.alarm_color, attrs=["bold"]) + text            
        else:
            print colored(heading, self.color, attrs=["bold"]) + text
