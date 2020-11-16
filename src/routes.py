import sys
import re
import datetime as dt
import random as rnd
import numpy as np
import itertools
import copy
from math import ceil
import params

def zeros_padding_to_number_digits(mystring):
	"""
	Returns all numbers on 5 digits to let sort the string with numeric order.
	Ex: zeros_padding_to_number_digits("a6b12.125")  ==> "a00006b00012.00125"
	"""
	return ''.join([format(int(x), '05d') if x.isdigit() else x for x in re.split(r'(\d+)', mystring)])

class routes_class(object):

	def __init__(self, puzzle):
		self.num_vans = puzzle.max_vans
		self.max_duty = puzzle.max_duty
		self.total_stops = puzzle.num_stops
		self.total_time = None
		self.stop_list = []

	# -----------------------------------------------------

	# Validity Rule for optimisation
	def valid_routes_time(self):
		if max([item[-1] for item in self.van_times]) > self.max_duty:
			return False
		else:
			return True

	# Validity Rule for optimisation
	def evaluate_routes_time(self):
		max_van_time = max([item[-1] for item in self.van_times])
		if max_van_time > params.max_duty:
			return "Invalid"
		else:
			return "Valid"

	# Validity Rule if needs to keep the Van number constant
	def accept_routes_fixed_fleet_size(self):
		if self.num_vans != params.max_vans:
			return False
		else:
			return True

	def routes_start_at_hub(self, depot_id):
		self.van_id = [(i + 1) for i in range(self.num_vans)]
		self.van_stop_list = [[depot_id] for i in range(self.num_vans)]
		self.van_times = [[0] for i in range(self.num_vans)]
		self.van_num_stops = [0] * self.num_vans

	def routes_append_postcode(self, puzzle, m, n, start, end):
		self.van_stop_list[m].append(end)
		self.van_times[m].append(self.van_times[m][n] + puzzle.time_mtx.loc[start, end] + params.service_time)
		self.van_num_stops[m] += 1

	def routes_end_at_hub(self, puzzle):
		for m in range(self.num_vans):
			n = self.van_num_stops[m]
			start = self.van_stop_list[m][n]
			end = puzzle.depot_id

			self.van_times[m].append(self.van_times[m][n] + puzzle.time_mtx.loc[start, end])
			self.van_stop_list[m].append(end)

	def routes_sumup(self):
		self.total_time = 0
		tot_stops = 0
		for m in range(self.num_vans):
			self.total_time += self.van_times[m][-1]
			tot_stops += self.van_num_stops[m]
		return tot_stops

	# Initial random first set of routes
	def build_at_random(self, puzzle, seed_val=12345):

		self.routes_start_at_hub(puzzle.depot_id)

		stop_list = puzzle.stop_list[:]
		list_left = len(stop_list)

		rnd.seed(seed_val)
		rnd.shuffle(stop_list)

		m = n = 0
		while list_left:

			start = self.van_stop_list[m][n]
			end = stop_list.pop(0)

			self.routes_append_postcode(puzzle, m, n, start, end)

			m = m + 1
			if m == self.num_vans:
				m = 0
				n = n + 1

			list_left -= 1

		self.routes_end_at_hub(puzzle)

		assert self.routes_sumup() == self.total_stops

	# Initial postcode-sector split set of routes
	def build_from_postcodes(self, puzzle):

		print("\n Initialisation of Routes from Sorted Postcodes...")

		self.routes_start_at_hub(puzzle.depot_id)

		avg_deliveries_per_van = int(ceil(self.total_stops / self.num_vans))

		stop_list = puzzle.data.postcode.str.replace(" ","").apply\
			(lambda x: zeros_padding_to_number_digits(x)).sort_values().index.tolist()
		list_left = len(stop_list)

		m = n = 0
		while list_left:
			start = self.van_stop_list[m][n]
			end = stop_list.pop(0)

			self.routes_append_postcode(puzzle, m, n, start, end)

			n += 1
			if n == avg_deliveries_per_van:
				n = 0
				m += 1

			list_left -= 1

		self.routes_end_at_hub(puzzle)

		assert self.routes_sumup() == self.total_stops

	def print_route_stats(self):
		print("\t---------")
		print('\tNumber of Vans    =', self.num_vans)
		print('\tNumber of Stops   =', self.total_stops)
		print("\t---------")
		for m in range(self.num_vans):
			print('\t\tVan', self.van_id[m],
				  '\t Stops =', "%2d" % self.van_num_stops[m],
				  '\t Time =', "%3.f" % self.van_times[m][-1], '[min]')
		print("\t---------")
		print('\tCumulative Time      =', "%3.f" % self.total_time, '[min]')
		print("\t---------")
		print("\tRoute Evaluation: ", self.evaluate_routes_time())
		print("\t---------")

