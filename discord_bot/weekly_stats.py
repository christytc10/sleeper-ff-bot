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


def load_weekly_stats(player_name, week):
    stats = {}
    fname = f"weekly_stats/weeklystats.csv"
    if not os.path.isfile(fname):
        return "No idea"
    with open(fname) as f:
        records = csv.DictReader(f)
        for row in (x for x in records if int(x['WK']) == week):
            stats[row['Player']] = row
    matches = difflib.get_close_matches(player_name, stats)
    if len(matches) == 0:
        print(f'Could not determine stats for {player_name} in week {week}')
        return "No idea"
    ratio = fuzz.ratio(matches[0].lower(), player_name.lower())
    if ratio > 80:
        return stats.get(matches[0])
    return None


def get_weekly_stats(player_name, week):
    player_stats = load_weekly_stats(player_name, int(week))
    if player_stats is not None:
        return parse_row(player_stats)
    else:
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


def points_for_stat(stats_obj, stat_name, multiplier):
    if stat_name not in stats_obj:
        return 0.0
    return float(stats_obj[stat_name]) * multiplier


def get_fantasy_score(player_name, week):
    print(f"{player_name} in week {week}")
    stats = load_weekly_stats(player_name, int(week))
    if stats is not None:
        fantasy_points = float(stats['Fantasy Points'])
        fantasy_points += points_for_stat(stats, 'REC', 0.5)
        return fantasy_points
    return "No idea"