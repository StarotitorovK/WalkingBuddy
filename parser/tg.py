import pandas as pd
import re
from telethon.sync import TelegramClient
from telethon import functions, types

from parser.config import API_ID, phone, API_HASH, BASE_DIR
# File config.py is unique, create it using Telegram API documentation

client = TelegramClient(phone, API_ID, API_HASH, system_version='4.16.30-vxCUSTOM')
client.start()


# PARSING SETTINGS FOR THE CHANNEL "LOCALSHERE"
def filter_posts_locals(raw_data):
    clean_data = []
    pattern = re.compile("\*\*Location.*\*\*")  # Pattern of suitable posts

    for i in raw_data.index:
        if raw_data['Text'][i]:
            parsed = raw_data['Text'][i].split('\n')
            if pattern.match(parsed[0]):
                clean_data.append([parsed[2], parsed[4], ''.join(parsed[5:-1]), raw_data['Grouped_id'][i]])

    df_clean = pd.DataFrame(clean_data, columns=['Title', 'Address', 'Description', 'Grouped_id'])
    return df_clean


async def get_photos_locals(data, grouped_id):
    photos = data[data['Grouped_id'] == grouped_id]
    for i in photos.index:
        await client.download_media(photos['Media'][i], file=f'{BASE_DIR}/database/tg_locals/{grouped_id}_{str(i)}.jpg')


async def main_locals():
    chat = 'https://t.me/localshere'
    data_message = []
    part_mes = client.iter_messages(chat)  # Get posts from channel with url "chat"

    async for message in part_mes:
        data_message.append([message.grouped_id, message.text, message.media])
    raw_message = pd.DataFrame(data_message, columns=['Grouped_id', 'Text', 'Media'])

    clean_message = filter_posts_locals(raw_message)  # Get df with places
    for id in clean_message['Grouped_id'].unique():
        await get_photos_locals(raw_message, id)  # Download photos of the place

    clean_message.to_csv(f'{BASE_DIR}/database/tg_locals/clean_data.csv')
    raw_message.to_csv(f'{BASE_DIR}/database/tg_locals/raw_data.csv')


# PARSING SETTINGS FOR THE CHANNEL "MY ROUTES"

def filter_posts_qaroutes(raw_data):
    clean_data = []

    for i in raw_data.index:
        if raw_data['Text'][i]:
            parsed = raw_data['Text'][i].split('*')
            match = re.findall(r"\b[А-ЯA-Z][А-ЯA-Z'’0-9 -]{3,}\b", raw_data['Text'][i])
            if match and len(parsed) > 2:
                if len(parsed[-1]) > len(parsed[-2]):
                    data = parsed[-1]
                else:
                    data = parsed[-2].split('📍')[0]
                data = data.replace('\n', ' ')
                data = data.replace('[', '')
                clean_data.append([match, '', data, re.findall(r"(https:.*)", data), raw_data['Grouped_id'][i]])

    df_clean = pd.DataFrame(clean_data, columns=['Title', 'Address', 'Description', 'Links', 'Grouped_id'])
    return df_clean


async def get_photos_qaroutes(data, grouped_id):
    photos = data[data['Grouped_id'] == grouped_id]
    for i in photos.index:
        await client.download_media(photos['Media'][i], file=f'{BASE_DIR}/database/tg_locals/{grouped_id}_{str(i)}.jpg')


async def main_qaroutes():
    chat = 'https://t.me/qaroutes'
    data_message = []
    part_mes = client.iter_messages(chat)  # Get posts from channel with url "chat"
    i = 0
    async for message in part_mes:
        i += 1
        data_message.append([message.grouped_id, message.text, message.media])
        print('Message', i, 'is done')
    raw_message = pd.DataFrame(data_message, columns=['Grouped_id', 'Text', 'Media'])

    clean_message = filter_posts_qaroutes(raw_message)  # Get df with places
    # for id in clean_message['Grouped_id'].unique():
    #     await get_photos_locals(raw_message, id)  # Download photos of the place

    clean_message.to_csv(f'{BASE_DIR}/database/tg_qaroutes/clean_data.csv')
    raw_message.to_csv(f'{BASE_DIR}/database/tg_qaroutes/raw_data.csv')


# Start parsing application
async def main():
    # await main_locals()
    await main_qaroutes()


with client:
    client.loop.run_until_complete(main())
