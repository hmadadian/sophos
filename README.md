# Introduction
Based on the task that Mr. Zsolt Csapi from Sophos in Hungary sent me, I should develop an application that finds the cheapest meal of each day on the menu containing "csirkemell" (chicken breast) from page "[https://www.teletal.hu/etlap/24](https://www.teletal.hu/etlap/24)" which is week 24 menu.

So I developed an application that is a bit more dynamic, which can search different components, e.g., "baconos", "gomba" or "marha". Also can crawl through other weeks' menus, e.g., "[https://www.teletal.hu/etlap/22](https://www.teletal.hu/etlap/22)" or "[https://www.teletal.hu/etlap/23](https://www.teletal.hu/etlap/23)" or any future generated menu.

**P.S.**: Search term should be in the Hungarian language!

# Challenges
There are a couple of challenges related to different sections, such as scraping, data processing, and concept.

### 1. Website using Lasy Load component (Scraping Challenge)
Lazyload is Ajax/JS component that makes the website faster by loading content when the user reaches a specific position in the website by scrolling down or clicking. So the mechanism of lazyloading is rendering a simpler HTML version when the user opens the website. If the user scrolls down or clicks on some object, a javascript code will retrieve data and overwrite the current HTML code. So, in this case, we can not simply grab the HTML of the website because it would be a pre-lazyloading content in which no useful information is there!

### 2. Full Day Menu (Concept Challenge)
If you look at the other tables, the concept is horizontal, meaning there is a row for every column (each represents the days of the week). But there is an exception! A menu called "Full Day Menu" is vertical, meaning all the rows of a column are for one meal and can only be bought as a pack! The screenshot attached below will clear everything up (click on the image to get a clear view).

