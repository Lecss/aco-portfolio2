import abc
from aco import ACO

from environment import GraphWrapper
from ant import Ant
from solution import Solution

import random
import math
import time
import json

from sets import Set


class MinMax(ACO):
    def __init__(self):	
    	self.ants = []
    	self.graph = GraphWrapper().get_graph()
    	self.best_ant = None


    def initialize_ants(self, no):
    	for i in range(0, no): 
    		self.ants.append(Ant(self.graph))


    def initialize_pheromones(self):
    	pass

    def run(self, iter_no=100, ant_no = 80):
    	self.initialize_pheromones()

    	for i in range(0, iter_no):
    		self.initialize_ants(ant_no)
    		for ant in self.ants:
    			solution = ant.construct_solution()
    			self.daemon(ant)
    			self.ants.remove(ant);

    		print self.best_ant.expected_val


    def daemon(self, ant):
    	if self.best_ant is None: 
    		self.best_ant = ant
    	else:
    		if self.best_ant.expected_val < ant.expected_val:
    			self.best_ant = ant

