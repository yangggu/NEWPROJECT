import folium
from dotenv import load_dotenv
import os

vw_apikey = os.getenv('vw_apikey')

# 지도 생성 함수 정의
def generate_map(coordinates=None, zoom=None):
    if coordinates is None:
        coordinates = [35.7, 127.7]
        zoom = 7
    else:
        zoom = 18
        
    map = folium.Map(location=coordinates, zoom_start=zoom)

    if coordinates != [35.7, 127.7]:
        folium.Marker(
            coordinates,
            # popup=folium.Popup(f'{refined_address}', max_width=200),
            icon=folium.Icon(color='blue', icon='flag')
        ).add_to(map)
    
    # 브이월드 API 추가 (배경지도, WMS(LX맵), 레이어 컨트롤, folium마커)
    folium.TileLayer(
        tiles=f'https://api.vworld.kr/req/wmts/1.0.0/{vw_apikey}/Base/{{z}}/{{y}}/{{x}}.png',
        attr='공간정보 오픈플랫폼(브이월드)',
        name='브이월드 배경지도',
    ).add_to(map)
    folium.WmsTileLayer(
        url='https://api.vworld.kr/req/wms?',
        layers='lt_c_landinfobasemap',
        request='GetMap',
        version='1.3.0',
        height=256,
        width=256,
        key=vw_apikey,
        fmt='image/png',
        transparent=True,
        name='LX맵(편집지적도)',
    ).add_to(map)
    folium.LayerControl().add_to(map)
    
    return map._repr_html_()