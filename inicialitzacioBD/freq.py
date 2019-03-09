#import csv
import json

if __name__ == '__main__':
	with open('passagierfrequenz.json') as json_data:
		d = json.load(json_data)
		res = {}
		reduction = 0.25
		last_travelers = 200
		for row in d:
			try:
				station = row['fields']['bahnhof_haltestelle']
				travelers = row['fields']['dtv']
			except KeyError:  # includes simplejson.decoder.JSONDecodeError
				travelers = -1
			if travelers != -1:
				res[str(station)] = int(travelers*reduction)
				last_travelers = travelers
			else:
				res[str(station)] = int(last_travelers)

		print(res)
	with open('result.json', 'w') as outfile:
		json.dump(res, outfile, ensure_ascii=False)
