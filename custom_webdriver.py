from traceback import format_exc
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from loguru import logger

class CustomWebDriver:
    def __init__(self):
        self._web_driver = None
        self._web_driver_wait = None
        self._web_driver_options = webdriver.ChromeOptions()

    def set_web_driver(self, headless: bool = False) -> bool:
        try:
            if self._web_driver is not None:
                raise ValueError('이미 웹 드라이버 세팅이 되어 있습니다.')

            if headless:
                self._web_driver_options.add_argument('headless=new')

            self._web_driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()),
                options=self._web_driver_options
            )
            self._web_driver_wait = WebDriverWait(self._web_driver, timeout=10)
        except Exception as e:
            logger.error(f"웹 드라이버 초기화 중 오류 발생: {format_exc()}")
            return False
        return True

    @property
    def web_driver(self) -> webdriver.Chrome:
        if self._web_driver is None:
            raise ValueError("웹 드라이버가 아직 초기화되지 않았습니다.")
        return self._web_driver

    @property
    def web_driver_wait(self) -> WebDriverWait:
        if self._web_driver_wait is None:
            raise ValueError("웹 드라이버 웨잇이 아직 초기화되지 않았습니다.")
        return self._web_driver_wait