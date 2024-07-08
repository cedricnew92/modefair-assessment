import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def distance(point1, point2):
	return np.sqrt(np.sum((point1 - point2)**2))

def ant_colony_optimization(points, n_ants, n_iterations, alpha, beta, evaporation_rate, Q):
	n_points = len(points)
	pheromone = np.ones((n_points, n_points))
	print('Init')
	print(pheromone)
	best_path = None
	best_path_length = np.inf
	
	for iteration in range(n_iterations):
		paths = []
		path_lengths = []
		
		for ant in range(n_ants):
			visited = [False]*n_points
			current_point = np.random.randint(n_points)
			visited[current_point] = True
			path = [current_point]
			path_length = 0
			
			while False in visited:
				temp = np.logical_not(visited)
				unvisited = np.where(temp)[0]
				probabilities = np.zeros(len(unvisited))
				
				# print(unvisited)
				for i, unvisited_point in enumerate(unvisited):
					pheromone_level = pheromone[current_point, unvisited_point]
					from_point = points[current_point]
					to_point = points[unvisited_point]
					heuristic_information = distance(from_point, to_point)
					probabilities[i] = pheromone_level**alpha / heuristic_information**beta
					# print("%-*s %-*s %-*s" % (15, from_point, 15, to_point, 15, heuristic_information))
					# print(probabilities[i])
				
				probabilities /= np.sum(probabilities)
				# print(probabilities)
				next_point = np.random.choice(unvisited, p=probabilities)
				# print(next_point)
				# print('\n\n\n')
				path.append(next_point)
				path_length += distance(points[current_point], points[next_point])
				visited[next_point] = True
				current_point = next_point
				# print(path)
				# print('\n')

			# print('\n\n\n\n')

			paths.append(path)
			# print('paths')
			# print(paths)
			# print('\n\n\n')
			path_lengths.append(path_length)
			
			if path_length < best_path_length:
				best_path = path
				best_path_length = path_length
		
		pheromone *= evaporation_rate

		print('zip')
		print(list(zip(paths, path_lengths)))
		print('\n')

		for path, path_length in zip(paths, path_lengths):
			# print('path : ' + str(path) + " ; path_length : " + str(path_length))
			for i in range(n_points-1):
				print(path[i])
				pheromone[path[i], path[i+1]] += Q/path_length
				print(pheromone)
				print('\n')
			pheromone[path[-1], path[0]] += Q/path_length
			print(pheromone)
	
	fig = plt.figure(figsize=(8, 6))
	ax = fig.add_subplot(111, projection='2d')
	ax.scatter(points[:,0], points[:,1], c='r', marker='o')
	
	for i in range(n_points-1):
		ax.plot([points[best_path[i],0], points[best_path[i+1],0]],
				[points[best_path[i],1], points[best_path[i+1],1]],
				c='g', linestyle='-', linewidth=2, marker='o')
		
	ax.plot([points[best_path[0],0], points[best_path[-1],0]],
			[points[best_path[0],1], points[best_path[-1],1]],
			c='g', linestyle='-', linewidth=2, marker='o')
	
	ax.set_xlabel('X Label')
	ax.set_ylabel('Y Label')
	plt.show()
	
# Example usage:
points = np.random.rand(10, 2) # Generate 10 random 3D points
ant_colony_optimization(points, n_ants=10, n_iterations=100, alpha=1, beta=1, evaporation_rate=0.5, Q=1)