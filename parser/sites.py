import re

import pandas as pd
import requests

from parser.config import BASE_DIR

base_url = ' https://kudago.com/public-api/v1.4/places/'
params = {
    'fields': 'id,title,address,description,subway,tags,categories,images',
    'location': 'msk',
    'text_format': 'text',
    'page_size': '100'
}


def get_places(url):  # Get info about places from KudaGo API
    df = pd.DataFrame(columns=['id', 'title', 'address', 'description', 'subway', 'tags', 'categories', 'images'])
    response = requests.get(url, params=params)
    data = response.json()
    next_page = data['next']
    page_df = pd.DataFrame(data['results'])
    df = pd.concat([df, page_df])
    i = 1
    print(f'Page {i} is done')
    while next_page:
        print(next_page)
        response = requests.get(next_page)
        next_page = response.json()['next']
        page_df = pd.DataFrame(response.json()['results'])
        df = pd.concat([df, page_df])
        i += 1
        print(f'Page {i} is done')

    df.to_csv(f'{BASE_DIR}/database/site_kudago/raw_data.csv')


data = pd.read_csv(f'{BASE_DIR}/database/site_kudago/raw_data.csv')


def filter_places(data):  # Deleting places with name 'квест'
    clean_data = []
    for i in data.index:
        match = re.search(r'квест', data.loc[i, 'title'])
        if not match:
            clean_data.append(data.iloc[i].tolist()[1:])
    return pd.DataFrame(clean_data, columns=data.columns[1:])


# get_places(base_url)
filter_places(data).to_csv(f'{BASE_DIR}/database/site_kudago/clean_data.csv')