![Full Day Menu](https://github.com/hmadadian/sophos/blob/main/doc-image/Challenge-2.png?raw=true)

### 3. Empty Cells in Menu (Data Processing Challenge)
It seems some days the restaurant is not working or on some specific days don't serve specific food. This may cause an empty cell (hole) in the menu. The screenshots attached below will clear everything up (click on the image to get a clear view).

![enter image description here](https://github.com/hmadadian/sophos/blob/main/doc-image/Challenge-3-1.png?raw=true)

![enter image description here](https://github.com/hmadadian/sophos/blob/main/doc-image/Challenge-3-2.png?raw=true)

# How it Works
The application contains 3 parts which will be described in different sections below!

### 1. Scraping:
As mentioned in the challenges section, there are two operational solutions for this part.
#### A. Reverse Enginning:
In this case, we should find the URL that the javascript tries to load the content. Which in this case, it is as below:

    https://www.teletal.hu/ajax/szekcio?ev=<>&het=<>&ewid=<>&varname=<>
     
All the values can retrieve from the section tag in the primary HTML. For instance:
```
<section class="uk-section uk-section-xsmall uk-section-default teletal-fozelekek" ev="2022" het="23" ewid="162900767" section="Főzelék" lang="hu">
```
**P.S.**: After loading the web page to get values from section tags, we should save the **PHPSESSID** cookie and include it in our requests header. Because without this cookie, the webserver return error!

**Pros**: 
 - Faster scraping
 - Less Resource Usage
 - More Reliable (usually no need to change the code if the style of the site changes)

**Cons**: 
 - Not always easy to find out the way.
 - Calling URL or API request format might change.
 - Retrieved data might be encoded, and decoding throws the encoded javascript!

#### B. Selenium Library and Web Driver:
Using selenium library and web drive helps us open a browser (in this case, in the background) and simulate the scrolling down. After getting to the bottom of the page and all javascript executed by the browser javascript engine, it returns the final HTML source code.

**Pros**:

- The easiest way to scraping
- Guaranteed that get the final HTML source

**Cons**:

- More time to scrape and execute javascript.
- More resources for executing web driver.
- Need fo redeveloping if website style change.

#### C. XLS File (Not operational) :
There is another way to retrieve data, and it is from an XML file downloadable on the menu page. The problem with this method that causes it impracticable is that there is some missing information in it, including the prices of some meals or menus. For instance, "Full Day Menu". However %95 websites don't support this kind of exporting, so this method is not operatable in most cases!

### 2. Processing scraped data and using proper data structure and algorithm for filtering and sorting:
After scraping data with the mentioned methods, as the scraped data are in HTML table format (as displayed below), we should first extract the raw data.
```
<table>
  <tr>
    <th>...</th>
    <th>...</th>
    <th>...</th>
  </tr>
  <tr>
    <td>...</td>
    <td>...</td>
    <td>...</td>
  </tr>
  <tr>
    <td>...</td>
    <td>...</td>
    <td>...</td>
  </tr>
</table>
```

The next step is putting this raw data in a proper data structure, which in this case, I use a nested dictionary. A sample of imported data is shown below. The attached screenshot shows how I used keys namings (click on the image to get a clear view).

```json
{"Table_Name" : {
    "Row_Name": {
      "Food_Type": {
        "Days_of_week": [
          {
            "food_description": "<>",
            "food_price": <>
          }
          .....
        ]
      }
      .....
    }
    .....
  }
  .....
  }
```

![enter image description here](https://github.com/hmadadian/sophos/blob/main/doc-image/How-it-works-1.png?raw=true)

Then with the recursive method, search in the dictionary and find a food description containing the initiate search term! If there is no search term in the description, the sub-root and root will be removed.
After filtering the dictionary, we must get the minimum price for a specific day. In another method, run the mentioned method for each day of the week and store the result in a new dictionary.

### 3. Output
The result dictionary can be exported in 3 formats:

 1. Text-based table (print in CLI or store in a file) - Default Exporting Method
 2. Save the table in HTML format and show it in the browser
 3. Export the data in JSON format (print in CLI or store in a file)

# Algorithm and Data Structures
There are 5 files as described below:

 1. `reverse_enginning.py`: Contain `ReverseEnginning` class for scraping with reverse engineering method.
 2. `selenium_scrap.py`: Contain `SeleniumScrap` class for scraping with selenium method.
 3. `table_process.py`: Contain `TableProcess` class for processing scraped data, filtering and sorting class.
 4. `output.py`: Contain `Output` class for creating formatted result (Table, HTML, JSON) as output.
 5. `main.py`: Handle CLI arguments and execute the application based on other objects and classes.

### 1. reverse_enginning.py (ReverseEnginning Class)

Attributes:  
1. `__url` (attributes, protected, str) set by the `url` variable in class initiation.
2. `__ajax_url` (attributes, protected, str) set to ajax url staticly.
3. `__cookies` (attributes, protected, dict) set as empty dictionary in class initiation.
4. `__scraped_data` (attributes, protected, None) set as None in class initiation.
5. `__none_tables` (attributes, protected, list) set as empty list in class initiation.
6. `__tables_content` (attributes, protected, dict) set as empty dictionary in class initiation.

Methods:
1. `scrape` (method, public, without argument, return dictionary object) is executing `requests` to get primary HTML content and assign it to `__scraped_data` attribute with `BeautifulSoup` HTML parser. also, assign the cookie to `__cookies` attribute. then execute `__get_tables_ajax` method. At the end returns `__tables_content`.
2. `__get_tables_ajax` (method, protected, without argument, without return) get the related `section` tags and grab values of tags' attributes. Iterate the values and send a request with the saved cookie to the ajax URL. Assign retrieved data as dictionary value and table name as the key in `__tables_content`. Append table names of those which can not retrieve in `__none_tables`. Then execute `__get_tables_website`.
3. `__get_tables_website` (method, protected, without argument, without return) is trying to retrieve the content of the tables (which is not found in Ajax) from the primary HTML source. Then join it with `__tables_content`.

### 2. selenium_scrap.py (SeleniumScrap Class)

Attributes:  
1. `__url` (attributes, protected, str) set by the `url` variable in class initiation.
2. `SCROLL_PAUSE_TIME` (attributes, public, float) set to 0.7s for scrolling the page down in class initiation.
3. `__driver` (attributes, protected, object) set as chrome web driver in class initiation
4. `__scraped_data` (attributes, protected, None) set as None in class initiation
5. `__tables_content` (attributes, protected, dict) set as empty dictionary in class initiation

Methods:
1. `scrape` (method, public, without argument, return dictionary object) is scrolling down with web driver and retrieving the full HTML content with selenium. Then assign it to `__scraped_data` attribute with `BeautifulSoup` HTML parser. Then execute `__get_tables` method. At the end returns `__tables_content`.
2. `__get_tables` (method, protected, without argument, without return) get the related `section` tags and data. Assign retrieved data as dictionary value and table name as the key in `__tables_content`.

### 3. table_process.py (TableProcess Class)

Attributes:  
1. `__data` (attributes, protected, object) set by the `scrape_data` variable in class initiation.
2. `__all_tables_dict` (attributes, protected, dict) set as empty dictionary in class initiation.
3. `__week_days` (attributes, protected, list) set as list of days in a week (in Hungarian) in class initiation.
4. `__filtered_dict` (attributes, protected, dict) set as empty dictionary in class initiation.

Methods:
1. `create_dict` (method, public, without argument, without return) is extracting the raw data with `BeautifulSoup` and create a nested dictionary. Also, dealing with challenges [#2](https://github.com/hmadadian/sophos#2-full-day-menu-concept-challenge) and [#3](https://github.com/hmadadian/sophos#3-empty-cells-in-menu-data-processing-challenge). Then assign the final result to `__all_tables_dict`.
2. `filter_dict` (method, public, with argument, without return) pass the search term as an argument and try to recursively find the search term in `__all_tables_dict`. Eliminate all roots and subroutes if they don't contain the search term. Then assign the final result to `__filtered_dict`.
3. `__get_min_price_by_day` (method, protected, with argument, return dictionary object) pass the day name (in Hungarian) as an argument, then return the minimum price food information for that specific day.
4. `get_cheapest_food_week` (method, public, without argument, return dictionary object) is calling `__get_min_price_by_day` with each day in `__week_days` and return a dictionary of all day's result.

### 4. output.py (Output Class)

Attributes:  
1. `__result` (attributes, protected, dict) set by the `result` variable in class initiation.
2. `__df` (attributes, protected, object) set to `pandas` DataFrame with given `result`.

Methods:
1. `to_html` (method, public, with argument, without return) passing a string as HTML `filename` to save exported HTML and open it in browser. The default `filename` value is `result.html`
2. `to_table` (method, public, with argument, conditional return) passing a string as a text `filename` to save exported table formatted data in a text file. Passing `print_result` for either save it in a file or print it in CLI console. The default `filename` value is `result.txt`, and the default `print_result` value is True.
3. `to_json` (method, public, with argument, conditional return) passing a string as a text `filename` to save exported JSON formatted data in a JSON file. Passing `print_result` for either save it in a file or print it in CLI console. The default `filename` value is `result.json`, and the default `print_result` value is True.

# How to Run

### 1. Create a virtual environment

A. Create a directory (Folder)
B. Download the source codes and move to the newly created directory in step A
C. Open a Terminal / Command Prompt / Powershell (based on your OS)
D. Change the directory to the newly created directory in step A
E. Create a venv environment with the below command
```
python -m venv .
```
F. Activate venv with the below command (based on your OS)
```bash
### For Command Prompt
.\Scripts\activate.bat

### For Powershell
.\Scripts\Activate.ps1

### For Linux Terminal
./Scripts/activate
```

### 2. Install dependencies and required libraries

Run the following command to install dependencies and required libraries automatically (based on your OS).
```bash
### For Windows
pip install -r .\requirements.txt

### For Linux
pip install -r ./requirements.txt
```

### 3. Run the application

Now it is time to run the application with desired arguments. A list of arguments and descriptions is mentioned below.

**Usage:**
```bash
> python main.py [-h] [--scraping-method [<Scraping-Method>]] [--search-term [<Search-Term>]] [--link [<Teletal-Menu-Link>]] [--output [<Result-Output>]]
```
**Options:**
```bash
  -h, --help            show this help message and exit
  --scraping-method [<Scraping-Method>]
                        There are two types of scraping methods for this application. Use "selenium" for scraping the web page using the Selenium library, or use "reverse" for scraping the
                        web page using methods that I found by reverse engineering! default is "reverse"
  --search-term [<Search-Term>]
                        Enter the desired meal name as a search term. This will search the entire menu to find meals containing that component.
  --link [<Teletal-Menu-Link>]
                        Specify the link to the menu on the Teletal website. e.g., "https://www.teletal.hu/etlap/24"
  --output [<Result-Output>]
                        Use "html" for exporting data to an HTML file and show in the browser, or use "table" to show in tabled (markdown) format in a text file, or use "json" to show in
                        JSON format in CLI! default is "table".
```

For instance, the following command will execute with the `selenium` scraping method and `csirkemell` as the search term and `https://www.teletal.hu/etlap/22` as the menu link and `html` as the output format.
```bash
python main.py --scraping-method "selenium" --search-term "csirkemell" --link "https://www.teletal.hu/etlap/22" --output "html"
```
