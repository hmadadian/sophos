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
