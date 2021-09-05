import kd_tree as kd
from numpy import random, array
import matplotlib.pyplot as plt
import cProfile

if __name__ == "__main__":
	points = list(random.rand(1000,2))
	for i in range(len(points)):
		points[i] = list(points[i])
	point = list(random.rand(2))
	cProfile.run("""tree = kd.KDTree(points)""")
	cProfile.run("""closest_point = tree.nearest_neighbor(point)""")
	
	# print(closest_point)
	# print([x[0] for x in points])

	fig = plt.figure()
	plt.scatter([x[0] for x in points], [x[1] for x in points], c='skyblue')
	plt.scatter(point[0], point[1], c='r')
	plt.scatter(closest_point.point[0], closest_point.point[1], c='g')
	plt.show()