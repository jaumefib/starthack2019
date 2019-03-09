import json
from pprint import pprint
import uuid

def make_data_stations():

     with open('haltestelle-dataset-with-services.json') as f:
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
        json.dump(data_stations, outfile)


def Main():

    make_data_stations()




if __name__ == '__main__':
    Main()