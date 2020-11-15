import sys
import os
import numpy as np
import pandas as pd

import params

from ortools.constraint_solver import pywrapcp
from timeit import default_timer as timer


def make_ortools_path(output_path):
	or_pathname = output_path + "/ortools"
	if not os.path.exists(or_pathname):
		os.makedirs(or_pathname)

def get_time_matrix(travel):
	df = travel.time
	time = np.array(df.values.tolist())
	time_mtx = time * 100  # Or_tools works best to large integers, so multiply every element by 100
	time_mtx = time_mtx.astype(int)
	time_mtx = time_mtx.tolist()
	return time_mtx

def create_data_model(depot, parcels, travel):
	"""Stores the data for the problem."""
	time_mtx = get_time_matrix(travel)
	# in_list, i_route, df, duplicate = get_init_route(hub_table_test, parcels_ics, mtx)
	data = {'time_matrix': time_mtx,
			# 'initialise_routes': i_route,
			'num_vehicles': depot.num_vans, 'depot': 0}

	return data, df


def run_or_tools(depot, parcels, travel):
	start = timer()

	make_ortools_path(depot.output_path)

	# Instantiate the data problem.
	data, postcode_df = create_data_model(depot, parcels, travel)

	# Create the routing index manager.
	manager = pywrapcp.RoutingIndexManager(len(data['time_matrix']),
										   data['num_vehicles'], data['depot'])

	# Create Routing Model.
	routing = pywrapcp.RoutingModel(manager)

