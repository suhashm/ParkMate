import os
from elasticsearch import Elasticsearch
es = Elasticsearch("http://ec2-52-3-61-194.compute-1.amazonaws.com:9200")
from elasticsearch import helpers
import json

if es.indices.exists('geotest'):
    print("deleting index...")
    res = es.indices.delete(index = 'geotest')

os.system('curl -X PUT ec2-52-3-61-194.compute-1.amazonaws.com:9200/geotest/')

bb= """curl -X PUT ec2-52-3-61-194.compute-1.amazonaws.com:9200/geotest/geotest/_mapping -d '{
    "geotest": {
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
os.system(bb)
