import sys
import time
from datetime import datetime
import utils
from puzzle import puzzle_class
from routes import routes_class
from ortools_solver import run_or_tools
from vrp_solver import run_vrp_solver

from viz import init_map, routes_map

def main():

    start_time = time.time()
    start_date = datetime.now()

    print("\n##################################################################\n")
    print("\t...Loading Dataset...")

    puzzle = puzzle_class()

    init_map(puzzle, "delivery_point_locations.html")

    current_time = utils.mytimeprint(start_time, start_time)

    print("\n##################################################################\n")
    print("\t...Building Initial Routes...")

    init_routes = routes_class(puzzle)
    init_routes.build_from_postcodes(puzzle)
    # init_routes.build_at_random(puzzle)
    routes_map(puzzle, init_routes, "init_routes_postcodes.html")

    print("\n\t...Inital Solution...\n")
    init_routes.print_route_stats()

    current_time = utils.mytimeprint(current_time, start_time)

    # print("\n##################################################################\n")
    # print("\t...Running OR-tools solver...\n")
    # or_routes= run_or_tools(puzzle, init_routes)
	#
    # routes_map(puzzle, or_routes, "ortools_routes_solution.html")
	#
    # print("\n##################################################################\n")
    # print("\t...OR-tools solution...\n")
	#
    # or_routes.print_route_stats()
	#
    # current_time = utils.mytimeprint(current_time, start_time)
	#
    print("\n##################################################################\n")
    print("\t...Running our own LNS solver...\n")

    final_route, record_perf_df = run_vrp_solver(puzzle, init_routes)
    routes_map(puzzle, final_route, "final_routes_postcodes.html")

    current_time = utils.mytimeprint(current_time, start_time)

    print("\n##################################################################\n")

    print("\n\t...Optimised Solution...\n")
    final_route.print_route_stats()

    print("\n##################################################################\n")
    end_date = datetime.now()
    print("-----\nVRP engine ran on the %02d-%02d-%4d\n" % (start_date.day, start_date.month, start_date.year))
    print('... started at ' + start_date.strftime("%H:%M:%S"))
    print('... finished at ' + end_date.strftime("%H:%M:%S"))
    print('\ntook %s [h:m:s] \n-----' % str(end_date - start_date).split('.')[0])

    return final_route, record_perf_df


if __name__ == '__main__':
    main()
