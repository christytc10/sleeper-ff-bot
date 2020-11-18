import csv
import difflib
import os
import re

from fuzzywuzzy import fuzz
from notifications.bot import get_current_week


def get_snap_counts_for_week(player_name, week):
    snap_counts = {}
    fname = f"discord_bot/weekly_stats/weeklystats.csv"
    if not os.path.isfile(fname):
        return None
    with open(fname) as f:
        records = csv.DictReader(f)
        for row in (x for x in records if int(x['WK']) == week):
            snap_counts[row['Player']] = row['Snap %']

    matches = difflib.get_close_matches(player_name, snap_counts)
    if len(matches) == 0:
        print('Could not determine snap count for ' + player_name)
        return 0
    ratio = fuzz.ratio(matches[0].lower(), player_name.lower())
    if ratio > 80:
        return snap_counts.get(matches[0])
    else:
        print(f'Closest match for {player_name} is {matches[0]}(ratio:{ratio}). Not close enough')
        return 0


def get_snap_counts(player_name):
    snaps = {}
    for week in range(1, get_current_week() + 1):
        snap_count = get_snap_counts_for_week(player_name, week)
        if snap_count in [None, "-", ""]:
            snap_count = 0.0
        else:
            snap_count = float(re.findall("\d+\.\d+", snap_count)[0])
        snaps[f"Week-{week}"] = snap_count

    raw = [x for x in snaps.values() if x > 0]
    snaps['Avg (active)'] = round(sum(raw) / len(raw), 2)
    snaps_string = f'{player_name} snap counts\n'
    for key in snaps.keys():
        snaps_string += f"{key}: {snaps[key]}\n"
    return snaps_string