import os
import folium
from folium.features import DivIcon
from datetime import datetime, timedelta
import params

coloricons_choices = [
	'red', 'blue', 'green', 'orange', 'purple', 'pink', 'cadetblue', 'darkred', 'darkblue',
	'darkgreen', 'darkpurple', 'lightred', 'lightblue', 'lightgreen',
	'lightgray', 'gray', 'beige'
]
colorlines_choices = [
	'red', 'blue', 'green', 'orange', 'purple',
	'pink', 'cadetblue', 'darkred', 'darkblue',
	'darkgreen', 'indigo', 'tomato', 'lightblue',
	'lightgreen', 'lightgray', 'gray', 'beige'
]

def init_map(puzzle, map_name):

	fmap = folium.Map(location=[puzzle.data.latitude.mean(), puzzle.data.longitude.mean()], zoom_start=params.zoom_level)

	for i in puzzle.data.postcode:
		POSTCODE = i
		POP = 'Postcode ' + POSTCODE
		LAT = puzzle.data.loc[puzzle.data.postcode == POSTCODE].latitude.values[0]
		LON = puzzle.data.loc[puzzle.data.postcode == POSTCODE].longitude.values[0]

		folium.Marker([LAT, LON], popup=POP).add_to(fmap)

	start_time = params.departure_time
	start_time = datetime.strptime(start_time, '%H:%M')
	label = 'Depot -' + ' Postcode: ' + puzzle.depot_postcode + '-\tTime: ' + str(start_time.time())[:-3]

	folium.Marker([puzzle.depot_latitude, puzzle.depot_longitude], popup=label, icon=folium.Icon(color='black')).add_to(fmap)

	map_path = puzzle.output_path + "/maps"
	if not os.path.exists(map_path):
		os.makedirs(map_path)

	map_filename = map_path + "/" + map_name
	fmap.save(map_filename)

	return fmap


def routes_map(puzzle, routes, map_name):

	fmap = folium.Map(location=[puzzle.data.latitude.mean(), puzzle.data.longitude.mean()], zoom_start=params.zoom_level)

	LAT_DEPOT = puzzle.depot_latitude
	LON_DEPOT = puzzle.depot_longitude

	start_time = params.departure_time
	start_time = datetime.strptime(start_time, '%H:%M')

	line0 = '<div style="font-size: 11pt"> -------------------------------'
	line1 = '<div style="font-size: 11pt"> Number of Vans    =  %d </div>' % (routes.num_vans)
	line2 = '<div style="font-size: 11pt"> Number of Stops   =  %d </div>' % (routes.num_stops)
	line3 = '<div style="font-size: 11pt"> Total Time        =  %.f [min] </div>' % (routes.total_time)
	line4 = '<div style="font-size: 11pt"> Route Evaluation  =  %s </div>'%(routes.evaluate_routes_time())

	label = line0 + line1 + line2 + line0 + line3 + line0 + line4 + line0

	folium.Marker([LAT_DEPOT, LON_DEPOT], icon=DivIcon(icon_size=(250, 250), icon_anchor=(-500, 350), html=label)).add_to(fmap)

	for m in range(routes.num_vans):
		points = [tuple([LAT_DEPOT, LON_DEPOT])]
		for n in range(1, routes.van_num_stops[m] + 1):
			PC_ID = routes.van_stop_list[m][n]
			POSTCODE = puzzle.data.loc[puzzle.data.index == PC_ID].postcode.values[0]
			LAT = puzzle.data.loc[puzzle.data.index == PC_ID].latitude.values[0]
			LON = puzzle.data.loc[puzzle.data.index == PC_ID].longitude.values[0]
			DELTAT = timedelta(minutes=int(routes.van_times[m][n]))
			TIME = start_time + DELTAT
			POP = 'Route #'+str(m + 1) + '\t-\tStop #'+str(n) + '\t-\tPostcode: ' + POSTCODE + '\t-\tTime: ' + str(TIME.strftime('%H:%M'))

			folium.Marker([LAT, LON], popup=POP, icon=folium.Icon(color=coloricons_choices[m % len(coloricons_choices)])).add_to(fmap)
			points.append(tuple([LAT, LON]))

		points.append(tuple([LAT_DEPOT, LON_DEPOT]))

		folium.PolyLine(points, color=colorlines_choices[m % len(colorlines_choices)], weight=2.5, opacity=1).add_to(fmap)

	folium.map.LayerControl(postition='topleft').add_to(fmap)

	POSTCODE = puzzle.depot_postcode
	label = 'Depot -' + ' Postcode: ' + POSTCODE + '-\tTime: ' + str(start_time.time())[:-3]
	folium.Marker([LAT_DEPOT, LON_DEPOT], popup=label, icon=folium.Icon(color='black')).add_to(fmap)

	map_path = puzzle.output_path + "/maps"
	map_filename = map_path + "/" + map_name
	fmap.save(map_filename)

	return fmap


