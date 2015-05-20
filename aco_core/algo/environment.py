import networkx as nx
from networkx.readwrite import json_graph
import json
from aco import ACO

from portfolio.models import Portfolio,Drug


class GraphWrapper():
	
	def __init__(self, portfolio_id = 1):	
		self.test = True
		self.portfolio = Portfolio.objects.get(id=portfolio_id)
		self.portfolio.duration = 12
		self.portfolio.save()
		self.drugs = self.portfolio.drug_set.all()
		self.graph = None

	def get_graph(self):
		if self.graph is None:
			graph = self.create_graph()
			return graph
		else:
			return self.graph

	def create_graph(self):
		g = nx.Graph(drugs={}, drug_stages={})

		self.add_graph_attrs(g)
		self.add_nodes(g)
		self.add_edges(g)
		
		return g

	def add_nodes(self, g):
		for drug in self.drugs:
			c = 0
			final_stage_str = "Two" if len(drug.stage_set.all()) == 2 else "Three"
			for stage in drug.stage_set.all():
				g.add_node( (drug.name + stage.name).strip(), portfolio=self.portfolio, drug=drug, stage=stage, active = True if c is 0 else False, last_stage = final_stage_str in stage.name)
				c+=1
	
		g.add_node(ACO.food, cost=0, duration=0, active=True, portfolio=self.portfolio,  index=1)
		g.add_node(ACO.nest, cost=0, duration=0, active = True, portfolio=self.portfolio, index=1)

	def add_edges(self, g):
		for n in g.nodes():
			for y in g.nodes():
				if n is not y:
					g.add_edge(n, y)


	def add_graph_attrs(self,g):
		for d in self.drugs:
			g.graph['drugs'][d.name] = d
			g.graph['drug_stages'][d.name] =  d.stage_set.all()


