import re
import time
from more_itertools import unique_everseen

def mytime(tstamp):
	return round(time.time() - tstamp, 2)

def mytimeprint(current_time, start_time):
	print('\n\t--- took %s / %s seconds ---' % (mytime(current_time), mytime(start_time)))
	return time.time()

def ordered_van_sectors(depot, parcels):

	sectors_list = get_sectors_alpha_ordered(parcels)

	return split_even_sectors_per_van(depot.num_vans, sectors_list)

def get_sectors_alpha_ordered(parcels):
	
	stop_sorted = sorted(parcels.stop_list, key=alphaNumOrder)

	return list(unique_everseen([x[:-2] for x in stop_sorted]))

def alphaNumOrder(mystring):
	"""
	Returns all numbers on 5 digits to let sort the string with numeric order.
	Ex: alphaNumOrder("a6b12.125")  ==> "a00006b00012.00125"
	"""
	return ''.join([format(int(x), '05d') if x.isdigit() else x for x in re.split(r'(\d+)', mystring)])

def split_even_sectors_per_van(num_vans, ordered_sectors):

	sectors_per_van = int(len(ordered_sectors) / num_vans)
	remaining_sectors = int(len(ordered_sectors) % num_vans)

	num_sectors = 0
	van_count = 0
	new_sector_list = []
	vans_sectors = []

	for sector in ordered_sectors:
		if van_count < remaining_sectors:
			vans_sector_num = sectors_per_van + 1
		else:
			vans_sector_num = sectors_per_van
			
		if num_sectors < vans_sector_num:
			new_sector_list.append(sector)
			num_sectors += 1
		else:
			vans_sectors.append(new_sector_list)
			van_count += 1
			new_sector_list = [sector]
			num_sectors = 1
	# -----------------------------------------------------
	vans_sectors.append(new_sector_list)
	# -----------------------------------------------------
	return vans_sectors

