from sleeper_wrapper import League, User, Players
import json


def get_trade_leaders(league_id=517097510076678144, current_week=16):
    print(f'Getting trades for league {league_id} up to week {current_week}')
    trades_by_user = {}
    final = {}

    league = League(league_id)
    users = []
    rosters = league.get_rosters()
    for roster in rosters:
        userApi = User(roster['owner_id'])
        user = userApi.get_user()
        users.append({
            'username': user['username'],
            'user_id': user['user_id'],
            'roster_id': roster['roster_id'],
            'completed_trades': 0
        })
        trades_by_user[user['username']] = 0

    print(trades_by_user)
    for week in range(0, current_week):
        txns = league.get_transactions(week)
        if len(txns) == 0:
            continue

        trades = [txn for txn in txns if txn['type'] == 'trade' and txn['status'] == 'complete']
        trades_by_roster = []

        for trade in trades:
            trades_by_roster.append(trade['roster_ids'][0])
            trades_by_roster.append(trade['roster_ids'][1])

        for user in users:
            trades_done = trades_by_roster.count(user['roster_id'])
            trades_by_user[user['username']] = trades_by_user[user['username']] + trades_done
    for x in trades_by_user:
        if x in final:
            final[x] += trades_by_user.get(x)
        else:
            final[x] = trades_by_user.get(x)

    trade_leaders_string = "**Trade Leaderboard**\n"
    sorted_by_user = {k: v for k, v in sorted(final.items(), key=lambda item: item[1], reverse=True)}
    for z in sorted_by_user:
        if sorted_by_user.get(z) is None:
            continue
        trade_leaders_string += f'{z}: {sorted_by_user.get(z)}\n'
    return trade_leaders_string


def get_trending_players():
    players_api = Players()
    players = players_api.get_all_players()
    trends_players = players_api.get_trending_players("nfl", "add", 24, 5)

    formatted_players = []

    for trends_player in trends_players:
        player = players[trends_player['player_id']]
        url = f'https://sleepercdn.com/content/nfl/players/thumb/{trends_player["player_id"]}.jpg'
        print(url)
        formatted_players.append({
            "name": player['full_name'],
            "position": player['position'],
            "adds": trends_player['count'],
            "avatar": url})
    print(formatted_players)
    # return json.dumps(formatted_players)
    return '{"content": "Trending Players (last 24 hours)", "embeds": [{"description": "RB - Chicago Bears", "color": 7506394, "author": {"name": "1. Ryan Nall", "icon_url": "https://sleepercdn.com/content/nfl/players/thumb/5163.jpg"}, "footer": {"text": "200 adds"}}, {"description": "TE - New Orleans Saints", "author": {"name": "2. Jared Cook", "icon_url": "https://sleepercdn.com/content/nfl/players/thumb/5163.jpg"}, "footer": {"text": "150 adds"}}, {"description": "WR - Denver Broncos", "color": 15728640, "author": {"name": "2. KJ Hamler", "icon_url": "https://sleepercdn.com/content/nfl/players/thumb/5163.jpg"}, "footer": {"text": "150 adds"}}, {"description": "WR - Denver Broncos", "color": 971092, "author": {"name": "2. Jerry Jeudy", "icon_url": "https://sleepercdn.com/content/nfl/players/thumb/5163.jpg"}, "footer": {"text": "150 adds"}}]}'
