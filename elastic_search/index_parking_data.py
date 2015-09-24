from elasticsearch import Elasticsearch
from elasticsearch import helpers
import json, os

# connect to the elasticsearch instance
es = Elasticsearch("http://ec2-52-3-61-194.compute-1.amazonaws.com:9200")

# create index and mapping
INDEX_NAME = 'parktest'
if es.indices.exists(INDEX_NAME):
    print("deleting index...")
    res = es.indices.delete(index = INDEX_NAME)

os.system('curl -X PUT ec2-52-3-61-194.compute-1.amazonaws.com:9200/parktest/')
# os.system('curl -X PUT ec2-52-3-61-194.compute-1.amazonaws.com:9200/geotest/')

bb= """curl -X PUT ec2-52-3-61-194.compute-1.amazonaws.com:9200/parktest/parktest/_mapping -d '{
    "parktest": {
        "properties": {
            "location": {
                "type": "geo_point",
                "lat_lon": true,
                "geohash": true
            }
        }
    }
}'
"""
# bb= """curl -X PUT ec2-52-3-61-194.compute-1.amazonaws.com:9200/geotest/geotest/_mapping -d '{
#     "geotest": {
#         "properties": {
#             "location": {
#                 "type": "geo_point",
#                 "lat_lon": true,
#                 "geohash": true
#             }
#         }
#     }
# }'
# """
os.system(bb)


# bulk index and search

bulk_data1 = []

a = """
{"name" : "parking_A",
"location": {
  "lon": -71.285605,
  "lat": 46.869125
},
"availability": 23
}
"""
aa = """
{"name" : "parking_B",
  "location": {
    "lon": -71.356247,
    "lat": 46.855498
  },
  "availability": 12
  }
"""
aaa = """
{"name" : "Blore_IN",
  "location": {
    "lon": 77.594563,
    "lat": 12.971599
  },
  "availability": 100
  }
"""
# a = """
# {"name" : "Rue de Barfleur - Charlesbourg",
# "location": {
#   "lon": -71.285605,
#   "lat": 46.869125
# }
# }
# """
# aa = """
# {"name" : "Rue Racine - La Haute-Saint-Charles",
#   "location": {
#     "lon": -71.356247,
#     "lat": 46.855498
#   }
#   }
# """
b = json.loads(a)
bb = json.loads(aa)
bbb = json.loads(aaa)

bulk_data1.append(b)
bulk_data1.append(bb)
bulk_data1.append(bbb)

# q = '{"query":{"filtered":{"query":{"match_all":{}},"filter":{"geo_distance":{"distance":"100km","location":{"lat":46.884106,"lon":-71.377042}}}}}}'
q = '{"query":{"filtered":{"query":{"match_all":{}},"filter":{"geo_distance":{"distance":"100km","location":{"lat":46.884106,"lon":-71.377042}}}}}}'
# q = '{"query":{"filtered":{"query":{"match_all":{}},"filter":{"geo_distance":{"distance":"100km","location":{"lat":12.969773,"lon":77.597337}}}}}}'
# results = helpers.bulk(es, bulk_data1, index='geotest', doc_type='geotest', refresh=True)
results = helpers.bulk(es, bulk_data1, index=INDEX_NAME, doc_type=INDEX_NAME, refresh=True)

res = es.search(index = INDEX_NAME, size=5, body=q)
print json.dumps(res, indent=2)
print ""
print "total number of returned records are ",len(res['hits']['hits'])
