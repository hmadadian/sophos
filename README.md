# Introduction
Based on the task that Mr. Zsolt Csapi from Sophos in Hungary sent me, I should develop an application that finds the cheapest meal of each day on the menu containing "csirkemell" (chicken breast) from page "[https://www.teletal.hu/etlap/24](https://www.teletal.hu/etlap/24)" which is week 24 menu.

So I developed an application that is a bit more dynamic, which can search different components, e.g., "baconos", "gomba" or "marha". Also can crawl through other weeks' menus, e.g., "[https://www.teletal.hu/etlap/22](https://www.teletal.hu/etlap/22)" or "[https://www.teletal.hu/etlap/23](https://www.teletal.hu/etlap/23)" or any future generated menu.

**P.S.**: Search term should be in the Hungarian language!

# Challenges
There are a couple of challenges related to different sections, such as scraping, processing, and concept.

### 1. Website using Lasy Load component (Scraping Challenge)
Lazyload is Ajax/JS component that makes the website faster by loading content when the user reaches a specific position in the website by scrolling down or clicking. So the mechanism of lazyloading is rendering a simpler HTML version when the user opens the website. If the user scrolls down or clicks on some object, a javascript code will retrieve data and overwrite the current HTML code. So, in this case, we can not simply grab the HTML of the website because it would be a pre-lazyloading content in which no useful information is there!

### 2. Full Day Menu (Concept Challenge)
If you look at the other tables, the concept is horizontal, meaning there is a row for every column (each represents the days of the week). But there is an exception! A menu called "Full Day Menu" is vertical, meaning all the rows of a column are for one meal and can only be bought as a pack! The screenshot attached below will clear everything up.

![Full Day Menu](https://github.com/hmadadian/sophos/blob/main/doc-image/Challenge-2.png?raw=true)
