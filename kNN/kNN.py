from numpy import random, array
import matplotlib.pyplot as plt

class Node:
	"""Node of KD Tree"""
	def __init__(self, coords=None,
				left=None, right=None):
		self.coords = coords
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
	# return sum((a[i] - b[i]) ** 2 for i in range(len(a)))

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
		return nearest_point(point, self.root, self.dimension)

def nearest_point(point, node, dimension, i=0, best=None):
	"""Finding closest neighbor of the given point"""
	if node is not None:
		dist = distance_squared(point, node.coords)
		d_axis = node.coords[i] - point[i]
		if not best or (dist < best[0]):
			best = [dist, node.coords]
		i = (i + 1) % dimension
		for _ in [d_axis < 0] + [d_axis >= 0] * (d_axis ** 2 < best[0]):
			if _:
				nearest_point(point, node.right, dimension, i, best)
			else:
				nearest_point(point, node.left, dimension, i, best)
	return best
	
if __name__ == "__main__":
	points = list(random.rand(100,2))
	# points = random.rand(50,2)
	for i in range(len(points)):
		points[i] = list(points[i])

	tree = KDTree(points)
	point = list(random.rand(2))
	# points = array(points)
	closest_point = tree.nearest_neighbor(point)
	# print(points)
	# print([x[0] for x in points])

	fig = plt.figure()
	# plt.scatter(points[:,0], points[:,1], c='b')
	plt.scatter([x[0] for x in points], [x[1] for x in points], c='b')
	plt.scatter(point[0], point[1], c='r')
	plt.scatter(closest_point[1][0], closest_point[1][1], c='g')
	plt.show()