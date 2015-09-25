# q = '{"query":{"filtered":{"query":{"match_all":{}},"filter":{"geo_distance":{"distance":"100km","location":{"lat":46.884106,"lon":-71.377042}}}}}}'
# q = '{"query":{"match_all":{}},"script_fields":{"distance":{"params":{"lat":46.884106,"lon":-71.377042},"script":"doc[\u0027location\u0027].distanceInKm(lat,lon)"}},"filter":{"geo_distance":{"distance":"100km","location":{"lat":46.884106,"lon":-71.377042}}}}'
# q = '{"query":{"filtered":{"query":{"match_all":{}},"filter":{"geo_distance":{"distance":"100km","location":{"lat":12.969773,"lon":77.597337}}}}}}'
# results = helpers.bulk(es, bulk_data1, index='geotest', doc_type='geotest', refresh=True)
# results = helpers.bulk(es, bulk_data1, index=INDEX_NAME, doc_type=INDEX_NAME, refresh=True)
