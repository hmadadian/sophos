import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


class ReverseEnginning:
    def __init__(self, url):
        self.__url = url
        # Ajax url for sending requests to
        self.__ajax_url = "https://" + urlparse(self.__url).hostname + "/ajax/szekcio?"
        self.__cookies = None
        self.__scraped_data = None
        self.__none_tables = list()
        self.__tables_content = dict()

    # Scrape the primary HTML
    def scrape(self):
        response = requests.get(self.__url)
        # If it is not possible to load webpage raise error
        response.raise_for_status()
        # Save PHPSESSID as cookie
        self.__cookies = {'PHPSESSID': response.cookies["PHPSESSID"]}
        # Convert it to BeautifulSoup object
        self.__scraped_data = BeautifulSoup(response.text, 'html.parser')
        self.__get_tables_ajax()
        return self.__tables_content

    # Retrieve tables from Ajax URL
    def __get_tables_ajax(self):
        tables_sections = list()
        # Find all section which has 'ev', 'het', 'ewid' and 'section' attribute in it and store them in list of dicts
        for child in self.__scraped_data.find_all('section'):
            try:
                tables_sections.append(
                    {"ev": child['ev'], "het": child['het'], "ewid": child['ewid'], "section": child['section']})
            except:
                pass

        # Send Ajax requests with 'ev', 'het', 'ewid' and 'section' values
        for tables_section in tables_sections:
            url = self.__ajax_url + "ev={}&het={}&ewid={}&varname={}".format(
                tables_section["ev"], tables_section["het"],
                tables_section["ewid"], tables_section["section"])
            response = requests.get(url, cookies=self.__cookies)
            # If get response assign it to __tables_content with table name as key
            if len(response.text) != 0:
                self.__tables_content[tables_section["section"]] = response.text
            # If cant retrieve data, append table name to __none_tables
            else:
                self.__none_tables.append(tables_section["section"])
        if len(self.__none_tables) != 0:
            self.__get_tables_website()

    # Retrieve tables from primary HTML
    def __get_tables_website(self):
        tables_website = dict()
        for table_section in self.__none_tables:
            # Find all tr tags in each section and slice it from 3 position (first and second is useless)
            child = self.__scraped_data.find('section', {"section": table_section}).div.table.tbody.find_all('tr')[2:]
            # Join the sliced tr tags
            joined_html = ' '.join([str(elem) for elem in child])
            tables_website[table_section] = joined_html
        # Combine retrieved tables from primary HTML and retrieved tables from Ajax URL. Assign it to __tables_content
        self.__tables_content = tables_website | self.__tables_content
