#import csv
import json

if __name__ == '__main__':
	with open('passagierfrequenz.json') as json_data:
		d = json.load(json_data)
		res = {}
		anteriors_passatgers = 500
		for row in d:
			try:
				estacio = row['fields']['bahnhof_haltestelle']
				passatgers = row['fields']['dtv']
			except KeyError:  # includes simplejson.decoder.JSONDecodeError
				passatgers = -1
			if passatgers != -1:
				res[str(estacio)] = passatgers
				anteriors_passatgers = passatgers
			else:
				res[str(estacio)] = anteriors_passatgers

		print(res)
	with open('result.json', 'w') as outfile:
		json.dump(res, outfile, ensure_ascii=False)
