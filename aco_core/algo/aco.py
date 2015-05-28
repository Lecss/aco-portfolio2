import networkx as nx 
import abc
from solution import Solution
from ant import Ant

class ACO(object):
	__metaclass__ = abc.ABCMeta

	alpha = 1
	betha = 3
	rho = 0.5

	ph_on = True
	heuristics_on = True

	position_heuristic = True
	ratio_heuristic = True

	dynamic = False

	iterations = 75
	ants_no = 85

	food = "food"
	nest = "nest"

	def __init__(self):
		self.G = None
		self.ants = []

	@abc.abstractmethod
	def initialize_pheromones(self):
		return

	@abc.abstractmethod
	def initialize_ants(self, number):
		return

	@abc.abstractmethod
	def run(self, iterations, ants_no):
		return