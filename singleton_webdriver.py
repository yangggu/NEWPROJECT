from selenium import webdriver
import docker
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class WebDriverSingleton:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            try:
                options = webdriver.ChromeOptions()
                options.add_argument('--headless')
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--disable-gpu') 
                options.add_argument('--window-size=1920x1080') 
                
                # Selenium Remote WebDriver 설정
                cls._instance = webdriver.Remote(
                    command_executor='http://localhost:4444/wd/hub',
                    desired_capabilities=DesiredCapabilities.CHROME,
                    options=options
                )
                
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

# Docker 클라이언트 설정 및 컨테이너 실행
client = docker.from_env()

container = client.containers.run(
    "selenium/standalone-chrome:latest",
    ports={'4444/tcp': 4444},
    detach=True,
    name="zipup-selenium"
)

# 컨테이너가 완전히 시작될 때까지 대기
time.sleep(5)

# 애플리케이션이 종료될 때 컨테이너 정리
import atexit
atexit.register(lambda: container.stop())
atexit.register(lambda: container.remove())