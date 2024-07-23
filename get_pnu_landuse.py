import requests
import config
import json
vw_apikey = config.vw_apikey

# 좌표input -> 필지번호output
def get_pnu(coordinates):
    url = "https://api.vworld.kr/req/data"
    params = {
        'key': vw_apikey,
        'request': 'GetFeature',
        'service': 'data',
        'data': 'lp_pa_cbnd_bubun',
        'geomFilter': f'POINT({coordinates[1]} {coordinates[0]})',
        'format': 'json',
        'crs':'EPSG:4326'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['response']['status'] == 'OK':
            pnu = data['response']['result']['featureCollection']['features'][0]['properties']['pnu']
    return pnu

# 필지번호input -> 용도지역output
def get_landuse(pnu):
    landuse_level1 = ['도시지역', '주거지역', '상업지역', '공업지역', '녹지지역', '관리지역', '보전관리지역', '생산관리지역', '계획관리지역', '농림지역', '자연환경보전지역']
    landuse_level2 = ['전용주거지역', '제1종전용주거지역', '제2종전용주거지역', '일반주거지역', '제1종일반주거지역', '제2종일반주거지역', '제3종일반주거지역', '준주거지역', '중심상업지역', '일반상업지역', '근린상업지역', '유통상업지역', '전용공업지역', '일반공업지역', '준공업지역', '보전녹지지역', '생산녹지지역', '자연녹지지역']
    landuse_level = landuse_level1 + landuse_level2

    url = "https://api.vworld.kr/ned/data/getLandUseAttr"
    params = {
        'key': vw_apikey,
        'pnu': pnu,
        'numOfRows': 50 # 용도지역지구구역 넉넉하게 50항목 나오게 함. 넘는 경우는 없겠지?
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()

        landuse_list = []
        for field in data['landUses']['field']:
            prposAreaDstrcCodeNm = field['prposAreaDstrcCodeNm']
            if prposAreaDstrcCodeNm in landuse_level:
                landuse_list.append(prposAreaDstrcCodeNm)
    
    # 용도지역 순서 맞추기
    landuse_list.sort(key=lambda x: landuse_level.index(x.split()[0]) if x.split()[0] in landuse_level1 else len(landuse_level1))

    return landuse_list

