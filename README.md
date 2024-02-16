# Wikipedia Scraper Countries and their leaders

This project contains a wikipedia scraper that looks for countries, their leader and fetches a short bio on their personal Wikipedia page.

For that we will query an API to obtain a list of countries and their past political leaders.

The start url is https://country-leaders.onrender.com.

The API documentation is available at https://country-leaders.onrender.com/docs

![alt text](image-1.png)

# Workflow

## Code logic flow chart:

```mermaid
graph TD;
    A["get_countries()"] --> B{? Cookie valid}
    B -- NO --> C["refresh_cookie()"] --> D[COUNTRIES]
    B -- YES --> D[COUNTRIES]
    D --> E["get_leaders(COUNTRIES)"]
    E --> F[LEADERS_DATA_PER_COUNTRY]
    F --> G["get_leaders_data(LEADERS_DATA_PER_COUNTRY)"]
    G --> H[LEADERS_DATA]
    H --> I["save_to_csv(LEADERS_DATA)"]
    H --> J["save_to_json(LEADERS_DATA)"]
```

# Installation

1. In a new folder clone the repo

```bash
git clone git@github.com:NathNacht/wikipedia-scraper-countries-and-leaders.git
```

2. Install the requirements

```bash
pip install -r requirements.txt
```

3. Run the script

```bash
$ python3 main.py
```


### Result

Find the results in the data folder: `leaders_data.json` and `leaders_data.csv`


# Usage

- This program starts from https://country-leaders.onrender.com/countries to fetch the countries.
- Next it fetches the leaders from each country
- End result is a .json and a .csv file that countains the countries, leaders (first_name, last_name), their wikipedia page and a short bio.


# Timeline

This project was created in 3 days

# Personal situation

This project was made as an assignment in the BeCode course: Data AI operator.



