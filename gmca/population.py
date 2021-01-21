import numpy as np
from abc import abstractproperty
from abc import ABC, abstractmethod


class IPopulation(ABC):

	@abstractproperty
	def chromosomes(self) -> list:
		pass

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
		
		if len(self._chromosomes) > self.n_chromosomes:
			self._chromosomes.sort()
			self._chromosomes = self._chromosomes[:self.n_chromosomes]


	def wfould_tour(self, w: int = 3) -> tuple:

		
		chromosomes = np.random.choice(self._chromosomes, w,replace = False)
		
		chromosome1 = np.min(chromosomes)
		chromosome2 = np.random.choice(self._chromosomes, 1)[0]

		return (chromosome1, chromosome2)