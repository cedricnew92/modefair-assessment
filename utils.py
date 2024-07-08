import math

def distance(c1, c2):
	return 100 * math.sqrt(math.pow((c2.longitude - c1.longitude), 2) + math.pow((c2.latitude - c1.latitude), 2))