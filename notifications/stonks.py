from sleeper_wrapper import League, User, Players
import json


def get_trade_leaders(league_id=517097510076678144, current_week=1):
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

    for week in range(0, current_week + 1):
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

    formatted_players = "Today's Trending Players:\n"

    for trends_player in trends_players:
        player = players[trends_player['player_id']]
        name = player['full_name'] if 'full_name' in player else f"{player['first_name']} {player['last_name']}"
        formatted_players += f"{player['position']} - {player['team']} - {name} - Added {trends_player['count']} times\n"
    return formatted_players
