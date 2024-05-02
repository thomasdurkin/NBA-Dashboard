from django.core.management.base import BaseCommand
from NBAapp.models import BoxScore, Team
from bs4 import BeautifulSoup, Comment

import requests
import pandas as pd


class Command(BaseCommand):
    help = "Seed Box Scores Table"


    def handle(self, *args, **options):
        dates = pd.date_range(start = "2024-04-30", end = "2024-04-30")
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

                    # Access boxscore
                    page = requests.get(base_link + boxscore_link)
                    soup = BeautifulSoup(page.content, "html.parser")

                    # Line Score data is stored in comments so this is a work around
                    comment = soup.find("div", id = 'all_line_score').find(string=lambda text: isinstance(text, Comment))
                    if "div_line_score" in comment:
                        line_score = BeautifulSoup(comment.string, "html.parser")

                        teams = line_score.find_all("a")
                        team1_text = teams[0].text.strip()
                        team2_text = teams[1].text.strip()
                        team1 = Team.objects.get(team_abbr = team1_text)
                        team2 = Team.objects.get(team_abbr = team2_text)
                       

                        data = line_score.find('tbody').find_all("td")
                        team1_q1_points = int(data[0].text.strip())
                        team1_q2_points = int(data[1].text.strip())
                        team1_q3_points = int(data[2].text.strip())
                        team1_q4_points = int(data[3].text.strip())

                        team2_q1_points = int(data[4].text.strip())
                        team2_q2_points = int(data[5].text.strip())
                        team2_q3_points = int(data[6].text.strip())
                        team2_q4_points = int(data[7].text.strip())

                    # Four Factors data is stored in comments
                    comment = soup.find("div", id = 'all_four_factors').find(string=lambda text: isinstance(text, Comment))
                    if "div_four_factors" in comment:
                        factors = BeautifulSoup(comment.string, "html.parser")
                        
                        data = factors.find_all('td')
                        team1_pace = float(data[0].text.strip())
                        team1_efg = float(data[1].text.strip())
                        team1_tov = float(data[2].text.strip())
                        team1_orb = float(data[3].text.strip())
                        team1_ft_per_fg = float(data[4].text.strip())
                        team1_off_rtg = float(data[5].text.strip())

                        team2_pace = float(data[6].text.strip())
                        team2_efg = float(data[7].text.strip())
                        team2_tov = float(data[8].text.strip())
                        team2_orb = float(data[9].text.strip())
                        team2_ft_per_fg = float(data[10].text.strip())
                        team2_off_rtg = float(data[11].text.strip())   
                    
                    box_score = BoxScore(date=date.strftime('%Y-%m-%d'),
                                         team1 = team1,
                                         team2 = team2,
                                         team1_q1_points = team1_q1_points,
                                         team1_q2_points = team1_q2_points,
                                         team1_q3_points = team1_q3_points,
                                         team1_q4_points = team1_q4_points,
                                         team2_q1_points = team2_q1_points,
                                         team2_q2_points = team2_q2_points,
                                         team2_q3_points = team2_q3_points,
                                         team2_q4_points = team2_q4_points,
                                         team1_pace = team1_pace,
                                         team1_efg = team1_efg,
                                         team1_tov = team1_tov,
                                         team1_orb = team1_orb,
                                         team1_ft_per_fg = team1_ft_per_fg,
                                         team1_off_rtg = team1_off_rtg,
                                         team2_pace = team2_pace,
                                         team2_efg = team2_efg,
                                         team2_tov = team2_tov,
                                         team2_orb = team2_orb,
                                         team2_ft_per_fg = team2_ft_per_fg,
                                         team2_off_rtg = team2_off_rtg)
                    box_score.save()
                    print(f"BOX SCORE FOR {team1_text} vs {team2_text} for {date.month}-{date.day}-{date.year} ADDED!")
            except Exception as e:
                print(e)

    
            