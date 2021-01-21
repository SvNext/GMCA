import numpy as np
import networkx as nx
from abc import abstractmethod
from abc import ABC, abstractproperty

from gmca.mdb_index import MDBIndex
from gmca.chromosome import Chromosome
from gmca.population import Population


class IGMCA(ABC):
	
	@abstractproperty
	def clusters(self) -> dict:
		pass


	@abstractproperty
	def TB_chromosome(self) -> Chromosome:
		pass


	@abstractmethod
	def fit(self, n_iter: int) -> None:
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

			medoids = np.random.choice(graph.nodes(), self.k_max, replace = False)			
			chromosome = self.create_chromosome(set(list(medoids)))
			self.population.chromosomes = chromosome


	@property
	def clusters(self) -> dict:
		return self.mdb.split_clusters(self.TB_chromosome)
	

	@property	
	def TB_chromosome(self) -> Chromosome:
		return self.population.chromosomes[0]


	def create_chromosome(self, medoids: set) -> Chromosome:

		chromosome = Chromosome(medoids)
		chromosome = self.heuristic_operator(chromosome)

		mdb_value = self.mdb.calculate_index(chromosome)
		chromosome.SICV = mdb_value

		return chromosome


	def heuristic_operator(self, chromosome: Chromosome, 
						n_subset: float = 0.5) -> Chromosome:

		medoids  = list(chromosome.medoids)
		cluster_data = self.mdb.split_clusters(chromosome)
		
		for medoid in medoids.copy():

			n_node = len(cluster_data[medoid])
			subset = np.random.uniform(0.3, 0.7, 1)[0]
			nodes = np.random.choice(cluster_data[medoid], 
				int(n_node * subset) + 1, replace = False)

			distance = [self.mdb.time_table[node, medoid] for node in nodes]
			upmedoid = nodes[np.argmin(distance)]

			medoids.remove(medoid)
			medoids.append(upmedoid)

		return Chromosome(set(medoids))


	def crossover(self, n_subset: float = 0.5, w: float = 3) -> list:

		new_population = []
		for _ in range(int(self.n_chromosomes * n_subset)):

			p1, p2 = self.population.wfould_tour(w)
			pmix = p1.medoids.union(p2.medoids)

			child1 = np.random.choice(list(pmix), self.k_max, replace = False)
			child2 = np.random.choice(list(pmix), self.k_max, replace = False)

			new_population.append(self.create_chromosome(set(list(child1))))
			new_population.append(self.create_chromosome(set(list(child2))))

		return new_population


	def mutation(self, new_population: list, n_subset: float = 0.25) -> list:

		n_mutation  = int(len(new_population) * n_subset)
		chromosomes = np.random.choice(new_population, n_mutation, replace = False)

		for chromosome in chromosomes:

			medoids = chromosome.medoids
			nodes = set(self.graph.nodes())

			dmedoid = np.random.choice(list(medoids), 1)[0]
			nmedoid = np.random.choice(list(set(nodes).difference(medoids)), 1)[0]

			medoids.remove(dmedoid)
			medoids.add(nmedoid)

			new_chromosome = self.create_chromosome(medoids)
			
			new_population.remove(chromosome)
			new_population.append(new_chromosome)

		return new_population


	def fit(self, n_iter: int = 150) -> None:
		for i in range(n_iter):

			new_population = self.crossover()
			new_population = self.mutation(new_population)

			for chromosome in new_population:
				self.population.chromosomes = chromosome

			print('Iteration: {}'.format(i))
			for chromosome in self.population.chromosomes[:5]:
				print('SICV: {:0.3f}, Medoids: {}'.format(chromosome.SICV, chromosome.medoids))

			print()

