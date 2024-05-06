from django.shortcuts import render
from .models import BoxScore

from bs4 import BeautifulSoup, Comment
from datetime import datetime

import requests
import pandas as pd

# Create your views here.
def index(request):

    #Load dummy data for now need to change to fanduel today's games
    games = BoxScore.objects.all()
    context = {"games": games}

    #date = datetime.today()
    #date = date.strftime("%Y%m%d")
    #link = f"https://www.espn.com/nba/schedule/_/date/{date}"

    #headers = requests.utils.default_headers()
    #headers.update({
    #    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
    #})

    #page = requests.get(link, headers=headers)
    #soup = BeautifulSoup(page.content, "html.parser")

    #todays_games = soup.find("div", class_ = "ScheduleTables").find("tbody")

    #data = []
    #rows = todays_games.find_all('tr')
    #for row in rows:
    #    cols = row.find_all('span')
    #    game = []
    #    for col in cols:
    #        col = col.text.strip()
    #        if col != "@":
    #            game.append(col)
    #    data.append(game)
  

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

def game_summary(request):

    #context = {"team_name1" : team_name1,
    #           "team_name2" : team_name2}
    
    return render(request, 'game_summary.html')

def player_props(request):

    return render(request, 'player_props.html')