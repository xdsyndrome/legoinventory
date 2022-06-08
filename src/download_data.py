"""Download Lego Data
This module downloads Lego Data from Rebrickable
"""
import os
import re
import logging
from http.client import IncompleteRead
from tqdm import tqdm
from bs4 import BeautifulSoup
import requests
import yaml
import pandas as pd

dir_ = os.path.join(os.getcwd(), 'config.yaml')
with open(fr'{dir_}', 'r') as file:
    CONFIG_ = yaml.safe_load(file)

class LegoData:
    """_summary_
    Attributes
        dataset_names: list of dataset names
        downloads_urls: mapping of dataset names to download URLs
        datasets: mapping of dataset names to dataframes
    """
    def __init__(self, url, config, download=False):
        self.url = url
        self.dataset_names = config['datasets']
        self.downloads_urls = dict()
        self.soup = LegoData.get_connection(self.url)
        self.downloads_urls = self.get_download_urls(self.soup)
        if download:
            self.datasets = self.download_data()
            self.save_dataset()

    @staticmethod
    def get_connection(url):
        """Gets connection to website

        Args:
            url (string): Website URL

        Returns:
            BeautifulSoup: parsed HTML content
        """
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        return soup

    def get_download_urls(self, soup):
        """Gets URLs for downloading CSVs

        Args:
            soup (BeautifulSoup): soup object to get CSV downloads from

        Returns:
            list[string]: List of CSV URLs
        """
        results = soup.find_all("a",
                      {"href": re.compile(r'downloads/')},
                      href=True,
                      text=re.compile(r'.csv'))
        url_list = [x['href'] for x in results]
        for dataset_name in self.dataset_names:
            for url in url_list:
                if dataset_name in url:
                    self.downloads_urls[dataset_name] = url
        return self.downloads_urls

    def download_data(self):
        """Downloads the .csv data into dataframes in self.datasets

        Returns:
            dict{dataset_name: dataframe}: dataset_name
        """
        self.datasets = dict()
        retry_count = 3
        datasets_to_retry = []
        for dataset_name in tqdm(self.dataset_names):
            print(self.downloads_urls[dataset_name])
            try:
                self.datasets[dataset_name] = pd.read_csv(self.downloads_urls[dataset_name], compression='gzip')
            except IncompleteRead:
                print(f'Unable to download {dataset_name}')
                datasets_to_retry.append(dataset_name)
        while datasets_to_retry:
            # Retry up to 3 times
            try:
                retry_dataset = datasets_to_retry.pop()
                self.datasets[retry_dataset] = pd.read_csv(self.downloads_urls[retry_dataset], compression='gzip')
            except IncompleteRead:
                datasets_to_retry.append(retry_dataset)
            retry_count -= 1
            if retry_count == 0:
                break
        if datasets_to_retry:
            print(f'Unable to download {datasets_to_retry} after 3 tries.')
        return self.datasets

    def save_dataset(self):
        """_summary_
        """
        file_path = os.path.join(os.getcwd(), 'data/')
        for dataset in self.datasets:
            print(f'Saving {dataset} in {file_path}')
            try:
                self.datasets[dataset].to_csv(fr'{file_path}{dataset}.csv')
                print(f'Saved as {dataset}.csv')
            except OSError:
                print("Please grant write access")
        return

lego = LegoData(url="https://rebrickable.com/downloads/", config=CONFIG_, download=False)