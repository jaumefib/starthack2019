import json
from pprint import pprint
import uuid
import names
from random import randint


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
                if travelers * reduction < 10:
                    res['name'] = str(station)
                    res['cups'] = min_cups
                else:
                    res['name'] = str(station)
                    res['cups'] = int(travelers * reduction)

                last_travelers = travelers
            else:
                if last_travelers * reduction < 10:
                    res['name'] = str(station)
                    res['cups'] = min_cups
                else:
                    res['name'] = str(station)
                    res['cups'] = int(travelers * reduction)
            res['lat'] = lat
            res['lon'] = lon
            # print(lat, lon)
            total_stations.append(res)

        # print(total_stations)


def make_cups():
    data_out = []
    k = 0
    for i, station in enumerate(total_stations):
        total_cups = total_stations[i]['cups']
        for j in range(total_cups):
            cup = {'model': 'website.Cup',
                   'fields': {'sellPoint': i}
                   }
            data_out.append(cup)
            k += 1

    with open('../../../dataset/data_cups.json', 'w') as outfile:
        json.dump(data_out, outfile, sort_keys=False, ensure_ascii=False)


def make_data_results():
    data_out = []

    company = {'fields': {}}
    company['pk'] = 0
    company['model'] = 'website.Company'

    company['fields']['name'] = 'company0'

    data_out.append(company)

    for i in range(0, len(total_stations)):
        station = {'fields': {}}
        station['pk'] = i
        station['model'] = 'website.Station'

        station['fields']['name'] = total_stations[i]['name']
        station['fields']['lat'] = total_stations[i]['lat']
        station['fields']['lon'] = total_stations[i]['lon']

        cups = total_stations[i]['cups']
        if cups >= 693:
            imp = 5
        elif cups >= 40:
            imp = 4
        elif cups >= 20:
            imp = 3
        elif cups >= 10:
            imp = 2
        else:
            imp = 1
        station['fields']['importance'] = imp

        data_out.append(station)

        sellPoint = {'fields': {}}
        sellPoint['pk'] = i
        sellPoint['model'] = 'website.SellPoint'

        name = 'sellpoint' + str(i)
        sellPoint['fields']['name'] = name
        sellPoint['fields']['company'] = 0
        sellPoint['fields']['station'] = i
        sellPoint['fields']['cups_desired'] = cups
        sellPoint['fields']['cups_current'] = cups
        data_out.append(sellPoint)

        dropOff = {'fields': {}}
        dropOff['pk'] = i
        dropOff['model'] = 'website.DropOff'

        dropOff['fields']['station'] = i
        data_out.append(dropOff)

    with open('../../../dataset/data_results.json', 'w') as outfile:
        json.dump(data_out, outfile, sort_keys=False, ensure_ascii=False)


def make_users():
    data_out = []
    k = 0
    for i, station in enumerate(total_stations):
        total_cups = total_stations[i]['cups']
        for j in range(int(0.1*(total_cups))):
            name = names.get_first_name()
            surname = names.get_last_name()
            username = name.lower() + "." + surname.lower() + "." + str(randint(1, 2019))
            email = username + "@sbb.ch"
            user = {'model': 'website.CustomUser',
                   'fields': {"username": username, 'role': 1, "name": name, "surname": surname, "email": email}
                   }
            data_out.append(user)
            k += 1

    with open('../../../dataset/data_users.json', 'w') as outfile:
        json.dump(data_out, outfile, sort_keys=False, ensure_ascii=False)



def Main():
    abstract_traffic()
    make_data_results()
    make_cups()
    make_users()


if __name__ == '__main__':
    Main()
