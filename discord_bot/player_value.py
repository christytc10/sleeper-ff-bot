import csv, urllib.request
import difflib
from fuzzywuzzy import fuzz
from datetime import datetime, timedelta

prices = {}
values_updated = {"when": datetime.now() - timedelta(days = 365)}


def load_prices():
    if (prices is None or len(prices) == 0) and (abs((values_updated["when"] - datetime.now()).days) > 1):
        url = 'https://raw.githubusercontent.com/dynastyprocess/data/master/files/values.csv'
        response = urllib.request.urlopen(url)
        lines = [l.decode('utf-8') for l in response.readlines()]
        records = csv.DictReader(lines)
        for row in records:
            prices[row['player']] = float(row['value_2qb'])
    values_updated["when"] = datetime.now()


def find_value(player_name):
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
    load_prices()
    matches = difflib.get_close_matches(player_name, prices)
    if len(matches) == 0:
        print('Could not determine value for ' + player_name)
        return "No idea"
    ratio = fuzz.ratio(matches[0].lower(), player_name.lower())
    if ratio > 80:
        min_price = 0.95 * prices.get(matches[0])
        max_price = 1.05 * prices.get(matches[0])
        similars = [x for x in prices if min_price < prices.get(x) < max_price]
        return "\n".join(similars)
