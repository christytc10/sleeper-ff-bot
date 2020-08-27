import json
import urllib.request as urlrq
import certifi


def player_stats_for_week(season, week, player_espn_ids):
    with urlrq.urlopen('https://fantasy.espn.com/apis/v3/games/ffl/seasons/2020/segments/0/leaguedefaults/3?view=kona_player_info', cafile=certifi.where()) as url:
        data = json.loads(url.read().decode())
        players = data['players']
        player_stats = []
        for player in players:
            if player['player']['id'] not in player_espn_ids:
                continue

            for week_stats in (x['stats'] for x in player['player']['stats'] if
                               x['statSourceId'] == 0 and x['seasonId'] == season and x['scoringPeriodId'] == week):
                stats_obj = {
                    'name': player['player']['fullName'],
                    'espn_id': player['id'],
                    'targets': int(week_stats.get("58", 0)),
                    'receptions': int(week_stats.get("53", 0)),
                    'rec_yards': int(week_stats.get("61", 0)),
                    'rec_tds': int(week_stats.get("43", 0)),
                    'rush_attempts': int(week_stats.get("23", 0)),
                    'rush_yards': int(week_stats.get("24", 0)),
                    'rush_tds': int(week_stats.get("25", 0))
                }
                player_stats.append(stats_obj)
        return player_stats
