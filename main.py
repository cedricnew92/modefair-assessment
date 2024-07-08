import numpy as np
from models import *
from utils import *

def ant_colony_optimization(customers, vehicles, depot, n_ants, n_iterations, alpha, beta, evaporation_rate, Q):
	n_customers = len(customers)
	pheromone = np.ones((n_customers, n_customers)) # initialize pheromone
	n_vehicles = len(vehicles)

	best_path = None
	best_path_length = np.inf
	
	for iteration in range(n_iterations):
		paths = []
		path_lengths = []
		
		for ant in range(n_ants):
			# initialize of ant path searching work
			path = Path()
			current_vehicle = np.random.randint(n_vehicles) # randomly select vehicle
			route = Route(vehicles[current_vehicle])
			route.visit(depot) # start at depot
			visited = [False] * n_customers
			current_customer = np.random.randint(n_customers) # randomly select customer
			visited[current_customer] = True
			route.visit(customers[current_customer]) # and travel to selected customer
			
			# movement probabilities calculation and visit
			while False in visited:
				unvisited = np.where(np.logical_not(visited))[0]
				probabilities = np.zeros(len(unvisited))
				
				for i, unvisited_customer in enumerate(unvisited):
					pheromone_level = pheromone[current_customer, unvisited_customer]
					from_customer = customers[current_customer]
					to_customer = customers[unvisited_customer]
					if route.remaining < to_customer.demand:
						continue
					heuristic_information = distance(from_customer, to_customer)
					probabilities[i] = pheromone_level**alpha / heuristic_information**beta
				
				# move to next customer with calculated probabilities
				if np.sum(probabilities) > 0:
					probabilities /= np.sum(probabilities)
					next_customer = np.random.choice(unvisited, p=probabilities)
					route.visit(customers[next_customer]) # travel to next customer
					visited[next_customer] = True
					current_customer = next_customer
				else:
					route.visit(depot) # back to depot
					path.add(route)
					current_vehicle = np.random.randint(n_vehicles)
					route = Route(vehicles[current_vehicle])
					route.visit(depot) # start at depot again

			route.visit(depot) # end at depot
			path.add(route)
			path_lengths.append(path.length)
			paths.append(path.full_path_without_depot())

			if path.length < best_path_length:
				best_path = path
				best_path_length = path.length
		
		# update pheromone to share with other ants
		pheromone *= evaporation_rate

		for path, path_length in zip(paths, path_lengths):
			for i in range(n_customers-1):
				pheromone[path[i], path[i+1]] += Q/path_length
			pheromone[path[-1], path[0]] += Q/path_length

	return (best_path, best_path_length)

if __name__ == "__main__":

	depot = Coordinate(-1, 'Depot', 4.4184, 114.0932)
	customers = [
		Customer(0, 'Customer 1', 4.3555, 113.9777, 5),
		Customer(1, 'Customer 2', 4.3976, 114.0049, 8),
		Customer(2, 'Customer 3', 4.3163, 114.0764, 3),
		Customer(3, 'Customer 4', 4.3184, 113.9932, 6),
		Customer(4, 'Customer 5', 4.4024, 113.9896, 5),
		Customer(5, 'Customer 6', 4.4142, 114.0127, 8),
		Customer(6, 'Customer 7', 4.4804, 114.0734, 3),
		Customer(7, 'Customer 8', 4.3818, 114.2034, 6),
		Customer(8, 'Customer 9', 4.4935, 114.1828, 5),
		Customer(9, 'Customer 10', 4.4932, 114.1322, 8)
	]
	vehicles = [
		Vehicle('A', 25, 1.2),
		Vehicle('B', 30, 1.5)
	]
	path, length = ant_colony_optimization(
		customers, 
		vehicles, 
		depot, 
		n_ants=50, 
		n_iterations=100, 
		alpha=1, 
		beta=1, 
		evaporation_rate=0.5, 
		Q=1
	)

	total_distance = length
	total_cost = 0

	detail = ""
	for route in path.routes:
		vehicle = route.vehicle
		distance = route.length
		cost = vehicle.cost * distance
		total_cost += cost
		demand = vehicle.capacity - route.remaining
		detail += ("Vehicle (%s):\n" % (vehicle.name))
		detail += ("Round Trip Distance: %s km, Cost: RM %s, Demand: %s\n" % (distance, cost, demand))
		for stop in route.stops:
			detail += "%s -> " % stop.name
		detail = detail[:-4]
		detail += "\n\n"

	print("%-*s : %-*s km" % (15, "Total Distance", 15, total_distance))
	print("%-*s : RM %-*s" % (15, "Total Cost", 15, total_cost))
	print("\n")
	print(detail)

