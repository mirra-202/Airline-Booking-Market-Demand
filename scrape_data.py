import pandas as pd
import requests
from bs4 import BeautifulSoup
import random

def scrape_airfare_data():
    url = "https://en.wikipedia.org/wiki/List_of_busiest_passenger_flight_routes"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all wikitable elements
    tables = soup.find_all("table", {"class": "wikitable"})

    if not tables:
        return pd.DataFrame(columns=["route", "year", "passengers", "price"])

    table = tables[0]  # Use the first wikitable: Top 10 most capacitated flight routes

    all_data = []

    # These are the year columns we want (based on the Wikipedia table structure)
    year_columns = ["2024", "2023", "2022", "2021", "2019"]

    for row in table.find_all("tr")[1:11]:  # Only Top 10 rows
        cols = row.find_all("td")
        if len(cols) < 5:
            continue

        # Create route name from Departing and Arriving columns
        departing = cols[1].text.strip().replace("\n", " ")
        arriving = cols[2].text.strip().replace("\n", " ")
        route = f"{departing} - {arriving}"

        for i, year in enumerate(year_columns):
            try:
                pax_text = cols[4 + i].text.strip().replace(",", "")
                passengers = int(pax_text)
            except:
                passengers = None

            if passengers:
                all_data.append({
                    "route": route,
                    "year": int(year),
                    "passengers": passengers,
                    "price": random.randint(100, 500)  # Simulated price
                })

    return pd.DataFrame(all_data)
