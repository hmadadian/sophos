import argparse
from reverse_enginning import ReverseEnginning
from selenium_scrap import SeleniumScrap
from table_process import TableProcess
from output import Output
from urllib.parse import urlparse


# Validate the scraping_method argument input
def sm_check(a):
    if a.lower() != "selenium" and a.lower() != "reverse":
        raise argparse.ArgumentTypeError(
            'You should choose [--scraping-method] value from "selenium" or "reverse"')
    return a


# Validate the link argument input
def link_check(a):
    parsed_url = urlparse(a)
    if parsed_url:
        if parsed_url.netloc == "www.teletal.hu" and parsed_url.path.strip('/').split('/')[0] == "etlap":
            return a
    raise argparse.ArgumentTypeError(
        'You should enter a valid Teletal menu URL. e.g., "https://www.teletal.hu/etlap/24"')


# Validate the output argument input
def output_check(a):
    if a.lower() != "html" and a.lower() != "table" and a.lower() != "json":
        raise argparse.ArgumentTypeError(
            'You should choose [--output] value from "html" , "table" or "json"')
    return a


# Execution
def execute(scraping_method, link, search_term, output_method):
    # Create scraper object based on scraping_method input
    if scraping_method == "reverse":
        scraper = ReverseEnginning(link)
    else:
        scraper = SeleniumScrap(link)
        # m.SCROLL_PAUSE_TIME=0.5
    tables_raw_data = scraper.scrape()
    table = TableProcess(tables_raw_data)
    table.create_dict()
    table.filter_dict(search_term)
    data = table.get_cheapest_food_week()
    # Create output object and formatting based on output argument input
    output_data = Output(data)
    if output_method == "html":
        output_data.to_html()
    elif output_method == "table":
        output_data.to_table(False)
    else:
        output_data.to_json()


# Execution of the application
if __name__ == '__main__':
    # Parsing arguments throw the CLI
    parser = argparse.ArgumentParser(
        description='Get the cheapest meal including your desired component, from the "teletal.hu" weekly menu!' +
                    ' e.g., "csirkemell"\n Notice: the search term should be in Hungarian.')
    parser.add_argument('--scraping-method', metavar='<Scraping-Method>', type=sm_check,
                        help='There are two types of scraping methods for this application. Use "selenium" for' +
                             ' scraping the web page using the Selenium library, or use "reverse" for scraping the' +
                             ' web page using methods that I found by reverse engineering! default is "reverse"',
                        default="reverse", nargs='?')
    parser.add_argument('--search-term', metavar='<Search-Term>', type=str,
                        help='Enter the desired meal name as a search term. This will search the entire menu to' +
                             ' find meals containing that component.', default="csirkemell", nargs='?')
    parser.add_argument('--link', metavar='<Teletal-Menu-Link>', type=link_check,
                        help='Specify the link to the menu on the Teletal website. ' +
                             'e.g., "https://www.teletal.hu/etlap/24"', default="https://www.teletal.hu/etlap/24",
                        nargs='?')
    parser.add_argument('--output', metavar='<Result-Output>', type=output_check,
                        help='Use "html" for exporting data to an HTML file and show in the browser, or use "table"' +
                             ' to show in tabled (markdown) format in a text file, or use "json" to show in JSON' +
                             ' format in CLI! default is "table".', default="table", nargs='?')
    args = vars(parser.parse_args())
    execute(args["scraping_method"], args["link"], args["search_term"], args["output"])
