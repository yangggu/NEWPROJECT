from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

class WebDriverSingleton:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            try:
                chrome_driver_path = ChromeDriverManager().install()
                service = ChromeService(chrome_driver_path)

                options = webdriver.ChromeOptions()

                options.binary_location = "/usr/bin/google-chrome"

                options.add_argument('--headless')
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--disable-gpu') 
                options.add_argument('--window-size=1920x1080') 
                cls._instance = webdriver.Chrome(service=service, options=options)
            except Exception as e:
                print(f"Failed to create WebDriver instance: {e}")
                cls._instance = None
        return cls._instance

    @classmethod
    def quit_instance(cls):
        if cls._instance is not None:
            try:
                cls._instance.quit()
            except Exception as e:
                print(f"Failed to quit WebDriver instance: {e}")
            finally:
                cls._instance = None