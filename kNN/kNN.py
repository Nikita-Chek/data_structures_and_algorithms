from numpy import random, array
import matplotlib.pyplot as plt
import collections


class Node:
	"""Node of KD Tree"""
	def __init__(self, point=None,
				left=None, right=None):
		self.point = point
		self.left = left
		self.right = right


def build_tree(points: list, dimension, i=0):
	if len(points) == 1:
		return Node(points[0])
	
	elif not points:
		return None
	
	else:
		points.sort(key=lambda y: y[i])
		i = (i + 1) % dimension
		middle = len(points) // 2
		return Node(points[middle],
					build_tree(points[:middle], dimension, i),
					build_tree(points[middle + 1:], dimension, i))


def distance_squared(a: list, b: list):
	assert (len(a) == len(b)), 'points must be of the same dimension'
	return sum((i - j) ** 2 for i, j in zip(a, b))


BestNN = collections.namedtuple("BestNN", ["point", "distance"])
BestNN.__doc__ = """
	Used to keep track of the current best
	guess during a nearest neighbor search.
	"""

class KDTree:
	"""Accepts only a list of 
		points(of the same dimension) as input"""
	def __init__(self, points: list):
		if points:
			self.dimension = len(points[0])
			self.root = build_tree(points, self.dimension)
		else:
			self.root = Node()

	def nearest_neighbor(self, point):
		"""Finding closest neighbor of the given point"""
		best = None

		def searching(point, node, i=0):
			"""Going recursively through the tree to find NN"""
			nonlocal best
			if node is None:
				return
			
			dist = distance_squared(point, node.point)
			if not best or (dist < best.distance):
				best = BestNN(point=node.point, distance=dist)

			axis = i % self.dimension
			diff = point[axis] - node.point[axis]
			if diff <= 0:
				close, far = node.left, node.right
			else:
				close, far = node.right, node.left
			searching(point, close, i + 1)
			if diff ** 2 < best.distance:
				searching(point, far, i+1)
		
		searching(point, self.root, 0)
		return best
	
if __name__ == "__main__":
	points = list(random.rand(100,2))
	for i in range(len(points)):
		points[i] = list(points[i])
	point = list(random.rand(2))
	tree = KDTree(points)
	closest_point = tree.nearest_neighbor(point)
	
	# print(closest_point)
	# print([x[0] for x in points])

	fig = plt.figure()
	plt.scatter([x[0] for x in points], [x[1] for x in points], c='skyblue')
	plt.scatter(point[0], point[1], c='r')
	plt.scatter(closest_point.point[0], closest_point.point[1], c='g')
	plt.show()