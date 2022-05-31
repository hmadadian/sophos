import pandas as pd
import webbrowser
import os
import json


class Output:
    def __init__(self, result):
        self.__result = result
        # Convert dictionary to pandas DataFrame
        self.__df = pd.DataFrame.from_dict(result,
                                           columns=['table_name', 'row_name', 'food_type', 'food_desc', 'food_price'],
                                           orient='index')

    # Save Table in html format and open it in browser
    def to_html(self, filename="result.html"):
        self.__df.to_html(filename, justify='center')
        file = 'file:///' + os.getcwd() + '/' + filename
        webbrowser.open_new_tab(file)

    # Save or print the result in table format
    def to_table(self, print_result=True, filename="result.txt"):
        if print_result:
            print(self.__df.to_markdown())
        else:
            self.__df.to_markdown(filename)
            return self.__df

    # Save or print the result in json format
    def to_json(self, print_result=True, filename="result.json"):
        if print_result:
            print(json.dumps(self.__result, indent=4))
        else:
            with open(filename, 'w') as f:
                f.write(json.dumps(self.__result, indent=4))
            return json.dumps(self.__result)
