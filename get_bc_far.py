from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from singleton_webdriver import WebDriverSingleton
from dotenv import load_dotenv
import os

load_dotenv()
law_apikey_id = os.getenv('law_apikey_id')

def fetch_law_page(JoNm):
    driver = WebDriverSingleton.get_instance()
    url = f"http://www.law.go.kr/DRF/lawService.do?OC={law_apikey_id}&target=law&type=html&MST=262827&JO={JoNm}"
    driver.get(url)

    try:
        # Use WebDriverWait instead of sleep
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'lawService')))
        print("Page loaded successfully.")

        # Switch to iframe
        iframe = driver.find_element(By.ID, 'lawService')
        driver.switch_to.frame(iframe)

        # Get the page source
        iframe_source = driver.page_source

        # Switch back to the default content
        driver.switch_to.default_content()

        return iframe_source
    
    except Exception as e:
        print(f"Error fetching law page: {e}")
        return None

def extract_value_from_html(html, filterword):
    if html is None:
        print("Received None HTML content.")
        return None
    
    soup = BeautifulSoup(html, 'html.parser')
    lawcon_divs = soup.find_all('div', class_='lawcon')
    for lawcon in lawcon_divs:
        for p_tag in lawcon.find_all('p'):
            text = p_tag.get_text()
            if filterword in text:
                return text.split(': ', 1)[1]
    return None

def building_coverage(landuse):
    html = fetch_law_page('008400')
    if html is None:
        print("Failed to fetch building coverage page.")
        return None
    return extract_value_from_html(html, landuse)

def floor_area_ratio(landuse):
    html = fetch_law_page('008500')
    if html is None:
        print("Failed to fetch floor area ratio page.")
        return None
    return extract_value_from_html(html, landuse)

