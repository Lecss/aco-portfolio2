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

	def __init__(self, graph, ph_on, heuristics_on, alpha, betha, p_h, r_h, dynamic):	
		self.id = 0
		self.set_id()
		self.graph = graph
		self.path = []
		self.used_nodes = {}
		self.not_active = [n for n in self.graph.nodes() if not self.graph.node[n]["active"]]

		self.heuristics_on = heuristics_on
		self.ph_on = ph_on
		self.alpha = alpha
		self.betha = betha
		self.pos_heuristic = p_h
		self.ratio_heuristic = r_h
		self.dynamic = dynamic

		self.expected_val = 0

		self.next_stage = {"One": "Two", "Two" : "Three"}
		#print self.not_active
		self.curr_node = None
		self.max_path_length = 0

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
		fitnesses = []

		neighbors = self.sanitize_neighbors(self.graph.neighbors(curr_node))
		if len(neighbors) == 0:
			return Ant.food

		neighbor_ph_sum = 0
		for n in neighbors: 
			ph= self.graph.edge[curr_node][n]["ph"] if self.ph_on else 1
			neighbor_ph_sum += ph
			
			heuristics = self.get_heuristics(n) if self.heuristics_on else 1
			neighbor_ph_sum += heuristics

			#prob = math.pow(ph, 1) * math.pow(heuristics,2)
			prob = math.pow(ph, self.alpha) * math.pow(heuristics, self.betha)
			fitnesses.append(prob)

		for i,f in enumerate(fitnesses):
			fitnesses[i] /= neighbor_ph_sum

		selection = self.roulette_select(neighbors, fitnesses, len(neighbors))
		return selection[random.randint(0, len(selection) - 1)]

	def get_heuristics(self,node):
		result = 0
		h1 = self.related_investments_heuristic(node) if self.pos_heuristic else 0
		h2 = self.drug_ratio_heuristic(node) if self.ratio_heuristic else 0
	
		result+= h1 + h2

		if result is 0: 
			return 1

		return result

	def related_investments_heuristic(self, node):
		if node == "food":
			return 0.2
		
		stage = self.graph.node[node]["stage"]
		#total_stages = len(self.graph.graph['drug_stages'][drug.name])
		
		stage_map = { "One": 0.4, "Two": 0.6, "Three": 1}
		return stage_map[stage.name.strip()]

	def drug_ratio_heuristic(self, node):
		if node == "food" or node =="nest":
			return 1
		return 1 - 1/self.graph.node[node]["drug"].profit_year

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

	def update_pheromones(self, evap_rate):
		#evaporate
		for edge in self.graph.edges():
			ph = self.graph.edge[edge[0]][edge[1]]["ph"]
			self.graph.edge[edge[0]][edge[1]]["ph"] = (1-evap_rate)*ph

		if self.expected_val is 0 :
			return 
		#increase ph levels 
		for i in range(0, len(self.path)-1): 
			from_stage = self.path[i]
			to_stage = self.path[i+1]

			try:
				self.graph.edge[from_stage][to_stage]["ph"] += min(1- ((1/(self.expected_val / (i+1)))) * 2, 1)

				if self.graph.edge[from_stage][to_stage]["ph"] > 1: 
					self.graph.edge[from_stage][to_stage]["ph"] = 1

				if self.graph.edge[from_stage][to_stage]["ph"] < 0.22: 
					self.graph.edge[from_stage][to_stage]["ph"] = 0.22
			except:
				pass
		"""for edge in self.graph.edges():
			ph = self.graph.edge[edge[0]][edge[1]]["ph"]
			print ph
		print "------------" """

	def evaluate_solution(self):
		self.remove_unfinished()

		expected_val = ExpectedValue(self.graph, self.path)
		e = expected_val.compute()

		return e

	def remove_unfinished(self):
		for n in self.path:
			if n == "food" or n == "nest":
				continue
			drug = self.graph.node[n]["drug"]
			stage = self.graph.node[n]["stage"]
			total_stages = len(self.graph.graph['drug_stages'][drug.name])

			if (total_stages == 2) and (drug.name + "Two" not in self.path):
				self.path.remove(n)
			elif (total_stages == 3) and (drug.name + "Three" not in self.path):
				self.path.remove(n)


	def roulette_select(self, population, fitnesses, num):
		""" Roulette selection, implemented according to:
			<http://stackoverflow.com/questions/177271/roulette
			-selection-in-genetic-algorithms/177278#177278>
			http://stackoverflow.com/questions/298301/roulette-wheel-selection-algorithm"""

		total_fitness = float(sum(fitnesses))
		rel_fitness = [f / total_fitness for f in fitnesses]
		# Generate probability intervals for each individual
		probs = [sum(rel_fitness[:i + 1]) for i in range(len(rel_fitness))]
		# Draw new population
		new_population = []
		for n in xrange(num):
			r = random.random()
			for (i, individual) in enumerate(population):
				if r <= probs[i]:
					new_population.append(individual)
					break
		return new_population



