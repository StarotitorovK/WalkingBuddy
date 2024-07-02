import re
from warnings import simplefilter

import pandas as pd

from parser.config import BASE_DIR

simplefilter(action="ignore", category=pd.errors.PerformanceWarning)


def clean_locals():
    data = pd.read_csv(f'{BASE_DIR}/database/tg_locals/clean_data.csv')

    data = data[['Title', 'Address', 'Description', 'Grouped_id']]
    for i in data.index:
        # print(data['Title'][i], data['Address'][i])
        match_title = re.search("\[.*]", data['Title'][i])
        match_address = re.search("\[.*]", data['Address'][i])
        if match_title:  # If address or title contains links remove it
            data.loc[i, 'Title'] = match_title[0][1:len(match_title[0]) - 1]
        if match_address:
            data.loc[i, 'Address'] = match_address[0][1:len(match_address[0]) - 1]
    data.to_csv(f'{BASE_DIR}/clean_data_2.csv')
# database/tg_locals/
clean_locals()
