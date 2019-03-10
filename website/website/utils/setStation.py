import json

from django.utils import timezone
from datetime import datetime, timedelta
from pprint import pprint
import uuid
import names
from random import randint


sellPoints = []
dropOffs = []
cups = []
users = []


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
            if j < total_stations[i]['cups2']:
                cup = {'model': 'website.Cup',
                       "pk": str(uuid.uuid4()),
                       'fields': {'sellPoint': i}
                       }
            else:
                cup = {'model': 'website.Cup',
                       "pk": str(uuid.uuid4()),
                       'fields': {'dropOff': i}
                       }
            data_out.append(cup)
            list.append(cups, cup)
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
        total_stations[i]['cups2'] = int(0.75*cups*(randint(8, 10)/10))
        cups2 = total_stations[i]['cups2']
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
        sellPoint['fields']['cups_current'] = cups2
        data_out.append(sellPoint)

        list.append(sellPoints, i)

        name = names.get_first_name()
        surname = names.get_last_name()
        username = name.lower() + "." + surname.lower() + "." + str(randint(1, 2019))
        email = username + "@shop.ch"
        user = {'model': 'website.CustomUser',
                'fields': {"username": username, 'role': 1, "first_name": name, "last_name": surname, "email": email, "sellPoint": sellPoint["pk"]}
                }
        data_out.append(user)

        dropOff = {'fields': {}}
        dropOff['pk'] = i
        dropOff['model'] = 'website.DropOff'

        dropOff['fields']['station'] = i
        data_out.append(dropOff)

        list.append(dropOffs, i)

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
                    "pk": k,
                   'fields': {"username": username, 'role': 1, "first_name": name, "last_name": surname, "email": email}
                   }
            data_out.append(user)

            list.append(users, user)

            k += 1

    with open('../../../dataset/data_users.json', 'w') as outfile:
        json.dump(data_out, outfile, sort_keys=False, ensure_ascii=False)


def make_history():
    data_out = []
    current = datetime.now()-timedelta(hours=1)
    shifts = [50, 25, 0, 0, 50, 150, 400, 750, 1500, 650, 575, 675, 850, 525, 425, 575, 675, 425, 325, 275, 225, 200, 150, 75]
    for _ in range(24*7):
        shift = current.hour
        currentshift = randint(int(shifts[shift]/2), shifts[shift])
        for i in range(currentshift):
            cup = cups[randint(0, len(cups) - 1)]
            time1 = (current-timedelta(minutes=randint(0, 60)))
            time1_str = time1.replace(tzinfo=timezone.utc).astimezone(tz=None).strftime("%Y-%m-%d %H:%M:%S")
            dropoff = dropOffs[randint(0, len(dropOffs) - 1)]
            time4 = (time1-timedelta(hours=randint(2, 4), minutes=randint(0, 60)))
            time4_str = time4.replace(tzinfo=timezone.utc).astimezone(tz=None).strftime("%Y-%m-%d %H:%M:%S")
            user = users[randint(0, len(users) - 1)]["pk"]
            time3 = (time4-timedelta(hours=randint(0, 1), minutes=randint(0, 60)))
            time3_str = time3.replace(tzinfo=timezone.utc).astimezone(tz=None).strftime("%Y-%m-%d %H:%M:%S")
            sellpoint = sellPoints[randint(0, len(sellPoints) - 1)]
            time2 = (time3-timedelta(hours=randint(0, 1), minutes=randint(0, 60)))
            time2_str = time2.replace(tzinfo=timezone.utc).astimezone(tz=None).strftime("%Y-%m-%d %H:%M:%S")
            history = {'model': 'website.History',
                       'fields': {"time1": time1_str, "time2": time2_str, "time3": time3_str, "time4": time4_str,
                                  "sellPoint": sellpoint, "dropOff": dropoff, "user": user, "cup": cup["pk"]}}
            cup["sellPoint"] = sellpoint
            data_out.append(history)
        current -= timedelta(hours=1)

    with open('../../../dataset/data_history.json', 'w') as outfile:
        json.dump(data_out, outfile, sort_keys=False, ensure_ascii=False)


def main():
    abstract_traffic()
    print("Traffic abstracted!")
    make_data_results()
    print("Date results done!")
    make_cups()
    print("Cups done!")
    make_users()
    print("Users done!")
    make_history()
    print("History done!")


if __name__ == '__main__':
    main()
