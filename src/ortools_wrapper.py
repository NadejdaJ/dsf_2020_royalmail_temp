import sys
import os
import numpy as np
import pandas as pd

import params

from ortools.constraint_solver import pywrapcp, routing_enums_pb2
from timeit import default_timer as timer

from routes import routes_class

SEARCHES = {
	'GREEDY_DESCENT': routing_enums_pb2.LocalSearchMetaheuristic.GREEDY_DESCENT,
	'TABU_SEARCH': routing_enums_pb2.LocalSearchMetaheuristic.TABU_SEARCH,
	'GUIDED_LOCAL_SEARCH': routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH,
	'SIMULATED_ANNEALING': routing_enums_pb2.LocalSearchMetaheuristic.SIMULATED_ANNEALING
}

def make_ortools_path(output_path):
	or_pathname = output_path + "/ortools"
	if not os.path.exists(or_pathname):
		os.makedirs(or_pathname)
	return or_pathname

def get_time_matrix(travel):
	df = travel.time
	time = np.array(df.values.tolist())
	time_mtx = time * 100  # Or_tools works best to large integers, so multiply every element by 100
	time_mtx = time_mtx.astype(int)
	time_mtx = time_mtx.tolist()
	return time_mtx

def get_stop_postcodes(depot, parcels):
	df = parcels.data
	h_p = depot.postcode
	df = df[['postcode']]
	df.loc[-1] = [h_p]  # adding a row
	df.index = df.index + 1  # shifting index
	df = df.sort_index()  # sorting by index
	duplicate_stops = df[df['postcode'].duplicated()]['postcode'].tolist()
	# saveList(duplicate_dps, "duplicate_dp.npy")
	df = df.drop_duplicates(['postcode'])
	df = df.reset_index(drop=True)
	return df, duplicate_stops

def create_data_model(depot, parcels, travel, init_routes):
	"""Stores the data for the problem."""
	time_mtx = get_time_matrix(travel)

	in_list = init_routes.stop_list[:]
	no_hub = init_routes.van_stop_list
	no_hub = [x[1:-1] for x in no_hub]
	data_df = parcels.data
	initial_route = [[data_df[data_df['postcode'] == x].index.values[0] for x in xs] for xs in no_hub]
	initial_route = [list(set(tuple(i))) for i in initial_route]

	df, duplicate = get_stop_postcodes(depot, parcels)

	data = {'time_matrix': time_mtx,
			'initialise_routes': initial_route,
			'num_vehicles': depot.num_vans,
			'depot': 0}

	return data, df

def saveList(mylist, filename):
	# the filename should mention the extension 'npy'
	np.save(filename, mylist)

def print_solution(data, manager, routing, solution, postcode_df, iterations, iteration_time, or_pathname):
	total_distance = 0
	or_file_ouput = []
	slacks = 0
	for vehicle_id in range(data['num_vehicles']):
		index = routing.Start(vehicle_id)
		plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
		or_console_output = 'Route for vehicle {}:\n'.format(vehicle_id)
		route_distance = 0
		count = 0
		while not routing.IsEnd(index):
			plan_output += ' {} -> '.format(manager.IndexToNode(index))
			or_console_output += ' {} -> '.format(postcode_df.loc[manager.IndexToNode(index)].values[0])  # Obtain postcode from solver's index

			or_file_ouput.append(postcode_df.loc[manager.IndexToNode(index)].values[0])  # Save Or_tools
			# output to be reconstructed
			previous_index = index
			index = solution.Value(routing.NextVar(index))
			route_distance += routing.GetArcCostForVehicle(
				previous_index, index, vehicle_id)
			count += 1
		plan_output += '{}\n'.format(manager.IndexToNode(index))
		or_console_output += '{}\n'.format(postcode_df.loc[manager.IndexToNode(index)].values[0])
		slack = (count - 1) * 2
		slacks += slack

		plan_output += 'Time of the route: {}mins\n'.format(int(route_distance / 100) + slack)
		# print(plan_output)
		# print(or_console_output)
		total_distance += route_distance

	print("Number of Iterations: {}".format(iterations))
	print("Iterations duration: {} seconds".format(int(iteration_time)))
	print("Time per iteration(sec/iter): {} ".format(iteration_time / iterations))
	print('Time for entire route: {}mins'.format(int(total_distance / 100) + slacks))

	# Save the metrics to be used in constructing the plots
	saveList([iterations, iteration_time, iteration_time / iterations], or_pathname + "/metrics.npy")
	# Save the list that will be used as the constructed route
	saveList(or_file_ouput, or_pathname + "/or_file_output.npy")

	return or_file_ouput


def build_quick_routes(depot, parcels, traffic, input_list):
	# Build class from input list
	input_routes = routes_class(parcels)
	input_routes.stop_list = input_list[:]
	input_routes.remove_adjacent_hub(depot)
	input_routes.fold_list_to_routes(depot)
	input_routes.compute_routes_cost(depot, traffic.time, traffic.dist)
	input_routes.evaluate_parcel_cnt(parcels.parcel_per_stop)

	return input_routes

def run_or_tools(depot, parcels, travel, init_routes):
	start = timer()

	or_pathname = make_ortools_path(depot.output_path)

	# Instantiate the data problem.
	data, postcode_df = create_data_model(depot, parcels, travel, init_routes)

	# Create the routing index manager.
	manager = pywrapcp.RoutingIndexManager(len(data['time_matrix']), data['num_vehicles'], data['depot'])

	# Create Routing Model.
	routing = pywrapcp.RoutingModel(manager)

	# Create and register a transit callback.
	def distance_callback(from_index, to_index):
		"""Returns the distance between the two nodes."""
		# Convert from routing variable Index to distance matrix NodeIndex.
		from_node = manager.IndexToNode(from_index)
		to_node = manager.IndexToNode(to_index)
		return data['time_matrix'][from_node][to_node]

	transit_callback_index = routing.RegisterTransitCallback(distance_callback)

	# Define cost of each arc.
	routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

	# Add Distance constraint.
	dimension_name = 'Time'
	routing.AddDimension(
		transit_callback_index,
		1,  # no slack
		params.max_duty * 10000,  # vehicle maximum travel distance
		True,  # start cumul to zero
		dimension_name)
	distance_dimension = routing.GetDimensionOrDie(dimension_name)
	distance_dimension.SetGlobalSpanCostCoefficient(1)

	# # Set default search parameters.
	# search_parameters = pywrapcp.DefaultRoutingSearchParameters()
	# search_parameters.solution_limit = params.num_ortools_iters
	# search_parameters.local_search_metaheuristic = SEARCHES[params.search_ortools_options]
	# search_parameters.log_search = True
	#
	# routing.CloseModelWithParameters(search_parameters)  # Close the model to allow the search parameter to take effect

	initial_solution = routing.ReadAssignmentFromRoutes(data['initialise_routes'], True)

	# Solve the problem.
	# solution = routing.SolveFromAssignmentWithParameters(initial_solution, search_parameters)
	solution = routing.Solve(initial_solution)

	end = timer()

	duration = end - start
	iterations = params.num_ortools_iters
	iteration_time = duration

	# Print solution on console.
	if solution:
		# print("\n")
		# print("OR-tools Solution after search:")
		# print("\n")
		or_output = print_solution(data, manager, routing, solution, postcode_df, iterations, iteration_time, or_pathname)
		or_routes = build_quick_routes(depot, parcels, travel, or_output)

		return or_routes
	else:
		print("\n OR-Tools was unable to find a solution...\n")
