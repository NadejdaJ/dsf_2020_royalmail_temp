import sys
import datetime as dt
import random as rnd
import numpy as np
import itertools
import copy
import params

from utils import ordered_van_sectors, alphaNumOrder

class routes_class(object):

	def __init__(self, parcels):
		self.num_vans = params.max_vans
		self.max_duty = params.max_duty
		self.total_parcels = parcels.num_parcels
		self.total_stops = parcels.num_stops
		self.total_time = None
		self.total_distance = None
		self.opexcost = None
		self.stop_list = []

	# remove consecutive hubs and ending hubs in stop_array
	def remove_adjacent_hub(self, depot):
		stop_array = np.array(self.stop_list)
		stop_roll = np.roll(stop_array, -1)
		myfilter = np.where(~((stop_array == stop_roll) & (stop_array == depot.postcode)))
		self.stop_list = list(stop_array[myfilter])

	# -----------------------------------------------------
	# Pack list to routes
	def fold_list_to_routes(self, depot):

		# Number of separate vans
		self.num_vans = self.stop_list.count(depot.postcode)
		self.van_id = [(i + 1) for i in range(self.num_vans)]
		self.van_stop_list = [[] for i in range(self.num_vans)]

		stop_cnt = 0
		route_cnt = 0

		self.van_stop_list[route_cnt].append(depot.postcode)

		for idx, stop in enumerate(self.stop_list[1:]):
			stop_cnt += 1
			self.van_stop_list[route_cnt].append(stop)

			if stop == depot.postcode:
				route_cnt += 1
				self.van_stop_list[route_cnt].append(stop)

		self.van_stop_list[route_cnt].append(depot.postcode)
		assert (route_cnt + 1) == self.num_vans
		return self.van_stop_list

	# -----------------------------------------------------
	# Unfold routes to list
	def unfold_routes_to_list(self):
		self.stop_list = [stops for subroute in self.van_stop_list for stops in subroute[:-1]]
		return self.stop_list

	# -----------------------------------------------------
	# Evaluate routes cost
	def compute_routes_cost(self, hub_table, matrix_time, matrix_dist):
		# -----------------------------------------------------
		# Initialisation of vans variables ...
		self.van_times = [[0] for i in range(self.num_vans)]
		self.van_distances = [[0] for i in range(self.num_vans)]
		self.van_num_stops = [len(subroute) - 2 for subroute in self.van_stop_list]
		# -----------------------------------------------------
		# Adding time & distance to go to each drop, one van at a time...
		for i in range(self.num_vans):
			for j in range(self.van_num_stops[i]):
				start = self.van_stop_list[i][j]
				end = self.van_stop_list[i][j + 1]
				self.van_times[i].append(
					self.van_times[i][j] + matrix_time.loc[start, end] + params.service_time)
				self.van_distances[i].append(self.van_distances[i][j] + matrix_dist.loc[start, end])

		# Adding time & distance to go back to hub...
		for m in range(self.num_vans):
			n = self.van_num_stops[m]
			start = self.van_stop_list[m][n]
			end = hub_table.postcode
			self.van_times[m].append(self.van_times[m][n] + matrix_time.loc[start, end])
			self.van_distances[m].append(self.van_distances[m][n] + matrix_dist.loc[start, end])
		# -----------------------------------------------------
		tot_stops = self.routes_sumup()
		# -----------------------------------------------------
		# print(tot_stops, self.total_stops, sum(self.van_num_stops))
		# -----------------------------------------------------
		assert tot_stops == self.total_stops
		# -----------------------------------------------------
		self.compute_opexcost()
		# -----------------------------------------------------

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

	# Operational cost function, used in the simulated annealing, convergence criteria
	def compute_opexcost(self):
		self.opexcost  = params.pounds_per_min * self.total_time
		self.opexcost += params.pounds_per_km * self.total_distance

	# Parcel evaluation per van
	def evaluate_parcel_cnt(self, parcel_per_stop):
		self.van_num_parcels = [0] * self.num_vans
		for i, van in enumerate(self.van_stop_list):
			for j, stop in enumerate(van[1:-1]):
				self.van_num_parcels[i] += parcel_per_stop[stop]

	# Validity Rule if needs to keep the Van number constant
	def accept_routes_fixed_van_num(self):
		if self.num_vans != params.max_vans:
			return False
		else:
			return True

	def routes_start_at_hub(self, depot):
		self.van_id = [(i + 1) for i in range(self.num_vans)]
		self.van_stop_list = [[depot.postcode] for i in range(self.num_vans)]
		self.van_times = [[0] for i in range(self.num_vans)]
		self.van_distances = [[0] for i in range(self.num_vans)]
		self.van_num_stops = [0] * self.num_vans
		self.van_num_parcels = [0] * self.num_vans

	def routes_append_postcode(self, parcels, travel, m, n, start, end):
		self.van_stop_list[m].append(end)
		self.van_times[m].append(self.van_times[m][n] + travel.time.loc[start, end] + params.service_time)
		self.van_distances[m].append(self.van_distances[m][n] + travel.dist.loc[start, end])
		self.van_num_stops[m] += 1
		self.van_num_parcels[m] += parcels.parcel_per_stop[end]

	def routes_end_at_hub(self, depot, travel):
		for m in range(self.num_vans):
			n = self.van_num_stops[m]
			start = self.van_stop_list[m][n]
			end = depot.postcode

			self.van_times[m].append(self.van_times[m][n] + travel.time.loc[start, end])
			self.van_distances[m].append(self.van_distances[m][n] + travel.dist.loc[start, end])
			self.van_stop_list[m].append(end)

	def routes_sumup(self):
		self.total_time = 0
		self.total_distance = 0
		tot_stops = 0
		for m in range(self.num_vans):
			self.total_time += self.van_times[m][-1]
			self.total_distance += self.van_distances[m][-1]
			tot_stops += self.van_num_stops[m]
		return tot_stops

	# Initial random first set of routes
	def init_random_routes(self, depot, parcels, travel, seed_val=12345):

		print("\n Initialisation of Random Routes...")

		self.routes_start_at_hub(depot)

		stop_list = parcels.stop_list[:]
		list_left = len(stop_list)

		rnd.seed(seed_val)
		rnd.shuffle(stop_list)

		m = n = 0
		while list_left:

			start = self.van_stop_list[m][n]
			end = stop_list.pop(0)

			self.routes_append_postcode(parcels, travel, m, n, start, end)

			m = m + 1
			if m == self.num_vans:
				m = 0
				n = n + 1

			list_left -= 1

		self.routes_end_at_hub(depot, travel)

		tot_stops = self.routes_sumup()
		assert tot_stops == self.total_stops

		self.compute_opexcost()

		return self

	# Initial postcode-sector split set of routes
	def init_sector_routes(self, depot, parcels, travel):

		print("\n Initialisation of Routes from Postcode Sectors...")

		self.routes_start_at_hub(depot)

		stop_list = sorted(parcels.stop_list, key=alphaNumOrder)

		vans_sectors = ordered_van_sectors(depot, parcels)

		van_stops_count = [0] * self.num_vans

		while stop_list:
			end = stop_list.pop(0)

			m = [idx for idx, sects in enumerate(vans_sectors) if end[:-2] in sects][0]
			n = self.van_num_stops[m]
			start = self.van_stop_list[m][n]

			self.van_stop_list[m].append(end)

			self.van_times[m].append(self.van_times[m][n] + travel.time.loc[start, end] + params.service_time)
			self.van_distances[m].append(self.van_distances[m][n] + travel.dist.loc[start, end])
			self.van_num_stops[m] += 1
			self.van_num_parcels[m] += parcels.parcel_per_stop[end]

			van_stops_count[m] += 1

		self.routes_end_at_hub(depot, travel)

		tot_stops = self.routes_sumup()
		assert tot_stops == self.total_stops

		self.compute_opexcost()

		return self

	def return_route_monetary_cost_per_parcel(self):
		return self.opexcost / self.total_parcels

	def print_route_stats(self):

		print("\t---------")
		print('\tNumber of Vans    =', self.num_vans)
		print('\tNumber of Parcels =', self.total_parcels)
		print('\tNumber of Stops   =', self.total_stops)
		print("\t---------")

		for m in range(self.num_vans):
			print('\t\tVan', self.van_id[m],
				  '\t Stops =', "%2d" % self.van_num_stops[m],
				  '\t Parcels =', "%2d" % self.van_num_parcels[m],
				  '\t Time =', "%3.f" % self.van_times[m][-1], '[min]',
				  '\t Distance =', "%3.f" % self.van_distances[m][-1], '[km]')

		print("\t---------")
		print('\tCumulative Time      =', "%3.f" % self.total_time, '[min]')
		print('\tCumulative Distance  =', "%3.f" % self.total_distance, '[km]')
		print("\t---------")
		print("\tCost per Parcel      = £%.2f" % self.return_route_monetary_cost_per_parcel())
		print("\t---------")
		print("\tRoute Evaluation: ", self.evaluate_routes_time())
		print("\t---------")

