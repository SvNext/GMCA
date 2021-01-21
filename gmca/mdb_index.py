import numpy as np
import networkx as nx
from abc import ABC, abstractmethod
from .chromosome import Chromosome

class IMDBIndex(ABC):

	@abstractmethod
	def split_clusters(self, chromosome: Chromosome) -> dict:
		pass

	@abstractmethod
	def calculate_index(self, chromosome: Chromosome) -> float:
		pass


class MDBIndex(IMDBIndex):

	def __init__(self, graph: nx.Graph):

		self.graph = graph
		n = graph.number_of_nodes()
		self.time_table = np.zeros((n, n))

		for row in range(n):
			for col in range(row, n):

				value = self.calculate_time(row, col)
				self.time_table[row, col] = value
				self.time_table[col, row] = value


	def split_clusters(self, chromosome: Chromosome) -> dict:
		
		medoids  = np.array(list(chromosome.medoids))
		clusters = { medoid: [] for medoid in medoids }

		for node in self.graph.nodes():

			distance = [self.time_table[node, medoid] for medoid in medoids]
			medoid = medoids[np.argmin(distance)]

			clusters[medoid].append(node)

		return clusters
	

	def calculate_time(self, row: int, col: int) -> float:

		path = nx.shortest_path(self.graph, source = row, 
			target = col, weight = 'Time')

		return np.sum([self.graph.edges[i, j]['Time'] 
			for i, j in zip(path[:-1], path[1:])])


	def calculate_index(self, chromosome: Chromosome) -> float:

		medoids  = np.array(list(chromosome.medoids))
		cluster_data = self.split_clusters(chromosome)
		
		#S = { medoid: np.sum([self.time_table[node, medoid] 
		#	for node in cluster_data[medoid] ]) for medoid in medoids}

		#R = [np.max([(S[medoid1] + S[medoid2]) / self.time_table[medoid1, medoid2 ] 
		#	for medoid2 in medoids if medoid1 != medoid2 ]) for medoid1 in medoids ]

		#return np.mean(R)
		return np.mean([np.sum([self.time_table[node, medoid] 
			for node in cluster_data[medoid]]) for medoid in medoids])