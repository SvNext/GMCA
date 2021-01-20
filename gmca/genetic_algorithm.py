import numpy as np
import networkx as nx
from abc import ABC, abstractproperty

from gmca.mdb_index import MDBIndex
from gmca.chromosome import Chromosome
from gmca.population import Population


class IGMCA(ABC):
	pass


class GMCA(IGMCA):

	def __init__(self, graph: nx.Graph, 
				k_max: int, n_chromosomes: int):

		self.graph = graph
		self.k_max = k_max
		self.n_chromosomes = n_chromosomes

		self.mdb = MDBIndex(graph)
		self.population = Population(n_chromosomes)

		for _ in range(n_chromosomes):

			k = np.random.randint(2, self.k_max + 1, 1)
			medoids = np.random.choice(graph.nodes(), k, replace = False)

			new_chromosome = Chromosome(set(medoids))
			new_chromosome = self.heuristic_operator(new_chromosome)

			mdb_value = self.mdb.calculate_index(new_chromosome)
			new_chromosome.SICV = mdb_value

			self.population.chromosomes = new_chromosome


	def heuristic_operator(self, chromosome: Chromosome, 
						n_subset: float = 0.5) -> Chromosome:

		# split by clasters
		medoids  = np.array(chromosome.medoids)
		clusters = { medoid: [] for medoid in medoids }

		for node in self.graph.nodes():

			distance = [self.time_table[node, medoid] for medoid in medoids]
			medoid = medoids[np.argmin(distance)]

			clusters[medoid].append(node)

		# update medoids
		for medoid in medoids.copy():

			n_node = len(clusters[medoid])
			subset = np.random.uniform(0.3, 0.7, 1)[0]
			nodes = np.random.choice(self.graph.nodes(), 
				int(n_node * subset) + 1, replace = False)

			distance = [self.mdb.time_table[node, medoid] for node in nodes]
			upmedoid = nodes[np.argmin(distance)]

			medoids.remove(medoid)
			medoids.append(upmedoid)

		return Chromosome(set(medoids))