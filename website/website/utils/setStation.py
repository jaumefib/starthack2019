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
                    res[str(station)] = min_cups
                else:
                    res[str(station)] = int(travelers*reduction)

                last_travelers = travelers
            else:
                if last_travelers*reduction < 10:
                    res[str(station)] = min_cups
                else:
                    res[str(station)] = int(last_travelers*reduction)
            res['lat'] = lat
            res['lon'] = lon
            #print(lat, lon)
            total_stations.append(res)

        print(len(total_stations))



def make_data_stations():

     with open('../../../dataset/haltestelle-dataset-with-services.json') as f:
        data_stations_import = json.load(f)

     global data_stations
     data_stations = {"stations": []}

     subdata = {}
     station = data_stations_import[0]['fields']['stationsbezeichnung']
     subdata['name'] = station
     subdata['id'] = uuid.uuid3(uuid.NAMESPACE_DNS, str(0))
     data_stations['stations'].append(subdata)

     for i in range(1, len(data_stations_import)):
        subdata = {}
        station = data_stations_import[i]['fields']['stationsbezeichnung']
        #lon =
        #lat =
        for j in range(0, len(data_stations['stations'])):

            if not station in data_stations['stations'][j].values():
                #print('hello')
                subdata['name'] = station
                subdata['id'] = uuid.uuid3(uuid.NAMESPACE_DNS, str(key))
                data_stations['stations'].append(subdata)


     #json_data = json.dumps(data_stations)
     #pprint(json_data['stations'][0])


     with open('data_out.json', 'w') as outfile:
        json.dump(data_stations, outfile, ensure_ascii=False)


def Main():

    abstract_traffic()

    #make_data_results()

if __name__ == '__main__':
    Main()