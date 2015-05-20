import copy
from sets import Set
from operator import mul

class ExpectedValue():
	min_so_far = 0
	calculated_before = {}

	def __init__(self, G, path, failed=[]):
		self.years = {}
		self.G = G
		self.path = path
		self.portfolio = self.G.node[self.G.nodes()[0]]["portfolio"]

	def init_years(self):
		for x in range(0, self.portfolio.duration):
			self.years[x] = {"items": [], "restricted_items": [], "budget": self.portfolio.budget, "complete": [],
							 "generated": 0}
	  
	def compute(self, failed=[]):
		self.init_years()
		self.failed_drugs = [self.G.node[x]["drug"]["name"] for x in failed]
	
		#self.set_path = Set() if len(path) == 0 else Set(path)
		
		for stage in self.path:
			if stage is "food" or stage is "nest":
				continue
			if not self.add_to_year(stage):
				return None
		
		#calculate the expected value
		expected_value = self.expected_value()

		#update the minimum found so far
		if expected_value < ExpectedValue.min_so_far:
			min_so_far = expected_value

		return expected_value

	def add_to_year(self, stage):
		complement = self.get_stage_complement(stage)
		stage_cost = self.G.node[stage]["stage"].cost
		stage_duration = self.G.node[stage]["stage"].duration

		min_invest_year = 0

		for x in self.years:
			if self.years[x]["budget"] - stage_cost < 0 or stage in self.years[x]['restricted_items']:
				min_invest_year = x + 1

		can_add = self.portfolio.duration - min_invest_year > stage_duration

		if can_add:
			invested_in_year = min_invest_year

			for x in range(min_invest_year, self.portfolio.duration - stage_duration):
				if self.years[x]["budget"] - stage_cost >= 0:
					if stage not in self.years[x]["restricted_items"]:
						self.years[x]["items"].append(stage)
						invested_in_year = x
						break

			for x in range(invested_in_year, self.portfolio.duration):
				self.years[x]["budget"] = self.years[x]["budget"] - stage_cost

			for x in range(0, invested_in_year + stage_duration):
				self.years[x]["restricted_items"] += complement

			if self.G.node[stage]["last_stage"]:
				self.years[invested_in_year + stage_duration]["complete"].append(self.G.node[stage]["drug"].name)

				if (invested_in_year + stage_duration) <= self.portfolio.duration:
					for x in range(invested_in_year + stage_duration, self.portfolio.duration):
						# print self.years[x]["generated"]
						diff = x - invested_in_year + stage_duration

						self.years[x]["generated"] = self.years[x]["generated"] \
													 + self.G.node[stage]["drug"].profit_year * diff
						self.years[x]["budget"] = self.years[x]["budget"] \
												  + self.G.node[stage]["drug"].profit_year * diff
			return True
		else:
			return False

	def years_(self):
		return self.years

	def get_stage_complement(self, node):
		if node is "food" or node is "nest":
			return []

		complement = []
		drug = self.G.node[node]["drug"]

		for stage in self.G.graph['drug_stages'][drug.name]:
			complement.append(drug.name + stage.name.strip()) 
		complement.remove(node)
		
		return complement 


	def expected_value(self):
		cost = self.get_fixed_cost()
		complete_expected = 0

		# compute the generated value across the years
		for x in self.years:
			for d in self.years[x]["complete"]:
				if d == "nest" or d == "food":
					continue

				drug = self.G.graph['drugs'][d]
				cummulated_prob = reduce(mul, [o.fail for o in self.G.graph['drug_stages'][d]])
				complete_expected += cummulated_prob * drug.profit_year * (self.portfolio.duration - x)
		
		return complete_expected + cost

	def get_fixed_cost(self):
		cost = 0
		for i in self.path:
			#stage_count = self.G.node[i]["drug"]["stages_count"]
			if i == "nest" or i == "food":
				continue
 			cost += -1 * self.G.node[i]["stage"].cost

		return cost

	def print_trace(self):
		generated = [self.years[x]["generated"] for x in self.years]
		print generated

		for x in self.years:
			print "\t" + str(x) + ": " + str(self.years[x]["items"]) + ": " + str(
				self.years[x]["budget"])  # + str(self.years[x]["restricted_items"])
			print self.years[x]["complete"]



