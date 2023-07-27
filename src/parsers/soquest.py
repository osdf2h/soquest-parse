import logging
import datetime
import json
import math
import os
import time

from tqdm import tqdm

import requests

import pandas as pd

from settings import BASE_DIR

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

API_URL = 'https://api.sograph.xyz/api/campaign/list'
PAGE_SIZE = 12


class SoQuest:
    def __init__(self, address: str, signature: str):
        self.address = address
        self.signature = signature
        self.headers = {
            'address': self.address,
            'signature': self.signature
        }
        self.data = []
        self.upload_data = []

    def parse_data(self):
        logging.info('Made by https://t.me/soquest_everyday')
        time.sleep(3)
        total_count = self.__get_campaigns_count()
        if total_count > 0:
            total_pages = math.ceil(total_count / PAGE_SIZE)
            logging.info(f'Got {total_count} campaigns. Total pages: {total_pages}')
            for page in tqdm(range(1, total_pages+1)):
                self.data.extend(self.__get_data_per_page(page))
            self.__dump_json()
            self.__process_data()
            self.__dump_xlsx()
        else:
            logging.info('No active unfinished campaigns found')

    def __get_campaigns_count(self) -> int:
        logging.info(f'Start parsing SoQuest campaigns for address: {self.address}')
        params = {
            'campaign_type': 'all',
            'reward_type': 'all',
            'status': 'active',
            'trending': '0',
            'verified': '0',
            'name': '',
            'page': str(1),
            'pagesize': str(PAGE_SIZE),
            'hide_completed': '1',
        }
        response = requests.get(API_URL, params=params, headers=self.headers)
        if response.status_code == 200:
            return int(response.json().get('data').get('total'))
        else:
            return 0

    def __get_data_per_page(self, page: int) -> dict | None:
        params = {
            'campaign_type': 'all',
            'reward_type': 'all',
            'status': 'active',
            'trending': '0',
            'verified': '0',
            'name': '',
            'page': str(page),
            'pagesize': str(PAGE_SIZE),
            'hide_completed': '1',
        }
        response = requests.get(API_URL, params=params, headers=self.headers)
        if response.status_code == 200:
            return response.json().get('data').get('data')
        else:
            logging.error(f'Error with API response. Status code: {response.status_code}')
            return None

    def __process_data(self):
        for data in self.data:
            gems_count = 20 if data.get('is_verify') and data.get('is_recommend')\
                else (10 if data.get('is_verify')
                      else (1))

            end_timestamp = data.get('end_time')
            if end_timestamp:
                current_time = datetime.datetime.now()
                target_time = datetime.datetime.fromtimestamp(end_timestamp)
                time_difference = target_time - current_time
                hours_left = round(time_difference.total_seconds() / 3600, 2)
            else:
                hours_left = 'Нет ограничения'

            self.upload_data.append(
                {
                    'Кол-во гемов': gems_count,
                    'Ссылка': data.get('url'),
                    'Название кампании': data.get('space_name'),
                    'Кол-во заданий': data.get('task_count'),
                    'Тип призов': ', '.join(data.get("prize_types")),
                    'Осталось времени (ч.)': hours_left
                }
            )

    def __dump_json(self):
        with open(BASE_DIR / 'assets' / 'test.json', 'w+', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    def __dump_xlsx(self):
        cur_datetime = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M_%S')
        filename = BASE_DIR / 'assets' / f'result_{cur_datetime}.xlsx'
        df = pd.DataFrame(self.upload_data)
        grouped = df.groupby('Кол-во гемов')
        for name, group in grouped:
            if not os.path.exists(filename):
                group.to_excel(filename, sheet_name=str(name), index=False)
            else:
                with pd.ExcelWriter(filename, engine='openpyxl', mode='a') as writer:
                    group.to_excel(writer, sheet_name=str(name), index=False)
