import os

from pytube import YouTube

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from custom_webdriver import CustomWebDriver
from utils import time_sleep

class YoutubeCrawler:
    search_url = 'https://www.youtube.com/results?search_query={}'
    
    def __init__(
        self,
        keyword,
        custom_webdriver:CustomWebDriver
    ):
        self.keyword = keyword
        self.custom_webdriver = custom_webdriver
    
    def run_crawler(self):
        self.search_url = self.search_url.format(self.keyword)
        
        self.custom_webdriver.set_web_driver()
        driver = self.custom_webdriver.web_driver
        wait = self.custom_webdriver.web_driver_wait
        
        element = driver.find_element(By.CSS_SELECTOR, '[title="동영상"]')
        element.click()

    # def get_detail_link(self):
    #     link = content.find_element(By.ID, 'thumbnail').get_attribute('href')
    #     return
    
if __name__ == '__main__':
    from custom_webdriver import ChromeDriverManager
    yc = YoutubeCrawler(
        keyword='강아지',
        custom_webdriver=CustomWebDriver()
    )
    yc.run_crawler()
    
    
    #chips > yt-chip-cloud-chip-renderer.style-scope.yt-chip-cloud-renderer.iron-selected
    # document.querySelector("#chips > yt-chip-cloud-chip-renderer.style-scope.yt-chip-cloud-renderer")