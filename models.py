from utils import *

class Coordinate:
	def __init__(self, id, name, latitude, longitude):
		self.id = id
		self.name = name
		self.latitude = latitude
		self.longitude = longitude

class Customer(Coordinate):
	def __init__(self, id, name, latitude, longitude, demand):
		super().__init__(id, name, latitude, longitude)
		self.demand = demand

class Vehicle:
	def __init__(self, name, capacity, cost):
		self.name = name
		self.capacity = capacity
		self.cost = cost

class Route:
	def __init__(self, vehicle):
		self.length = 0
		self.stops = []
		self.vehicle = vehicle
		self.remaining = vehicle.capacity

	def visit(self, coordinate):
		if len(self.stops) > 0:
			self.length += distance(self.stops[-1], coordinate)
		if isinstance(coordinate, Customer):
			self.remaining -= coordinate.demand
		self.stops.append(coordinate)

class Path:
	def __init__(self):
		self.routes = []
		self.length = 0

	def add(self, route):
		self.routes.append(route)
		self.length += route.length

	def full_path_without_depot(self):
		full_path_without_depot = []
		for route in self.routes:
			for coordinate in route.stops:
				if coordinate.id != -1:
					full_path_without_depot.append(coordinate.id)
		return full_path_without_depot
