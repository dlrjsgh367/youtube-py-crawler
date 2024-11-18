from custom_webdriver import CustomWebDriver
from youtube_crawler import YoutubeCrawler

def main():
    yc = YoutubeCrawler(
        custom_webdriver=CustomWebDriver(),
        keyword='강아지',
    )
    yc.run()
    # yc.download()
    
if __name__ == '__main__':
    main()