"""_summary_
"""
import warnings
import os
import yaml
import pandas as pd
from src.download_data import LegoData

warnings.filterwarnings("ignore")

dir_ = os.path.join(os.getcwd(), 'config.yaml')
with open(fr'{dir_}', 'r') as file:
    CONFIG_ = yaml.safe_load(file)

class TestLegoData:
    """_summary_
    """
    def test_get_connection_and_download(self):
        """Checks if URLs for downloading datasets are correct
        """
        test_lego = LegoData("https://rebrickable.com/downloads/", config=CONFIG_, download=False)
        soup = test_lego.soup
        urls = test_lego.get_download_urls(soup)
        test = [url.replace(".", "/").split("/") for url in urls]
        datasets = {
            "themes": 0,
            "colors": 0,
            "part_categories": 0,
            "parts": 0,
            "part_relationships": 0,
            "elements": 0,
            "sets": 0,
            "minifigs": 0,
            "inventories": 0,
            "inventory_parts": 0,
            "inventory_sets": 0,
            "inventory_minifigs": 0,
            }
        for k in datasets.copy():
            for url in test:
                if k in url:
                    datasets[k] = 1
        for _, value in datasets.items():
            assert value == 1

    def test_download_data(self):
        """Checks if downloaded csv files are not empty
        """
        test_lego = LegoData("https://rebrickable.com/downloads/", config=CONFIG_, download=False)
        for dataset_name in test_lego.dataset_names:
            file_path = os.path.join(os.getcwd(), 'data/')
            assert not pd.read_csv(fr'{file_path}{dataset_name}.csv').empty
