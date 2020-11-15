import sys
import time
from datetime import datetime
import utils
from depot import depot_class
from parcels import parcel_class
from travel import matrix_class

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
	current_time = utils.mytimeprint(current_time, start_time)
	print("\n##################################################################\n")
	print("\t...Loading Travel Matrix...")
	travel = matrix_class(parcels.data)
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