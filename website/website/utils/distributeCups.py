from website import models
import math


def filltocapacity():
	global estate
	stations = models.Station.objects.all()

	for station in stations:
		sellPoint = models.SellPoint.objects.filter(station=station.name)
		dropOff = models.DropOff.objects.filter(station=station.name)

		current = sellPoint.cups_current
		desired = sellPoint.cups_desired

		for dropOff_ind in dropOff:
			cups = models.Cup.objects.filter(dropOff=dropOff_ind)
			qtty = cups.count()

			lat = station.lat
			lon = station.lon

			if current < desired:

				if current+qtty > desired:  # If we only use the exact number of cups to have the desired number of cups
					models.Moviment.create(origin=dropOff, destination=sellPoint, quantity=desired-current)
					# cups that can be used to distribute to other stations
					estate[station.name] = (sellPoint, dropOff, current+qtty-desired, lat, lon)
				else:  # If we have the exact amount or less
					models.Moviment.create(origin=dropOff, destination=sellPoint, quantity=current+qtty)
					estate[station.name] = (sellPoint, dropOff, current+qtty-desired, lat, lon)

			else:  # If we have excess of cups in the dropOff, we could use it to distribute to other stations
				estate[station.name] = (sellPoint, dropOff, cups, lat, lon)

			if current+qtty-desired == 0:
				del estate[station.name]


def searchofcups():
	global estate

	for key in estate:

		if estate[key][3] < 0: # It means that the sellPoint needs more cups to have the desired amount
			min = math.inf
			station = key

			for key2 in estate:
				dist = int(math.sqrt((estate[key][4]-estate[key2][4]) ^ 2 + (estate[key][5]-estate[key2][5]) ^ 2))

				if key2 != key and estate[key][3] > 0 and dist < min:
					min = dist
					station = key2

			if key != station:
				qtty = estate[station][3]
				current = estate[key][1].cups_current
				desired = estate[key][1].cups_desired

				dropOff = estate[station][2]
				sellPoint = estate[key][1]

				if current + qtty > desired:  # If we only use the exact number of cups to have the desired number
					models.Moviment.create(origin=dropOff, destination=sellPoint, quantity=desired - current)

					# Delete the station that is at the desired quantity of cups
					del estate[key]

					sellPoint = estate[station][1]
					lat = estate[station][4]
					lon = estate[station][5]

					# We have to delete it because we can't modify tuples
					del estate[station]

					# cups that can be used to distribute to other stations
					estate[station] = (sellPoint, dropOff, current + qtty - desired, lat, lon)

				else:  # If we have the exact amount or less

					models.Moviment.create(origin=dropOff, destination=sellPoint, quantity=qtty)
					del estate[station]

					if current + qtty - desired == 0:
						del estate[key]
					else:
						estate[key] = (sellPoint, dropOff, current + qtty - desired, lat, lon)


def distribute():
	filltocapacity()
	searchofcups()

