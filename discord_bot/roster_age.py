from sleeper_wrapper import Players, League, User


def get_roster_ages(league_id=522501269823889408):
    players = Players().get_all_players()
    rostered_ages = {}

    for roster in League(league_id).get_rosters():
        rostered_players = []
        for player in roster['players']:
            rostered_players.append(players.get(player))
        ages = []
        for x in [p['age'] for p in rostered_players]:
            ages.append(x)
        username = User(roster["owner_id"]).get_username()
        average_age = sum(ages)/len(ages)
        rostered_ages[username] = average_age

    age_string = "Roster Ages:\n"
    sort_orders = sorted(rostered_ages.items(), key=lambda x: x[1], reverse=True)
    for roster_age in sort_orders:
        age_string += f"{roster_age}\n"

    return age_string


print(get_roster_ages(522501269823889408))
