import numpy as np
from abc import ABC, abstractmethod


class IPopulation(ABC):

	@abstractmethod
	def wfould_tour(self, w: int) -> tuple:
		pass


class Population(IPopulation):

	def __init__(self, n_chromosomes: int):

		self._chromosomes  = []
		self.n_chromosomes = n_chromosomes


	def __contains__(self, new_chromosome):

		for chromosome in self._chromosomes:
			if chromosome.medoids == new_chromosome.medoids:
				return True

		return False

	@property
	def chromosomes(self) -> list:
		return self._chromosomes

	@chromosomes.setter
	def chromosomes(self, chromosome) -> None:

		if chromosome not in self:
			self._chromosomes.append(chromosome)


	def wfould_tour(self, w: int = 3) -> tuple:

		indexes = np.random.choice(self.n_chromosomes, w, replace = False)
		chromosomes = np.array(self._chromosomes)[indexes]

		chromosome1 = np.min(chromosomes)
		index = np.random.choice(self.n_chromosomes, 1)[0]
		chromosome2 = self._chromosomes[index]

		return (chromosome1, chromosome2)