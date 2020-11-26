import re
import time
from more_itertools import unique_everseen
import routes

def mytime(tstamp):
	return round(time.time() - tstamp, 2)

def mytimeprint(current_time, start_time):
	print('\n\t--- took %s / %s seconds ---' % (mytime(current_time), mytime(start_time)))
	return time.time()

def build_quick_routes(puzzle, input_list):
	# Build class from input list
	input_routes = routes.routes_class(puzzle)
	input_routes.stop_list = input_list[:]
	input_routes.update_vans_from_stop_list(puzzle)

	return input_routes