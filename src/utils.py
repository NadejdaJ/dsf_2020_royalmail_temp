import time

def mytime(tstamp):
	return round(time.time() - tstamp, 2)

def mytimeprint(current_time, start_time):
	print('\n\t--- took %s / %s seconds ---' % (mytime(current_time), mytime(start_time)))
	return time.time()

