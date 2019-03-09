import json
from pprint import pprint
import uuid


def abstract_traffic():
    with open('../../../dataset/passagierfrequenz.json') as json_data:
        d = json.load(json_data)
        global total_stations
        total_stations = []

        reduction = 0.01
        last_travelers = 200
        min_cups = 20
        for row in d:
            res = {}
            try:
                station = row['fields']['bahnhof_haltestelle']
                travelers = row['fields']['dtv']
                [lat, lon] = row['fields']['geopos']

            except KeyError:  # includes simplejson.decoder.JSONDecodeError
                travelers = -1
            if travelers != -1:
                if travelers*reduction < 10:
                    res['name'] = str(station)
                    res['cups'] = min_cups
                else:
                    res['name'] = str(station)
                    res['cups'] = int(travelers*reduction)

                last_travelers = travelers
            else:
                if last_travelers*reduction < 10:
                    res['name'] = str(station)
                    res['cups'] = min_cups
                else:
                    res['name'] = str(station)
                    res['cups'] = int(travelers*reduction)
            res['lat'] = lat
            res['lon'] = lon
            #print(lat, lon)
            total_stations.append(res)

        #print(total_stations)

def make_data_results():

    data_out = []

    company = {'fields': {}}
    company['pk'] = 0
    company['model'] = 'website.Company'

    company['fields']['name'] = 'company0'

    data_out.append(company)

    for i in range(0, 4):
        station = {'fields': {}}
        station['pk'] = i
        station['model'] = 'website.Station'

        station['fields']['name'] = total_stations[i]['name']
        station['fields']['lat'] = total_stations[i]['lat']
        station['fields']['lon'] = total_stations[i]['lon']
        station['fields']['importance'] = 0
        data_out.append(station)


        sellPoint = {'fields': {}}
        sellPoint['pk'] = i
        sellPoint['model'] = 'website.SellPoint'

        name = 'sellpoint' + str(i)
        sellPoint['fields']['name'] = name
        sellPoint['fields']['company'] = 0
        sellPoint['fields']['station'] = i
        data_out.append(sellPoint)

        dropOff = {'fields': {}}
        dropOff['pk'] = i
        dropOff['model'] = 'website.DropOff'

        dropOff['fields']['station'] = i
        data_out.append(dropOff)


    with open('../../../dataset/data_results.json', 'w') as outfile:
        json.dump(data_out, outfile, ensure_ascii=False)

def Main():

    abstract_traffic()

    make_data_results()

if __name__ == '__main__':
    Main()