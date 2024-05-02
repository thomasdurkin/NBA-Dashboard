from django.core.management.base import BaseCommand
from NBAapp.models import Team


class Command(BaseCommand):
    help = "Seed Team Table"

    def handle(self, *args, **options):
        teams = {"Atlanta Hawks" : "ATL",
                "Boston Celtics" : "BOS",
                "Brooklyn Nets" : "BKN",
                "Charlotte Hornets": "CHA",
                "Chicago Bulls" : "CHI",
                "Cleveland Cavaliers" : "CLE",
                "Dallas Mavericks" : "DAL",
                "Denver Nuggets" : "DEN",
                "Detroit Pistons" : "DET",
                "Golden State Warriors" : "GSW",
                "Houston Rockets" : "HOU",
                "Indiana Pacers" : "IND",
                "Los Angeles Clippers" : "LAC",
                "Los Angeles Lakers" : "LAL",
                "Memphis Grizzlies" : "MEM",
                "Miami Heat" : "MIA",
                "Milwaukee Bucks" : "MIL",
                "Minnesota Timberwolves" : "MIN",
                "New Orleans Pelicans" : "NOP",
                "New York Knicks": "NYK",
                "Oklahoma City Thunder" : "OKC",
                "Orlando Magic" : "ORL",
                "Philadelphia 76ers" : "PHI",
                "Phoenix Suns" : "PHX",
                "Portland Trail Blazers" : "POR",
                "Sacramento Kings" : "SAC",
                "San Antonio Spurs" : "SAS",
                "Toronto Raptors" : "TOR",
                "Utah Jazz" : "UTA",
                "Washington Wizards" : "WAS"}
         
        for team, abbr in teams.items():
            t = Team(team_name  = team,
                     team_abbr = abbr)
            t.save()
        
        print("TEAMS HAVE SUCCESSFULLY BEEN ADDED TO DATABASE!")
            