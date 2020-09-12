import csv
import difflib
from fuzzywuzzy import fuzz
prices = {}


def load_prices():
    with open("discord_bot/pricing/sf.csv") as f:
        records = csv.DictReader(f)
        for row in records:
            prices[row['name']] = float(row['value'])


def find_value(player_name):
    if prices is None or len(prices) == 0:
        load_prices()
    matches = difflib.get_close_matches(player_name, prices)
    if len(matches) == 0:
        print('Could not determine value for ' + player_name)
        return 0
    ratio = fuzz.ratio(matches[0].lower(), player_name.lower())
    if ratio > 80:
        return prices.get(matches[0])
    else:
        print(f'Closest match for {player_name} is {matches[0]}(ratio:{ratio}). Not close enough')
        return 0


def similar_value(player_name):
    if prices is None or len(prices) == 0:
        load_prices()
    matches = difflib.get_close_matches(player_name, prices)
    if len(matches) == 0:
        print('Could not determine value for ' + player_name)
        return "No idea"
    ratio = fuzz.ratio(matches[0].lower(), player_name.lower())
    if ratio > 80:
        print(f'{matches[0]} : {prices.get(matches[0])}')
        min_price = 0.95 * prices.get(matches[0])
        max_price = 1.05 * prices.get(matches[0])
        similars = [x for x in prices if min_price < prices.get(x) < max_price]
        return "\n".join(similars)
