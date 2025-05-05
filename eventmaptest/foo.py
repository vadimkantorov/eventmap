import json
import csv

c = json.load(open('_data/citygeocoder.json'))

w = csv.writer(open('test.tsv', 'w'), delimiter = '\t')
w.writerow(['city', 'latlon'])
for k, v in c.items():
    w.writerow([k, v])
