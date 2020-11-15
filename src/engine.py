import sys
import time
import utils
from depot import depot_class
from parcels import parcel_class
from travel import matrix_class

def main():

	start_time = time.time()

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
	return


if __name__ == '__main__':
	main()