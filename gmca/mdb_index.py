import numpy as np
import networkx as nx
from abc import ABC, abstractmethod


class IMDBIndex(ABC):

	@abstractmethod
	def calculate_index(self, chromosome) -> float:
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


	def calculate_time(self, row: int, col: int) -> float:

		path = nx.shortest_path(self.graph, source = row, 
			target = col, weight = 'Time')

		print(path)
		return np.sum([self.graph.edges[i, j]['Time'] 
			for i, j in zip(path[:-1], path[1:])])


	def calculate_index(self, chromosome) -> float:


		# split by clusters
		medoids  = np.array(chromosome.medoids)
		clusters = { medoid: [] for medoid in medoids }

		for node in self.graph.nodes():

			distance = [self.time_table[node, medoid] for medoid in medoids]
			medoid = medoids[np.argmin(distance)]

			clusters[medoid].append(node)

		# calculate index
		value = np.sum([np.sum(clusters[medoid]) for medoid in medoids])
		return value