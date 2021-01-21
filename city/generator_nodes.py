import numpy as np
from abc import (ABC, abstractmethod, abstractproperty)


class IGenerator(ABC):

	@abstractproperty
	def nodes(self) -> list:
		pass

	@abstractmethod
	def generate_nodes(self) -> None:
		pass


class GeneratorNodes(IGenerator):

	def __init__(self, n_nodes: int, n_side: int, radius: float = 1):

		self._nodes = []
		self.radius = radius

		self.n_side  = n_side
		self.n_nodes = n_nodes

		self.generate_nodes()


	@property
	def nodes(self) -> list:
		return self._nodes


	def zoom(self, cnode: tuple) -> list:

		# cnode -> central node
		x_min = cnode[0] - 2 * self.radius
		x_max = cnode[0] + 2 * self.radius

		y_min = cnode[1] - 2 * self.radius
		y_max = cnode[1] + 2 * self.radius

		neighborhood = [node for node in self._nodes 
						if x_min <= node[0] <= x_max]

		neighborhood = [node for node in neighborhood
						if y_min <= node[1] <= y_max]

		return neighborhood
	

	def check_position(self, node: tuple) -> bool:

		neighborhood = self.zoom(node)
		if neighborhood != []:

			for neighbor in neighborhood:
				dx = neighbor[0] - node[0]
				dy = neighbor[1] - node[1]

				if np.hypot(dx, dy) < 2 * self.radius:
					return False

		return True


	def generate_nodes(self) -> None:

		self._nodes.append((0, 0))
		for _ in range(self.n_nodes):

			position = False
			while position == False:

				#choice random node and angle
				index = np.random.choice(len(self._nodes), 1)[0]
				angle = np.random.uniform(0, 2 * np.pi, 1)
				
				#create new node
				dx = 2 * self.radius * np.cos(angle)
				dy = 2 * self.radius * np.sin(angle)

				# find all neighborhood for node
				node = self._nodes[index]
				neighborhood = self.zoom(node)

				# check number neighborhood
				if len(neighborhood) <= (self.n_side + 1):
					new_node = (node[0] + dx[0], node[1] + dy[0])

					# check if the position is free for a new point
					position = self.check_position(new_node)

			# add new node to list
			self._nodes.append(new_node)