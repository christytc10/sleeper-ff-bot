import csv
import difflib
from fuzzywuzzy import fuzz
import os.path


def parse_row(row):
    keys = list(row.keys())
    row_string = ""
    position = row['POS']
    for key in keys:
        if row[key] in [None, "", "-", "0.0"]:
            continue
        if key.startswith("TM "):
            continue
        if position != "QB" and key.startswith("Pass"):
            continue
        val = row[key]
        row_string += f"{key}: {val}\n"
    return row_string


def get_weekly_stats(player_name, week):
    prices = {}
    fname = f"discord_bot/weekly_stats/weeklystats.csv"
    if not os.path.isfile(fname):
        return "No idea"
    with open(fname) as f:
        records = csv.DictReader(f)
        for row in (x for x in records if int(x['WK']) == week):
            prices[row['Player']] = parse_row(row)
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


def get_player_stat(player_name, stat_name):
    prices = {}
    fname = f"discord_bot/weekly_stats/weeklystats.csv"
    if not os.path.isfile(fname):
        return "No idea"
    with open(fname) as f:
        records = csv.DictReader(f)
        for row in (x for x in records if x['Player'] == player_name):
            prices[row['WK']] = row[stat_name]
    stat_string = f"{stat_name} by week:\n"
    for k in prices:
        stat_string += f'{k}: {prices[k]}\n'
    return stat_string