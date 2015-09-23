import requests
import time

for i in range(10):
    requests.get('https://parakana.herokuapp.com/get_parking_data')
    # time.sleep(2)
