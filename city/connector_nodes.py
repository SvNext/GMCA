import numpy as np
from abc import (ABC, abstractmethod,
	abstractproperty) 


class IConnector:

	@abstractproperty
	def connections(self) -> list:
		pass

	@abstractmethod
	def connect_nodes(self, nodes: list) -> list:
		pass


class ConnectorNodes(IConnector):

	def __init__(self, nodes: list, radius: float = 1):
		
		self.nodes = nodes
		self.radius = radius
		self._connections = []


	@property
	def connections(self) -> list:
		return self._connections


	def zoom(self, cnode: tuple) -> list:
		#cnode -> central node
		
		x_min = cnode[0] - 2 * self.radius
		x_max = cnode[0] + 2 * self.radius
		
		y_min = cnode[1] - 2 * self.radius
		y_max = cnode[1] + 2 * self.radius
		
		neighborhood = [node for node in self.nodes 
						if x_min <= node[0] <= x_max]

		neighborhood = [node for node in neighborhood 
						if y_min <= node[1] <= y_max]

		return neighborhood


	def connect_nodes(self) -> None:

		for node in self.nodes:

			neighborhood = self.zoom(node)
			for neighbor in neighborhood.copy():


				dx = neighbor[0] - node[0]
				dy = neighbor[1] - node[1]

				if np.hypot(dx, dy) < 2 * self.radius:
					neighborhood.remove(neighbor)

			for neighbor in neighborhood:
				if (node != neighbor) and ((neighbor, node) not in self._connections):
					self._connections.append((node, neighbor))