"""Download Lego Data
This module downloads Lego Data from Rebrickable
"""
import re
from bs4 import BeautifulSoup
import requests

class LegoData:
    """_summary_
    """
    def __init__(self, url):
        self.url = url
        self.soup = LegoData.get_connection(self.url)
        self.downloads = self.get_download_urls(self.soup)

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
        return [x['href'] for x in results]

lego = LegoData("https://rebrickable.com/downloads/")
print(lego.downloads)
