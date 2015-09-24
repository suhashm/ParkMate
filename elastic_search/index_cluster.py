from elasticsearch import Elasticsearch
from elasticsearch import helpers
import json, os, time

def create_index(data):
# connect to the elasticsearch instance
    es = Elasticsearch("http://ec2-52-3-61-194.compute-1.amazonaws.com:9200")

    # create index and mapping
    INDEX_NAME = 'parktest'
    if not es.indices.exists(INDEX_NAME):
        print("deleting index...")
        res = es.indices.delete(index = INDEX_NAME)

        os.system('curl -X PUT ec2-52-3-61-194.compute-1.amazonaws.com:9200/parktest/')

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
        os.system(bb)
        # q = '{"query":{"filtered":{"query":{"match_all":{}},"filter":{"geo_distance":{"distance":"100km","location":{"lat":46.884106,"lon":-71.377042}}}}}}'
        # q = '{"query":{"match_all":{}},"script_fields":{"distance":{"params":{"lat":46.884106,"lon":-71.377042},"script":"doc[\u0027location\u0027].distanceInKm(lat,lon)"}},"filter":{"geo_distance":{"distance":"100km","location":{"lat":46.884106,"lon":-71.377042}}}}'
        # q = '{"query":{"filtered":{"query":{"match_all":{}},"filter":{"geo_distance":{"distance":"100km","location":{"lat":12.969773,"lon":77.597337}}}}}}'
        # results = helpers.bulk(es, bulk_data1, index='geotest', doc_type='geotest', refresh=True)
        # results = helpers.bulk(es, bulk_data1, index=INDEX_NAME, doc_type=INDEX_NAME, refresh=True)
        d = {}
        d['time'] = data[0][0]
        d['garage_name'] = data[0][1]
        location = {}
        location['lat'] = data[0][2]
        location['lon'] = data[0][3]
        d['location'] = location
        d['availability'] = data[1]
        es.index(index=INDEX_NAME, doc_type=INDEX_NAME, body=d, refresh=True)
