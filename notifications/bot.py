import schedule
import time
import os
import pendulum
from notifications.discord_sender import Discord
from sleeper_wrapper import League, Stats, Players
from notifications.constants import STARTING_MONTH, STARTING_YEAR, STARTING_DAY, START_DATE_STRING
from notifications.injury_report import get_injury_report
from notifications.stonks import get_trade_leaders, get_trending_players

"""
These are all of the utility functions.
"""


def get_league_scoreboards(league_id, week):
    """
    Returns the scoreboards from the specified sleeper league.
    :param league_id: Int league_id
    :param week: Int week to get the scoreboards of
    :return: dictionary of the scoreboards; https://github.com/SwapnikKatkoori/sleeper-api-wrapper#get_scoreboards
    """
    league = League(league_id)
    matchups = league.get_matchups(week)
    users = league.get_users()
    rosters = league.get_rosters()
    scoreboards = league.get_scoreboards(rosters, matchups, users, "pts_half_ppr", week)
    return scoreboards


def make_roster_dict(starters_list, bench_list):
    """
    Takes in a teams starter list and bench list and makes a dictionary with positions.
    :param starters_list: List of a teams starters
    :param bench_list: List of a teams bench players
    :return: {starters:{position: []} , bench:{ position: []} }
    """
    week = get_current_week()
    players = Players().get_all_players()
    stats = Stats()
    week_stats = stats.get_week_stats("regular", STARTING_YEAR, week)

    roster_dict = {"starters": {}, "bench": {}}
    for player_id in starters_list:
        player = players[player_id]
        player_position = player["position"]
        player_name = player["first_name"] + " " + player["last_name"]
        try:
            player_std_score = week_stats[player_id]["pts_std"]
        except KeyError:
            player_std_score = None

        player_and_score_tup = (player_name, player_std_score)
        if player_position not in roster_dict["starters"]:
            roster_dict["starters"][player_position] = [player_and_score_tup]
        else:
            roster_dict["starters"][player_position].append(player_and_score_tup)

    for player_id in bench_list:
        player = players[player_id]
        player_position = player["position"]
        player_name = player["first_name"] + " " + player["last_name"]

        try:
            player_std_score = week_stats[player_id]["pts_std"]
        except KeyError:
            player_std_score = None

        player_and_score_tup = (player_name, player_std_score)
        if player_position not in roster_dict["bench"]:
            roster_dict["bench"][player_position] = [player_and_score_tup]
        else:
            roster_dict["bench"][player_position].append(player_and_score_tup)

    return roster_dict


def map_users_to_team_name(users):
    """
    Maps user_id to team_name
    :param users:  https://docs.sleeper.app/#getting-users-in-a-league
    :return: Dict {user_id:team_name}
    """
    users_dict = {}

    # Maps the user_id to team name for easy lookup
    for user in users:
        try:
            users_dict[user["user_id"]] = user["metadata"]["team_name"]
        except:
            users_dict[user["user_id"]] = user["display_name"]
    return users_dict


def map_roster_id_to_owner_id(league_id):
    """

    :return: Dict {roster_id: owner_id, ...}
    """
    league = League(league_id)
    rosters = league.get_rosters()
    result_dict = {}
    for roster in rosters:
        roster_id = roster["roster_id"]
        owner_id = roster["owner_id"]
        result_dict[roster_id] = owner_id

    return result_dict


def check_starters_and_bench(lineup_dict):
    """

    :param lineup_dict: A dict returned by make_roster_dict
    :return:
    """
    for key in lineup_dict:
        pass


def get_current_week():
    """
    Gets the current week.
    :return: Int current week
    """
    today = pendulum.today()
    starting_week = pendulum.datetime(STARTING_YEAR, STARTING_MONTH, STARTING_DAY)
    week = today.diff(starting_week).in_weeks()
    return week + 1


"""
These are all of the functions that create the final strings to send.
"""


def send_any_string(string_to_send):
    """
    Send any string to the bot.
    :param string_to_send: The string to send a bot
    :return: string to send
    """
    return string_to_send


def get_matchups_string(league_id):
    """
    Creates and returns a message of the current week's matchups.
    :param league_id: Int league_id
    :return: string message of the current week mathchups.
    """
    week = get_current_week()
    scoreboards = get_league_scoreboards(league_id, week)
    final_message_string = "________________________________\n"
    final_message_string += "Matchups for Week {}:\n".format(week)
    final_message_string += "________________________________\n\n"

    for i, matchup_id in enumerate(scoreboards):
        matchup = scoreboards[matchup_id]
        matchup_string = "Matchup {}:\n".format(i + 1)
        matchup_string += "{} VS. {} \n\n".format(matchup[0][0], matchup[1][0])
        final_message_string += matchup_string

    return final_message_string


