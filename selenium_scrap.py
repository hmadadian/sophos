from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import logging
import os


class SeleniumScrap:
    def __init__(self, url):
        self.__url = url
        # Each scrolling after 0.7 threshold
        self.SCROLL_PAUSE_TIME = 0.7
        # Disable Logging
        logging.getLogger('WDM').setLevel(logging.NOTSET)
        os.environ['WDM_LOG'] = "false"
        # Chrome webdriver Options
        chrome_options = Options()
        # Run in Background
        chrome_options.add_argument('--headless')
        # Set rendering page size to 1080P resolution
        chrome_options.add_argument("window-size=1920,1080")
        # Disable webdriver binding log
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.__driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.__scraped_data = None
        self.__tables_content = dict()

    # Scrape the page and process the javascript
    def scrape(self):
        self.__driver.get(self.__url)
        # Define tag for scrolling
        body = self.__driver.find_element(By.CSS_SELECTOR, "body")
        while True:
            # Send Page down key
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(self.SCROLL_PAUSE_TIME)
            elements = self.__driver.find_elements(By.TAG_NAME, "footer")
            # If it reach the end stop scrolling
            if [e.text for e in elements] != ['']:
                break
            else:
                continue
        # Convert it to BeautifulSoup object
        self.__scraped_data = BeautifulSoup(self.__driver.page_source, 'html.parser')
        self.__driver.close()
        self.__get_tables()
        return self.__tables_content

    # Retrieve tables
    def __get_tables(self):
        # Find all section which has 'ewid' attribute in it
        sections = self.__scraped_data.findAll('section', {"ewid": True})
        for section in sections:
            # Find all tr tags in each section and slice it from 3 position (first and second is useless)
            table_content = section.div.table.tbody.find_all('tr')[2:]
            # If it contains kod="NF11" in the first element slice it from 4 position because it is useless too
            if table_content[0]["kod"] == "NF11":
                table_content = section.div.table.tbody.find_all('tr')[3:]
            # If it contains kod="Z10" in the first element slice it from 2 position because 2 tr element is needed
            if table_content[0]["kod"] == "Z10":
                table_content = section.div.table.tbody.find_all('tr')[1:]
            # Join the sliced tr tags and assign it to __tables_content with table name as key
            joined_html = ' '.join([str(elem) for elem in table_content])
            self.__tables_content[section["section"]] = joined_html
