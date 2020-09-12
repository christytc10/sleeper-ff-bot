import csv
import difflib
from fuzzywuzzy import fuzz
prices = {}


def load_prices():
    with open("discord_bot/pricing/sf.csv") as f:
        records = csv.DictReader(f)
        for row in records:
            prices[row['name']] = row['value']


def find_value(player_name):
    if prices is None or len(prices) == 0:
        load_prices()
    matches = difflib.get_close_matches(player_name, prices)
    if len(matches) == 0:
        print('Could not determine value for ' + player_name)
        return 0
    ratio = fuzz.ratio(matches[0].lower(), player_name.lower())
    if ratio > 80:
        return float(prices.get(matches[0]))
    else:
        print(f'Closest match for {player_name} is {matches[0]}(ratio:{ratio}). Not close enough')
        return 0

