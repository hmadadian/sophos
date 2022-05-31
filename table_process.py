from bs4 import BeautifulSoup


class TableProcess:
    def __init__(self, scrape_data):
        self.__data = scrape_data
        self.__all_tables_dict = dict()
        # Days of the week in list
        self.__week_days = ["Hétfő", "Kedd", "Szerda", "Csütörtök", "Péntek", "Szombat", "Vasárnap"]
        self.__filtered_dict = dict()

    # Create dictionary out of scraped data
    def create_dict(self):
        for table_name, table_raw_data in self.__data.items():
            scraped_data = BeautifulSoup(table_raw_data, 'html.parser')
            rows = dict()
            children = scraped_data.find_all('tr')

            # Horizontal Menu processing
            try:
                for child in children:
                    td_values = child.find_all('td')
                    info = dict()
                    weekly_food_list = dict()
                    # Get food descriptions in each raw
                    food_descriptions_raw = td_values[2].find_all('div', {"class": "menu-cell-text-row uk-text-break"})
                    # Get food prices in each raw
                    food_prices_raw = td_values[2].find_all('div', {"class": "menu-cell-text-row menu-price-field"})

                    food_descriptions = list()
                    food_prices = list()

                    # if a day in table is without menu
                    counter = 0
                    for i in range(len(food_descriptions_raw)):
                        if len(food_descriptions_raw) != len(food_prices_raw):
                            if food_descriptions_raw[i].text != '':
                                food_descriptions.append(food_descriptions_raw[i].text)
                                try:
                                    price = food_prices_raw[i - counter].div.h6.text[:-3]
                                    # Convert prices form string to float
                                    if "." in price:
                                        price = float(price) * 1000
                                    food_prices.append(float(price))
                                except:
                                    pass
                            else:
                                counter = counter + 1
                                food_descriptions.append(None)
                                food_prices.append(None)
                        else:
                            food_descriptions.append(food_descriptions_raw[i].text)
                            price = food_prices_raw[i].text[:-3]
                            # Convert prices form string to float
                            if "." in price:
                                price = float(price) * 1000
                            food_prices.append(float(price))

                    # assign days of the week to description
                    for week_day, food_description, food_price in zip(self.__week_days, food_descriptions, food_prices):
                        weekly_food_list[week_day] = [{"food_description": food_description,
                                                       "food_price": food_price}]
                    if len(td_values[1].h2.text) != 0:
                        info[td_values[1].h2.text] = weekly_food_list
                    # If food type is set to png file and no text, set key as "unknown"
                    else:
                        info["Unknown"] = weekly_food_list
                    rows[td_values[0].h2.text] = info

            # Vertical Menu processing
            except:
                food_descriptions = list()
                food_prices = list()
                for child in children[2:]:
                    td_values = child.find_all('td')
                    food_descriptions.append(
                        td_values[1].find_all('div', {"class": "menu-cell-text-row uk-text-break"}))
                    food_prices.append(td_values[1].find_all('div', {"class": "menu-cell-text-row menu-price-field"}))

                food_descriptions = food_descriptions[:-1]
                vertical_food_descriptions = list()
                for i in range(len(food_descriptions) + 2):
                    vertical_food_descriptions.append(list(list(zip(*food_descriptions))[i]))

                weekly_food_list = dict()
                for week_day, food_description, food_price in zip(self.__week_days, vertical_food_descriptions,
                                                                  food_prices[-1]):
                    weekly_food_list[week_day] = [{"food_description": ', '.join(x.text for x in food_description),
                                                   "food_price": float(food_price.div.h6.text[:-3]) * 1000}]
                info = dict()
                info["Full Day Menu"] = weekly_food_list
                rows["FDM"] = info
            self.__all_tables_dict[table_name] = rows

    # Filter the dictionary with mentioned search term recursively
    def filter_dict(self, search_term, node=None, trigger=True):
        if trigger:
            node = self.__all_tables_dict.copy()
            last_loop = True
        if isinstance(node, list):
            if node[0]["food_description"] is not None and search_term.lower() in node[0]["food_description"].lower():
                return node
            else:
                return None
        else:
            dupe_node = {}
            for key, val in node.items():
                current_node = self.filter_dict(search_term, val, False)
                if current_node:
                    dupe_node[key] = current_node
            try:
                last_loop
                self.__filtered_dict = dupe_node or None
            except NameError:
                return dupe_node or None

    # Find minimum price for a specific day
    def __get_min_price_by_day(self, day):
        day_food = dict()
        for key, val in self.__filtered_dict.items():
            for inner_key, inner_val in val.items():
                food_type = list(inner_val.items())[0][0]
                if day in inner_val[food_type]:
                    food_desc = inner_val[food_type][day][0]["food_description"]
                    food_price = inner_val[food_type][day][0]["food_price"]
                    day_food[inner_key] = \
                        {"table_name": key, "food_type": food_type, "food_desc": food_desc, "food_price": food_price}
        row_name = min(day_food, key=lambda x: day_food[x]['food_price'])
        day_food[row_name]["row_name"] = row_name
        return day_food[row_name]

    # Find minimum price for entire week
    def get_cheapest_food_week(self):
        cheapest_week = dict()
        for day in self.__week_days:
            try:
                result = self.__get_min_price_by_day(day)
            except:
                result = {}
            cheapest_week[day] = result
        return cheapest_week
