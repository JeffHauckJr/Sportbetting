import tkinter as tk
from tkinter import ttk
import requests
from config import API_KEY
import json


REGIONS = 'us'
MARKETS = "h2h,spreads,totals"
ODDS_FORMAT = 'decimal'
DATE_FORMAT = 'iso'

class SportsBettingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sports Betting App")

    # Create the sports dropdown
        self.sports_dropdown = ttk.Combobox(self.root, state="readonly")
        self.sports_dropdown.pack(pady=10)

    # Populate the dropdown with titles
        sports_list = self.get_sports_list()
        self.sports_dropdown['values'] = [title for title, _ in sports_list]

    # Bind the selection event to the show_sport_frame method
        self.sports_dropdown.bind("<<ComboboxSelected>>", self.show_sport_frame)
    def get_sports_list(self):
        # Make a request to the Odds API to get a list of sports
        url = "https://api.the-odds-api.com/v4/sports"
        params = {"apiKey": API_KEY}
        response = requests.get(url, params=params)

        if response.status_code == 200:
            try:
                # Attempt to parse the JSON response
                data = response.json()

                # Check if the data is a list and contains dictionaries
                if isinstance(data, list) and all(isinstance(sport, dict) for sport in data):
                    # Define the desired titles
                    desired_titles = ["NFL", "NCAAF", "NBA", "MLB", "NCAAB"]

                    # Extract titles and keys for the desired sports as a list of tuples
                    sports_list = [(sport["title"], sport["key"]) for sport in data if sport["title"] in desired_titles]
                    return sports_list
                else:
                    print("Unexpected response format.")
                    return []
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                return []
        else:
            print(f"Failed to fetch sports list. Status code: {response.status_code}")
            return []

    def show_sport_frame(self, event):
        selected_sport_title = self.sports_dropdown.get()

    # Find the corresponding key for the selected sport
        sports_list = self.get_sports_list()
        selected_sport_key = next(key for title, key in sports_list if title == selected_sport_title)

    # Use the selected_sport_key to fetch odds
        odds_data = self.get_sport_odds(selected_sport_key)

    # Now you can process the odds_data as needed
        print(f"Odds data for {selected_sport_title}: {odds_data}")

    def get_sport_odds(self, selected_sport):

        url = f"https://api.the-odds-api.com/v4/sports/{selected_sport}/odds"
        params = {"apiKey": API_KEY,
                  "regions": REGIONS,
                  "markets": MARKETS}
        
        response = requests.get(url, params)

        if response.status_code == 200:
            odds_data = response.json()
            return odds_data
        else:
            print(f"Failed to fetch odds. Status code: {response.status_code}")
            return {}

    def run(self):
        self.root.mainloop()




# Create the main window
root = tk.Tk()

# Create an instance of the app
app = SportsBettingApp(root)

# Run the app
app.run()