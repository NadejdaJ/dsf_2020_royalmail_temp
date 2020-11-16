import sys
import time
from datetime import datetime
import utils
from depot import depot_class
from parcels import parcel_class
from travel import matrix_class
from routes import routes_class
from ortools_wrapper import run_or_tools

from viz import init_map, routes_map

def main():

	start_time = time.time()
	start_date = datetime.now()

	print("\n##################################################################\n")
	print("\t...Loading Hub Constraints...")

	depot = depot_class()

	current_time = utils.mytimeprint(start_time, start_time)
	print("\n##################################################################\n")
	print("\t...Loading Delivery Data...")

	parcels = parcel_class()

	init_map(depot, parcels, "delivery_point_locations.html")

	current_time = utils.mytimeprint(current_time, start_time)
	print("\n##################################################################\n")
	print("\t...Loading Travel Matrix...")

	travel = matrix_class(parcels.data)

	current_time = utils.mytimeprint(current_time, start_time)
	print("\n##################################################################\n")
	print("\t...Building Initial Route...")

	init_routes = routes_class(parcels)
	init_routes.init_random_routes(depot, parcels, travel)

	routes_map(depot, parcels, init_routes, "init_routes_random.html")

	init_routes.init_sector_routes(depot, parcels, travel)

	routes_map(depot, parcels, init_routes, "init_routes_sectors.html")

	print("\n##################################################################\n")
	print("\t...Input Routes...\n")
	init_routes.print_route_stats()

	current_time = utils.mytimeprint(current_time, start_time)
	print("\n##################################################################\n")
	print("\t...Running OR-tools solver...")

	or_routes= run_or_tools(depot, parcels, travel, init_routes)

	routes_map(depot, parcels, or_routes, "ortools_routes_solution.html")

	print("\n##################################################################\n")
	print("\t...OR-tools solution...\n")

	or_routes.print_route_stats()

	current_time = utils.mytimeprint(current_time, start_time)

	print("\n##################################################################\n")
	print("\t...Running our own LNS solver...\n")

	# final_route = vrp_solver(init_routes)

	current_time = utils.mytimeprint(current_time, start_time)
	print("\n##################################################################\n")
	end_date = datetime.now()
	print("-----\nVRP engine ran on the %02d-%02d-%4d\n" % (start_date.day, start_date.month, start_date.year))
	print('... started at ' + start_date.strftime("%H:%M:%S"))
	print('... finished at ' + end_date.strftime("%H:%M:%S"))
	print('\ntook %s [h:m:s] \n-----' % str(end_date - start_date).split('.')[0])
	return


if __name__ == '__main__':
	main()
