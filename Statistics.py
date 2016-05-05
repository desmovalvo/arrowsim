#!/usr/bin/python

# requirements
import pygal
from pygal.style import CleanStyle
from datetime import *
from output_helper import *

# class Statistics
class Statistics:

    """This class is used to collect statistics of a
    single simulation"""


    def __init__(self):
        
        """Constructor for the statistics collector"""

        # create an output helper
        self.oh = OutputHelper("yellow", "Statistics")

        # initializing class attributes
        # - network_usage represents the amount of kWh gathered from
        #   the network to recharge the local storage and the vehicles
        self.energy_from_net = 0
        self.energy_from_sun = 0
        self.soc = []
        
        # debug print
        self.oh.out("init", "Initializing the Statistics method")


# class statistics collector
class StatisticsCollector:

    """This class is used to collect statistics for
    multiple simulations and plot graphs"""

    def __init__(self):
        
        """Constructor for the statistics collector class"""

        # create an output helper
        self.oh = OutputHelper("yellow", "StatCollector")
        self.oh.out("init", "Initializing the StatCollector")
        
        # initialize an empty dictionary to
        # collect statistics from the different
        # simulations
        # the keys will be the car frequencies since
        # this is the parameter that will be varied
        # over the different simulations
        self.simulations = {}

        # determine a label to append to the rendered charts
        self.label = str(datetime.now().strftime("%Y%m%d-%H%M"))


    def add_simulation(self, carfreq, stat):
        
        """method to add the results of a simulation
        to the collector"""

        # debug print
        self.oh.out("add_simulation", "Adding simulation for carfreq %s" % carfreq)

        # add a new key
        self.simulations[str(carfreq)] = {}
        
        # fill that dictionary
        self.simulations[str(carfreq)]["soc"] = stat.soc
        self.simulations[str(carfreq)]["energy_from_net"] = stat.energy_from_net
        self.simulations[str(carfreq)]["energy_from_sun"] = stat.energy_from_sun


    def plot_soc_graph(self):

        """draws the soc line"""

        # create an instance of the Line class
        lc = pygal.Line(show_dots = False, 
                        style = CleanStyle, 
                        x_title = "time (s)", 
                        y_title = "State of charge (kWh)")

        # set the title
        lc.title = "State of charge during the simulation"

        # fill the line chart
        for k in sorted(self.simulations.keys(), key=int):
            lc.add(k, self.simulations[k]["soc"])

        # render it to file
        lc.render_to_file("soc-graph-%s.svg" % self.label)
        

    def plot_energy_from_net_graph(self):

        """draws a graph for the network energy usage"""

        # create an instance of the Line class
        lc = pygal.Line(style=CleanStyle, 
                        x_title = "vehicles", 
                        y_title = "Energy from Network (kWh)",
                        show_legend = False)

        # set the title
        lc.title = "State of charge during the simulation"

        # fill the line chart
        values = []
        for k in sorted(self.simulations.keys(), key=int):
            print self.simulations[k]["energy_from_net"]
            values.append(self.simulations[k]["energy_from_net"])
        lc.add("foo", values)

        # render it to file
        lc.render_to_file("net-graph-%s.svg" % self.label)
