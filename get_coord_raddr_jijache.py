import requests
from dotenv import load_dotenv
import os

vw_apikey = os.getenv('vw_apikey')

def get_coordinates(address, roadorparcel):
    url = 'https://api.vworld.kr/req/address?'
    params = {
        'service': 'address',
        'request': 'getcoord',
        'crs': 'epsg:4326',
        'address': address,
        'format': 'json',
        'type': roadorparcel,
        'key': vw_apikey
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['response']['status'] == 'OK':
            point = data['response']['result']['point']
            x = point['x']
            y = point['y']
            coordinates = [y, x] #folium 좌표는 x,y 바뀜
    return coordinates

def get_refined_address(address, roadorparcel):
    url = 'https://api.vworld.kr/req/address?'
    params = {
        'service': 'address',
        'request': 'getcoord',
        'crs': 'epsg:4326',
        'address': address,
        'format': 'json',
        'type': roadorparcel,
        'key': vw_apikey
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['response']['status'] == 'OK':
            refined_address = data['response']['refined']['text']
    return refined_address

def get_jijache(address, roadorparcel):
    url = 'https://api.vworld.kr/req/address?'
    params = {
        'service': 'address',
        'request': 'getcoord',
        'crs': 'epsg:4326',
        'address': address,
        'format': 'json',
        'type': roadorparcel,
        'key': vw_apikey
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        # with open('test.json', 'w', encoding='utf-8') as json_file:
        #     json.dump(data, json_file, ensure_ascii=False, indent=4)
        if data['response']['status'] == 'OK':
            bigcity_list = [
                '서울특별시','인천광역시','대전광역시','대구광역시','울산광역시',
                '부산광역시','광주광역시','세종특별자치시','제주특별자치도'
                ]
            level1 = data.get('response', {}).get('refined', {}).get('structure', {}).get('level1', '')
            level2 = data.get('response', {}).get('refined', {}).get('structure', {}).get('level2', '')
            if level1 in bigcity_list:
                jijache = level1
            else:
                jijache = level2

    return jijache
