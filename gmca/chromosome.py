import numpy as np
from abc import ABC
from functools import total_ordering
from abc import abstractproperty, abstractmethod


class IChromosome(ABC):

	@abstractproperty
	def SICV(self) -> float:
		pass


@total_ordering
class Chromosome(IChromosome):

	def __init__(self, medoids: set):

		# Sum of Intra-Cluster Variation
		self._SICV = None
		self.medoids = medoids


	@property
	def k(self) -> int:
		return len(self.medoids)


	@property
	def SICV(self) -> float:
		return self._SICV


	@SICV.setter
	def SICV(self, value: float):
		self._SICV = value


	def __lt__(self, chromosome) -> bool:
		return self.SICV < chromosome.SICV


	def __eq__(self, chromosome) -> bool:
		return self.SICV == chromosome.SICV