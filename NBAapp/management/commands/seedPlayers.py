from django.core.management.base import BaseCommand
from NBAapp.models import Player, Team
from bs4 import BeautifulSoup

import requests
import time


class Command(BaseCommand):
    help = "Seed Player Table"

    def handle(self, *args, **options):
        base_link = "https://www.basketball-reference.com"

        page = requests.get(base_link + "/teams")
        soup = BeautifulSoup(page.content, "html.parser")

        teams = soup.find("table", id = "teams_active").find_all("tr", class_ = "full_table")
        for team in teams:
            page = requests.get(base_link + team.find("a", href=True)['href'])
            soup = BeautifulSoup(page.content, "html.parser")
            time.sleep(2)
            
            # Get most recent team in table, hence break
            team_name = soup.find("h1").text.strip()
            print(f"{team_name}")
            print("-" * 25)
            rows = soup.find("tbody").find_all("tr")
            for row in rows:
                cols = row.find_all('td')
                team_link = cols[1].find("a", href=True)['href']

                page = requests.get(base_link + team_link)
                soup = BeautifulSoup(page.content, "html.parser")
                time.sleep(2)

                # Get all players on Roster
                players_table = soup.find("table", id = "roster")
                for row in players_table.tbody.find_all("tr"):
                    try:
                        number = int(row.find("th").text.strip())
                    except:
                        number = -1

                    cols = row.find_all('td')

                    if (cols != []):
                        name = cols[0].text.strip().replace("\xa0\xa0", "")
                        position = cols[1].text.strip()

                        #Check for two way player identifier
                        if(name[-1:] == ")"):
                            name = name.replace("(TW)", "")

                        team = Team.objects.filter(team_name = team_name).first()
                        p = Player(player_name = name,
                                   number = number,
                                   position = position,
                                   team = team)
                        p.save()
                        print(f"{name} SUCCESSFULLY BEEN ADDED TO DATABASE!")
                print()
                break
            