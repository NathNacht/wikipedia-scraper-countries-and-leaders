from src.scraper import WikipediaScraper

def main():
    output_path_json = './data/leaders_data.json'
    output_path_csv = './data/leaders_data.csv'


    # Instantiate the WikipediaScraper class
    scraper = WikipediaScraper()

    print("Processing your request...")
    print("Please be patient. This may take a few minutes.")
    print("Meanwhile you can think about what world leader you would like to meet and what question you would like to ask him/her.")

    # fetch the countries
    countries = scraper.get_countries()
    
    # fetch the leaders per country
    leaders_per_country = scraper.get_leaders(countries)
    
    # fetch the leaders_data

    leaders_data = scraper.get_leaders_data(leaders_per_country)  
    
    # export to json and csv

    scraper.to_json_file(leaders_data, output_path_json)
    scraper.to_csv_file(leaders_data, output_path_csv)

    print("Your files are ready in the data folder!")


if __name__ == "__main__":
    main()