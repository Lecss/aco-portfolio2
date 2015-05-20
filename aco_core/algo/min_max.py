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
		for edge in self.graph.edges():
			self.graph.edge[edge[0]][edge[1]]["ph"] = 1

	def run(self, iter_no=35, ant_no = 30):
		self.initialize_pheromones()

		for i in range(0, iter_no):
			self.initialize_ants(ant_no)
			for ant in self.ants:
				solution = ant.construct_solution()
				self.daemon(ant,i)
				self.ants.remove(ant);

			self.best_ant.update_pheromones(ACO.rho)


		for i in range(0, len(self.best_ant.path)-1): 
			from_stage = self.best_ant.path[i]
			to_stage = self.best_ant.path[i+1]

			print self.graph.edge[from_stage][to_stage]["ph"]

	def daemon(self, ant, iteration):
		if self.best_ant is None: 
			self.best_ant = ant
		else:
			if self.best_ant.expected_val < ant.expected_val:
				self.best_ant = ant
				self.best_ant.iter = iteration
