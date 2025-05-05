# https://www.wikidata.org/wiki/Wikidata:SPARQL_tutorial/en
# https://github.com/OSMNames/OSMNames, http://github.com/OSMNames/OSMNames/issues/208
# https://osmnames.org/download/

import sys
import json
import urllib.parse
import urllib.request

wikidata_url = 'https://query.wikidata.org/#'
wikidata_url_api = 'https://query.wikidata.org/sparql'

sparql = '''
SELECT DISTINCT ?city ?cityLabel ?countryLabel ?iso ?population ?gps
WHERE {
    ?city wdt:P31/wdt:P279* wd:Q515 .
    ?city wdt:P17 ?country .
    ?city wdt:P1082 ?population .
    ?city wdt:P625 ?gps .
    ?country wdt:P297 ?iso .
    
    FILTER (?population > 100000) .
    
    SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
ORDER BY DESC(?population)
LIMIT 5000
'''.strip()

print(wikidata_url + urllib.parse.quote(sparql), end = '\n\n', file = sys.stderr)

resultset = json.loads(urllib.request.urlopen(wikidata_url_api + '?' + urllib.parse.urlencode(dict(format = 'json', query = sparql))).read().decode('utf-8'))

# city, country, lon, lat
data = [[v['cityLabel']['value'], v['countryLabel']['value']] + v['gps']['value'].replace('Point', '').strip('()').split()[::-1] for v in resultset['results']['bindings']]

# lat,lon
print(json.dumps({row[0] : ','.join(row[-2:]) for row in data}, indent = 2, sort_keys = True, ensure_ascii = False))
