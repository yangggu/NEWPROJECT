import os
os.environ['PATH'] = os.environ.get('PATH', '') + ':/path/to/chrome'

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

class WebDriverSingleton:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            try:
                service = Service(ChromeDriverManager().install())
                options = webdriver.ChromeOptions()
                options.add_argument('--headless')
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--disable-gpu') 
                options.add_argument('--window-size=1920x1080') 
                cls._instance = webdriver.Chrome(service=service, options=options)
            except WebDriverException as e:
                print(f"웹 드라이버 오류: {e}")
        return cls._instance

    @classmethod
    def quit_instance(cls):
        if cls._instance is not None:
            cls._instance.quit()
            cls._instance = None
