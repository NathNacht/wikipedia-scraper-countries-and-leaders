import requests
import re
import json
import csv
from requests import Session
from bs4 import BeautifulSoup

class WikipediaScraper():
    """
    Instantiates the WikipediaScraper class
    """
    def __init__(self):
        self.base_url = 'https://country-leaders.onrender.com'
        self.country_endpoint = self.base_url + '/countries/'
        self.leaders_endpoint = self.base_url + '/leaders/'
        self.cookie_endpoint = self.base_url + '/cookie/'
        self.leaders_data = {}
        self.cookie = None
        

    def fetch_data_from_url(self, url: str, session: Session):    
        """
        Fetches data from a given url
        Checks if cookie is still valid and refreshes cookie of not

        :param url: url to fetch
        :param session: requests session
        :return: url response in json
        """
        response_json = (session.get(url)).json()

        if "message" in response_json and response_json['message']in ('The cookie is expired', 'The cookie is missing'):
            self.refresh_cookie(session)
            response_json = (session.get(url)).json()
    
        return response_json


    def refresh_cookie(self, session: Session):    
        """ 
        Refreshes the cookie

        :param session: requests session
        """
        session.get(self.cookie_endpoint)


    def get_countries(self):
        """
        Fetches the countries from the endpoint

        :return: list of countries
        """
        with Session() as session:
            countries = self.fetch_data_from_url(self.country_endpoint, session)

        return countries


    def get_leaders(self, countries:str):
        """
        Fetches the leaders from the endpoint looping over the list of countries

        :param countries: list of countries
        :return: list of leaders
        """

        with Session() as session:
            leaders_per_country = {country: self.fetch_data_from_url(self.leaders_endpoint + "?country=" + country, session) for country in countries}
        
        return leaders_per_country

      
    def get_leaders_data(self, leaders_per_country):
        """
        For each leader in each of the countries fetches first name, last name and wikipedia url
        Uses that url to fetch the first paragraph of the wikipedia page of the leader
        Creates a dictionary for each leader with the country code, first name, last name, wikipedia url and first paragraph and appends to the 
        dictionary that contains all leaders and their information

        :param leaders_per_country: dictionary of leaders per country with their details as fetched from the API
        :return: dictionary of leaders with the needed information (country code, first name, last name, wikipedia url and first paragraph of bio)
        """
        leaders_data = {}

        for country_code, leaders in leaders_per_country.items():
        
            for leader_info in leaders:
                first_name = leader_info['first_name']
                last_name = leader_info['last_name']
                wikipedia_url = leader_info['wikipedia_url']
        
                response = requests.get(wikipedia_url)
                soup = BeautifulSoup(response.text, "html.parser")
                paragraphs = soup.find_all('p')
        
                first_paragraph = self.get_first_paragraph(paragraphs)

                leader_data = {
                    'country_code': country_code,
                    'first_name': first_name,
                    'last_name': last_name,
                    'wikipedia_url': wikipedia_url,
                    'first_paragraph': first_paragraph
                }
        
                if country_code not in leaders_data:
                    leaders_data[country_code] = []
                leaders_data[country_code].append(leader_data)

        return leaders_data


    def get_first_paragraph(self, paragraphs):
        """
        Scrapes the first paragraph of the wikipedia page of the leader.
        Does some minor cleaning to remove unwanted elements

        :param paragraphs: list of paragraphs as scraped from the wikipedia page
        :return: string with the first paragraph 
        """
            
        filtered_paragraphs = []

        for paragraph in paragraphs:
        
            if paragraph.find('b') and len(paragraph.get_text()) > 100:
                filtered_paragraphs.append(paragraph)
                break
        
        first_paragraph = filtered_paragraphs[0].text

        first_paragraph = re.sub(r"\[.*?\]", "", first_paragraph.strip())

        return first_paragraph


    def to_json_file(self, leaders_data, filepath:str):
        """
        dumps the dictionary in a json file

        :param leaders_data: A dictionary with countrycode, first_name, last_name, wikipedia_url and the first paragraph of the bio
        :param filepath: The path of the json file     
        """
        
        with open(filepath, 'w', encoding='utf-8') as json_file:
            json.dump(leaders_data, json_file, indent=4, ensure_ascii=False)


    def to_csv_file(self, leaders_data, filepath:str):
        """
        dumps the dictionary in a csv file

        :param leaders_data: A dictionary with countrycode, first_name, last_name, wikipedia_url and the first paragraph of the bio
        :param filepath: The path of the json file     
        """
    
        with open(filepath, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=['country_code', 'first_name', 'last_name', 'wikipedia_url', 'first_paragraph'])
            writer.writeheader()
            for leaders in leaders_data.values():
                for leader in leaders:
                    writer.writerow(leader)
