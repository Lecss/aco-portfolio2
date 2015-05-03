import networkx as nx
from networkx.readwrite import json_graph
from expected_value import ExpectedValue
import random
import math
import json


class Ant():
	ant_id = 0
	food = "food"
	nest = "nest"

	def __init__(self, graph):	
		self.id = 0
		self.set_id()
		self.graph = graph
		self.path = []
		self.used_nodes = {}
		self.not_active = [n for n in self.graph.nodes() if not self.graph.node[n]["active"]]

		self.expected_val = 0

		self.next_stage = {"One": "Two", "Two" : "Three"}
		#print self.not_active
		self.curr_node = None

	def set_id(self):
		self.ant_id = Ant.ant_id 
		Ant.ant_id +=1

	def construct_solution(self):
		self.move_to(Ant.nest)

		isFood = False
		while(not isFood):
			next_node = self.choose_next_node(self.curr_node)
			self.move_to(next_node)
			isFood = next_node == Ant.food

		#print self.path

		self.expected_val = self.evaluate_solution()
		return self.expected_val


	def sanitize_neighbors(self, neighbors):
		return [item for item in neighbors if not self.used_nodes.has_key(item) and item not in self.not_active]

	def choose_next_node(self, curr_node):
		neighbors = self.sanitize_neighbors(self.graph.neighbors(curr_node))
		if len(neighbors) == 0:
			return Ant.food

		return neighbors[random.randint(0, len(neighbors) - 1)]


	def move_to(self, node):
		self.curr_node = node
		self.path.append(node)
		self.used_nodes[node] = True

		#print self.not_active
		self.enable_next_node(node)

	def enable_next_node(self, node):
		if node == "nest" or node == "food":
			return

		drug_name = (self.graph.node[node]["drug"]).name
		stage_name = node.replace(drug_name, "")

		try:
			next_stage = self.next_stage[stage_name]
			self.not_active.remove(drug_name + next_stage)
		except Exception:
			return

	def update_pheromone(self):
		pass

	def evaluate_solution(self):
		expected_val = ExpectedValue(self.graph, self.path)
		e = expected_val.compute()

		return e


	def get_neighbours(self):
		return self.graph