import csv
import difflib
from fuzzywuzzy import fuzz
prices = {}


def parse_row(row):
    keys = list(row.keys())
    combine_string = ""
    for key in keys:
        if row[key] is not None and row[key] != "":
            val = row[key]
            combine_string += f"{key}: {val}\n"
    return combine_string


def load_prices():
    with open("/discord_bot/weekly_stats/wk1.csv") as f:
        records = csv.DictReader(f)
        for row in records:
            prices[row['Player']] = parse_row(row)


def get_snap_counts(player_name):
    if prices is None or len(prices) == 0:
        load_prices()
    matches = difflib.get_close_matches(player_name, prices)
    if len(matches) == 0:
        print('Could not determine value for ' + player_name)
        return "No idea"
    ratio = fuzz.ratio(matches[0].lower(), player_name.lower())
    if ratio > 80:
        return prices.get(matches[0])
    else:
        print(f'Closest match for {player_name} is {matches[0]}(ratio:{ratio}). Not close enough')
        return "No idea"