def get_scores_string(league_id):
    """
    Creates and returns a message of the league's current scores for the current week.
    :param league_id: Int league_id
    :return: string message of the current week's scores
    """
    week = get_current_week()
    scoreboards = get_league_scoreboards(league_id, week)
    final_message_string = "Scores \n____________________\n\n"
    for i, matchup_id in enumerate(scoreboards):
        matchup = scoreboards[matchup_id]
        print(matchup)
        first_score = 0
        second_score = 0
        if matchup[0][1] is not None:
            first_score = matchup[0][1]
        if matchup[1][1] is not None:
            second_score = matchup[1][1]
        string_to_add = "Matchup {}\n{:<8} {:<8.2f}\n{:<8} {:<8.2f}\n\n".format(i + 1, matchup[0][0], first_score,
                                                                                matchup[1][0], second_score)
        final_message_string += string_to_add

    return final_message_string


def get_standings_string(league_id):
    """
    Creates and returns a message of the league's standings.
    :param league_id: Int league_id
    :return: string message of the leagues standings.
    """
    league = League(league_id)
    rosters = league.get_rosters()
    users = league.get_users()
    standings = league.get_standings(rosters, users)
    final_message_string = "________________________________\n"
    final_message_string += "Standings \n|{0:^7}|{1:^7}|{2:^7}|{3:^7}\n".format("rank", "team", "wins", "points")
    final_message_string += "________________________________\n\n"
    try:
        playoff_line = os.environ["NUMBER_OF_PLAYOFF_TEAMS"] - 1
    except:
        playoff_line = 5
    for i, standing in enumerate(standings):
        team = standing[0]
        if team is None:
            team = "Team NA"
        if len(team) >= 7:
            team_name = team[:7]
        else:
            team_name = team
        string_to_add = "{0:^7} {1:^10} {2:>7} {3:>7}\n".format(i + 1, team_name, standing[1], standing[3])
        if i == playoff_line:
            string_to_add += "________________________________\n\n"
        final_message_string += string_to_add
    return final_message_string


def run_notifications():
    """
    Main script for the bot
    """
    print('########## RUNNING NOTIFICATIONS ################')
    bot = None

    league_id = os.environ["LEAGUE_ID"]

    # Check if the user specified the close game num. Default is 20.
    try:
        close_num = os.environ["CLOSE_NUM"]
    except:
        close_num = 20

    starting_date = pendulum.datetime(STARTING_YEAR, STARTING_MONTH, STARTING_DAY)

    webhook = os.environ["WEBHOOK"]
    announcements_webhook = os.environ["ANNOUNCEMENTS_WEBHOOK"]
    spam_webhook = os.environ["SPAM_WEBHOOK"]
    print(f"Webhook is {webhook}, announcements is {announcements_webhook}, spam is {spam_webhook}")

    spam_bot = Discord(spam_webhook)
    announcements = Discord(announcements_webhook)
    bot = Discord(webhook)
    doctor_bot = Discord(webhook, "Injury Report",
                         "https://www.kindpng.com/picc/m/9-98059_red-cross-doctor-nurse-first-aid-logo-medical.png")
    stonks_bot = Discord(webhook, "Stonks", "https://m.media-amazon.com/images/I/81l-+mFDVzL._SS500_.jpg")
    awards_bot = Discord(webhook, "Draft Awards",
                         "https://image.shutterstock.com/image-vector/trophy-victory-reward-success-icon-260nw-1176405127.jpg")

    # scheduled injury reports
    schedule.every().sunday.at("13:00").do(doctor_bot.send, get_injury_report, league_id)
    schedule.every().thursday.at("19:00").do(doctor_bot.send, get_injury_report, league_id)

    # scheduled lineup reminders
    schedule.every().sunday.at("12:00").do(announcements.send, send_any_string, "REMINDER: NFL main slate today, set your lineups")
    schedule.every().thursday.at("18:00").do(announcements.send, send_any_string, "REMINDER: NFL games start today, set your lineups")

    # scheduled trending player report
    schedule.every().sunday.at("11:00").do(stonks_bot.send, get_trending_players)
    schedule.every().tuesday.at("17:00").do(stonks_bot.send, get_trending_players)

    spam_bot.send(get_trending_players)
    spam_bot.send(get_injury_report, league_id)
    spam_bot.send(get_trade_leaders, league_id, get_current_week())

    spam_bot.send(get_matchups_string, league_id)
    spam_bot.send(get_scores_string, league_id)

    # schedule.every().thursday.at("19:00").do(bot.send, get_matchups_string, league_id)  # Matchups Thursday at 4:00 pm ET
    # schedule.every().friday.at("12:00").do(bot.send, get_scores_string, league_id)  # Scores Friday at 12 pm ET
    # schedule.every().sunday.at("22:00").do(bot.send, get_close_games_string, league_id, int(close_num))  # Close games Sunday on 7:00 pm ET
    # schedule.every().monday.at("12:00").do(bot.send, get_scores_string, league_id)  # Scores Monday at 12 pm ET
    # schedule.every().tuesday.at("15:00").do(bot.send, get_standings_string, league_id)  # Standings Tuesday at 11:00 am ET
    # schedule.every().tuesday.at("15:01").do(bot.send, get_best_and_worst_string, league_id)  # Standings Tuesday at 11:01 am ET

    while True:
        if starting_date <= pendulum.today():
            schedule.run_pending()
        time.sleep(15)
