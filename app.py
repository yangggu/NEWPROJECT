from flask import Flask, request, render_template
import atexit
from singleton_webdriver import WebDriverSingleton
import get_bc_far, get_pnu_landuse, get_coord_raddr_jijache, generatemap

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    data = {}
    map_html = generatemap.generate_map()

    if request.method == 'POST':
        address = request.form['address']
        roadorparcel = 'road'
        
        if not address:
            data['error'] = "주소를 입력해 주세요."
            return render_template('index.html', map_html=map_html, data=data)
        
        try:
            print(f"Received address: {address}")
            coordinates = get_coord_raddr_jijache.get_coordinates(address, roadorparcel)
            print(f"Coordinates obtained: {coordinates}")

            if not coordinates:
                raise ValueError("Invalid address or coordinates not found.")
            
            map_html = generatemap.generate_map(coordinates)
            refined_address = get_coord_raddr_jijache.get_refined_address(address, roadorparcel)
            print(f"Refined address: {refined_address}")
            pnu = get_pnu_landuse.get_pnu(coordinates)
            print(f"PNU obtained: {pnu}")

            if not pnu:
                raise ValueError("PNU not found for the given coordinates.")
            
            landuse_list = get_pnu_landuse.get_landuse(pnu)
            print(f"Landuse list: {landuse_list}")

            if not landuse_list or len(landuse_list) < 2:
                raise ValueError("Landuse information is incomplete or missing.")
            
            building_coverage = get_bc_far.building_coverage(landuse_list[1])
            floor_area_ratio = get_bc_far.floor_area_ratio(landuse_list[1])
            print(f"Building coverage: {building_coverage}, Floor area ratio: {floor_area_ratio}")

            data = {
                    'refined_address': refined_address,
                    'landuse_list': landuse_list,
                    'building_coverage': building_coverage,
                    'floor_area_ratio': floor_area_ratio,
                }
            
        except Exception as e:
            print(f"Error occurred: {e}")
            data['error'] = "주소를 찾을 수 없습니다. 다시 시도해주세요."

    return render_template('index.html', map_html=map_html, data=data)

atexit.register(WebDriverSingleton.quit_instance)

if __name__ == "__main__":
    app.run(debug=True)