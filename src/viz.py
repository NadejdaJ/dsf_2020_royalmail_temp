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

def init_map(depot, parcels, map_name):

	fmap = folium.Map(location=[parcels.data.latitude.mean(), parcels.data.longitude.mean()], zoom_start=11)

	for i in parcels.data.postcode:
		POSTCODE = i
		POP = 'Postcode ' + POSTCODE
		LAT = parcels.data.loc[parcels.data.postcode == POSTCODE].latitude.values[0]
		LON = parcels.data.loc[parcels.data.postcode == POSTCODE].longitude.values[0]

		folium.Marker([LAT, LON], popup=POP).add_to(fmap)

	start_time = params.departure_time
	start_time = datetime.strptime(start_time, '%H:%M')
	label = 'Depot -' + ' Postcode: ' + depot.postcode + '-\tTime: ' + str(start_time.time())[:-3]

	folium.Marker([depot.latitude, depot.longitude], popup=label, icon=folium.Icon(color='black')).add_to(fmap)

	map_path = depot.output_path + "/maps"

	if not os.path.exists(map_path):
		os.makedirs(map_path)

	map_filename = map_path + "/" + map_name
	fmap.save(map_filename)

def routes_map(depot, parcels, routes, map_name):

	fmap = folium.Map(location=[parcels.data.latitude.mean(), parcels.data.longitude.mean()], zoom_start=11)

	LAT_DEPOT = depot.latitude
	LON_DEPOT = depot.longitude

	start_time = params.departure_time
	start_time = datetime.strptime(start_time, '%H:%M')

	line0  = '<div style="font-size: 11pt"> -------------------------------'
	line10 = '<div style="font-size: 11pt"> Number of Parcels =  %d </div>' % (routes.total_parcels)
	line11 = '<div style="font-size: 11pt"> Number of Stops   =  %d </div>' % (routes.total_stops)
	line2  = '<div style="font-size: 11pt"> Number of Vans    =  %d </div>' % (routes.num_vans)
	line3  = '<div style="font-size: 11pt"> Total Time        =  %.f [min] </div>' % (routes.total_time)
	line4  = '<div style="font-size: 11pt"> Total Distance    =  %.f [km] </div>' % (routes.total_distance)
	line5  = '<div style="font-size: 11pt"> Estimated Cost    =  %.2f £/parcel</div>' % (routes.return_route_monetary_cost_per_parcel())

	label = line0 + line10 + line11 + line2 + line0 + line3 + line4 + line0 + line5 + line0

	folium.Marker([LAT_DEPOT, LON_DEPOT], icon=DivIcon(icon_size=(250, 250), icon_anchor=(-300, 350), html=label)).add_to(fmap)

	for m in range(routes.num_vans):
		points = [tuple([LAT_DEPOT, LON_DEPOT])]
		for n in range(1, routes.van_num_stops[m] + 1):
			POSTCODE = routes.van_stop_list[m][n]
			DELTAT = timedelta(minutes=int(routes.van_times[m][n]))
			TIME = start_time + DELTAT
			LAT = parcels.data.loc[parcels.data.postcode == POSTCODE].latitude.values[0]
			LON = parcels.data.loc[parcels.data.postcode == POSTCODE].longitude.values[0]
			POP = 'Route #'+str(m + 1) + '\t-\tStop #'+str(n) + '\t-\tPostcode: ' + POSTCODE + '\t-\tTime: ' + str(TIME.strftime('%H:%M'))

			folium.Marker([LAT, LON], popup=POP, icon=folium.Icon(color=coloricons_choices[m % len(coloricons_choices)])).add_to(fmap)
			points.append(tuple([LAT, LON]))

		points.append(tuple([LAT_DEPOT, LON_DEPOT]))

		folium.PolyLine(points, color=colorlines_choices[m % len(colorlines_choices)], weight=2.5, opacity=1).add_to(fmap)

	folium.map.LayerControl(postition='topleft').add_to(fmap)

	POSTCODE = depot.postcode
	label = 'Depot -' + ' Postcode: ' + POSTCODE + '-\tTime: ' + str(start_time.time())[:-3]
	folium.Marker([LAT_DEPOT, LON_DEPOT], popup=label, icon=folium.Icon(color='black')).add_to(fmap)

	map_path = depot.output_path + "/maps"
	map_filename = map_path + "/" + map_name
	fmap.save(map_filename)


