from django.core.management.base import BaseCommand
from NBAapp.models import BoxScore, Team, PlayerStats
from bs4 import BeautifulSoup, Comment

import requests
import pandas as pd
import time

class Command(BaseCommand):
    help = "Seed Box Scores Table"


    def handle(self, *args, **options):
        dates = pd.date_range(start = "2024-03-28", end = "2024-03-28")
        base_link = "https://www.basketball-reference.com"

        for date in dates:
            link = base_link + "/boxscores/?month={0}&day={1}&year={2}".format(date.month, date.day, date.year)

            page = requests.get(link)
            soup = BeautifulSoup(page.content, "html.parser")
            # Get all games for the day
            try:
                games = soup.find("div", class_ = "game_summaries").find_all("table", class_= "teams")
                # Loop through all games to get boxscore link
                for game in games:
                    boxscore_link = game.find("td", class_ = "gamelink").find("a", href = True)['href']

                    # Access boxscore board to get teams
                    page = requests.get(base_link + boxscore_link)
                    time.sleep(2)
                    soup = BeautifulSoup(page.content, "html.parser")

                    teams = soup.find("div", class_="scorebox").find_all("strong")
                    team1_text = teams[0].text.strip()
                    team2_text = teams[1].text.strip()
                    team1 = Team.objects.get(team_name = team1_text)
                    team2 = Team.objects.get(team_name = team2_text)

                    # Get team abbreviation
                    comment = soup.find("div", id = 'all_line_score').find(string=lambda text: isinstance(text, Comment))
                    if "div_line_score" in comment:
                        line_score = BeautifulSoup(comment.string, "html.parser")

                        data = line_score.find('tbody').find_all("th")
                        team1_abbr = data[0].text
                        team2_abbr = data[1].text
                    
                        teams = [team1_abbr, team2_abbr]

                    teams_d = dict()
                    teams_d[team1_abbr] = Team.objects.get(team_name=team1_text)
                    teams_d[team2_abbr] = Team.objects.get(team_name=team2_text)
                    teams_against = dict()
                    teams_against[team1_abbr] = Team.objects.get(team_name=team2_text)
                    teams_against[team2_abbr] = Team.objects.get(team_name=team1_text)
                    for team in teams:
                        # Get stats for two teams respectively, this is basic stats
                        all_stats_row_basic1 = soup.find("div", id = 'div_box-'+team+'-game-basic')
                        stats = all_stats_row_basic1.find('tbody').find_all('tr')
                        name_l = []
                        basic_l = []
                        for stat in stats:
                            player_name = stat.find('th').text.strip()
                            if player_name == "Reserves":
                                continue
                            name_l.append(player_name)

                            player_stat = stat.find_all('td')

                            # Did not play for whatever reasons
                            if "Did Not" in player_stat[0].text:
                                basic_l.append([])
                                continue
                            tmp = []
                            # Fill in empty data slots
                            for i in player_stat:
                                if i.text.strip() == '':
                                    tmp.append(0.0)
                                else:
                                    tmp.append(i.text.strip())
                            basic_l.append(tmp)

                        # This is advanced stats with percentages
                        all_stats_row_adv1 = soup.find("div", id = 'div_box-'+team+'-game-advanced')
                        stats = all_stats_row_adv1.find('tbody').find_all('tr')
                        adv_l = []
                        for stat in stats:
                            player_name= stat.find('th').text.strip()
                            if player_name == "Reserves":
                                continue

                            player_stat = stat.find_all('td')

                            if "Did Not" in player_stat[0].text:
                                adv_l.append([])
                                continue
                            tmp = []
                            for i in player_stat:
                                tmp.append(i.text.strip())
                            adv_l.append(tmp)
                        
                        # Constructing input models to database
                        for i in range(len(name_l)):
                            # Hardcoded fill-in-the-blanks stats
                            if basic_l[i] == []:
                                basic_l[i] = [0] * 20
                                adv_l[i] = [0] * 16
                            playerStat = PlayerStats(date = date,
                                                    team = teams_d[team],
                                                    # against_team = teams_against[team],
                                                    player_name = name_l[i],
                                                    mp = basic_l[i][0],
                                                    fg = basic_l[i][1],
                                                    fga = basic_l[i][2],
                                                    fg_pct = basic_l[i][3],
                                                    fg3 = basic_l[i][4],
                                                    fg3a = basic_l[i][5],
                                                    fg3_pct = basic_l[i][6],
                                                    ft = basic_l[i][7],
                                                    fta = basic_l[i][8],
                                                    ft_pct = basic_l[i][9],
                                                    orb = basic_l[i][10],
                                                    drb = basic_l[i][11],
                                                    trb = basic_l[i][12],
                                                    ast = basic_l[i][13],
                                                    stl = basic_l[i][14],
                                                    blk = basic_l[i][15],
                                                    tov = basic_l[i][16],
                                                    pf = basic_l[i][17],
                                                    pts = basic_l[i][18],
                                                    plus_minus = basic_l[i][19],
                                                    ts_pct = adv_l[i][1],
                                                    efg_pct = adv_l[i][2],
                                                    fg3a_per_fga_pct = adv_l[i][3],
                                                    fta_per_fga_pct = adv_l[i][4],
                                                    orb_pct = adv_l[i][5],
                                                    drb_pct = adv_l[i][6],
                                                    trb_pct = adv_l[i][7],
                                                    ast_pct = adv_l[i][8],
                                                    stl_pct = adv_l[i][9],
                                                    blk_pct = adv_l[i][10],
                                                    tov_pct = adv_l[i][11],
                                                    usg_pct = adv_l[i][12],
                                                    off_rtg = adv_l[i][13],
                                                    def_rtg = adv_l[i][14],
                                                    bpm = adv_l[i][15])
                            playerStat.save()

                            print(f"PLAYER STATS FOR {name_l[i]} FROM TEAM {teams_d[team]} IN THE GAME {team1_text} vs {team2_text} ON {date.month}-{date.day}-{date.year} ADDED!")
            except Exception as e:
                print(e)
                print(f"NO GAMES PLAYED ON {date.month}-{date.day}-{date.year}.")
                time.sleep(2)

    
            