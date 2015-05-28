import abc
from aco import ACO

from environment import GraphWrapper
from ant import Ant
from solution import Solution

import random
import math
import time
import json
import timeit 

from sets import Set


class MinMax(ACO):
	def __init__(self):	
		self.ants = []
		self.graph = GraphWrapper().get_graph()
		self.best_ant = None

		self.startTime = timeit.default_timer()
		self.endTime = timeit.default_timer()
		self.last_iter_best = 0


	def initialize_ants(self, no):
		for i in range(0, no): 
			self.ants.append(Ant(self.graph, ACO.ph_on, ACO.heuristics_on, ACO.alpha, ACO.betha, ACO.position_heuristic, ACO.ratio_heuristic, ACO.dynamic))


	def initialize_pheromones(self):
		for edge in self.graph.edges():
			self.graph.edge[edge[0]][edge[1]]["ph"] = 1

	def run(self, iter_no=ACO.iterations, ant_no = ACO.ants_no):
		self.initialize_pheromones()

		for i in range(0, iter_no):
			self.initialize_ants(ant_no)
			for ant in self.ants:
				solution = ant.construct_solution()
				self.daemon(ant,i)
				self.ants.remove(ant);

			self.best_ant.update_pheromones(ACO.rho)



	def daemon(self, ant, iteration):
		if self.best_ant is None: 
			self.best_ant = ant
		else:
			if self.best_ant.expected_val < ant.expected_val:
				self.best_ant = ant
				self.best_ant.iter = iteration
				self.best_ant.timeToFind = -1 * (self.startTime - timeit.default_timer())


		"""min_ph = 1


		if iteration > 15:
			for edge in self.graph.edges():
				if self.graph.edge[edge[0]][edge[1]]['ph'] < min_ph:
					min_ph = self.graph.edge[edge[0]][edge[1]]['ph']

			for edge in self.graph.edges():
				if self.graph.edge[edge[0]][edge[1]]['ph'] == min_ph and  edge[0] not in self.best_ant.path and edge[1] not in self.best_ant.path:
					self.graph.remove_edge(*edge)"""

