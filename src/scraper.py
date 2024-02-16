"""Code up a WikipediaScraper scraper object that allows you to structurally retrieve data from the API.

The object should contain at least these six attributes:

base_url: str containing the base url of the API (https://country-leaders.onrender.com)
country_endpoint: str → /countries endpoint to get the list of supported countries
leaders_endpoint: str → /leaders endpoint to get the list of leaders for a specific country
cookies_endpoint: str → /cookie endpoint to get a valid cookie to query the API
leaders_data: dict is a dictionary where you store the data you retrieve before saving it into the JSON file
cookie: object is the cookie object used for the API calls
The object should contain at least these five methods:

refresh_cookie() -> object returns a new cookie if the cookie has expired
get_countries() -> list returns a list of the supported countries from the API
get_leaders(country: str) -> None populates the leader_data object with the leaders of a country retrieved from the API
get_first_paragraph(wikipedia_url: str) -> str returns the first paragraph (defined by the HTML tag <p>) with details about the leader
to_json_file(filepath: str) -> None stores the data structure into a JSON file
"""

import requests
import re
import json
import csv

from requests import Session
from bs4 import BeautifulSoup

class WikipediaScraper():
    def __init__(self):
        self.base_url = 'https://country-leaders.onrender.com/'
        self.country_endpoint = self.base_url + 'countries/'
        self.leaders_endpoint = self.base_url + 'leaders/'
        self.cookie_endpoint = self.base_url + 'cookie/'
        self.leaders_data = {}
        

    def fetch_data_from_url(self, url: str, session: Session):    
        response_json = (session.get(url)).json()
        if "message" in response_json and response_json['message']in ('The cookie is expired', 'The cookie is missing'):
            self.refresh_cookie(session)
            response_json = (session.get(url)).json()
    
        return response_json

    def refresh_cookie(self, session: Session):    
        session.get(self.cookie_endpoint)

    def get_countries(self):
        with Session() as session:
            countries = self.fetch_data_from_url(self.country_endpoint, session)
        return countries


    def get_leaders(self, countries:str):
        with Session() as session:
        
            # fetch leaders/country in a dictionary
            leaders_per_country = {country: self.fetch_data_from_url(self.leaders_endpoint + "?country=" + country, session) for country in countries}
        
        return leaders_per_country

    
      
    def get_leaders_data(self, leaders_per_country):
        """
        create a dictionary that contains countrycode, first_name, last_name, wikipedia_url
        """
        leaders_data = {}
        for country_code, leaders in leaders_per_country.items():
            for leader_info in leaders:
                first_name = leader_info['first_name']
                last_name = leader_info['last_name']
                wikipedia_url = leader_info['wikipedia_url']
        
                # now going after the wikipedia_urls
                response = requests.get(wikipedia_url)
                soup = BeautifulSoup(response.text, "html.parser")
                paragraphs = soup.find_all('p')
        
                first_paragraph = self.get_first_paragraph(paragraphs)

                # Store data in a dictionary
                leader_data = {
                    'country_code': country_code,
                    'first_name': first_name,
                    'last_name': last_name,
                    'wikipedia_url': wikipedia_url,
                    'first_paragraph': first_paragraph
                }
        
                # Append the leader data to the list of leaders
                if country_code not in leaders_data:
                    leaders_data[country_code] = []
                leaders_data[country_code].append(leader_data)

        return leaders_data

    def get_first_paragraph(self, paragraphs):
            
        #print(wikipedia_url) # keep this for the rest of the notebook

        filtered_paragraphs = []
        for paragraph in paragraphs:
            if paragraph.find('b') and len(paragraph.get_text()) > 100:
                filtered_paragraphs.append(paragraph)
                break
        
        first_paragraph = filtered_paragraphs[0].text

        first_paragraph = re.sub(r"\[.*?\]", "", first_paragraph.strip())

        return first_paragraph


    def to_json(self, leaders_data, filepath:str):

        # Your dictionary
        leaders_info = leaders_data

        # Save dictionary to JSON
        with open(filepath, 'w', encoding='utf-8') as json_file:
            json.dump(leaders_info, json_file, indent=4, ensure_ascii=False)

    def to_csv(self, leaders_data, filepath:str):
        # Save dictionary to CSV
        with open(filepath, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=['country_code', 'first_name', 'last_name', 'wikipedia_url', 'first_paragraph'])
            writer.writeheader()
            for leaders in leaders_data.values():
                for leader in leaders:
                    writer.writerow(leader)
