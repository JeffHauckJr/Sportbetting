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

        # Create frames for each sport
        self.football_frame = tk.Frame(self.root)
        self.basketball_frame = tk.Frame(self.root)
        self.baseball_frame = tk.Frame(self.root)

        # Create dropdown for selecting sports
        self.sports_dropdown = ttk.Combobox(self.root, values=self.get_sports_list())
        self.sports_dropdown.set("Select Sport")
        self.sports_dropdown.pack()

        # Create a label to display information
        self.info_label = tk.Label(self.root, text="Select a sport from the dropdown.")
        self.info_label.pack()

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
                # Extract the titles from the response
                titles = [sport["title"] for sport in data if sport["title"] in ["NFL", "NCAAF", "NBA", "MLB", "NCAAB"]]
                return titles
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                return []
        else:
            print(f"Failed to fetch sports list. Status code: {response.status_code}")
            return []

    def show_sport_frame(self, event):
        selected_sport = self.sports_dropdown.get()

        # Hide all frames
        self.football_frame.pack_forget()
        self.basketball_frame.pack_forget()
        self.baseball_frame.pack_forget()

        # Show the selected frame
        if selected_sport == "NCAAF":
            self.display_football_page()
        elif selected_sport == "NFL":
            self.display_basketball_page()
        elif selected_sport == "NBA":
            self.display_baseball_page()
        elif selected_sport == "MLB":
            self.display_baseball_page()
        elif selected_sport == "NCAAB":
            self.display_ncaab_page()

        self.get_sport_odds(selected_sport)

    def get_sport_odds(self, selected_sport):

        url = f"https://api.the-odds-api.com/v4/sports/{selected_sport}/odds"
        params = {"apiKey": API_KEY,
                  "regions": REGIONS,
                  "markets": MARKETS}
        
        response = requests.get(url, params)

        if (response.status_code == 200):
            odds_data = response.json()
            print(odds_data)
        else:
            print(f"Failed to fetch odds. Status code: {response.status_code}")
            print(response.text)
        

    def display_football_page(self):
        # Replace this with the logic to display NCAA Football information
        self.info_label.config(text="NCAA Football Information Page")

    def display_basketball_page(self):
        # Replace this with the logic to display NBA or NCAA Basketball information
        self.info_label.config(text="NBA Information Page")

    def display_ncaab_page(self):
        # Replace this with the logic to display NBA or NCAA Basketball information
        self.info_label.config(text="NCAA Basketball Information Page")

    def display_baseball_page(self):
        # Replace this with the logic to display MLB information
        self.info_label.config(text="MLB Information Page")

    def run(self):
        self.root.mainloop()




# Create the main window
root = tk.Tk()

# Create an instance of the app
app = SportsBettingApp(root)

# Run the app
app.run()