from django.shortcuts import render
from .models import GameOdds, Team
from datetime import datetime, timedelta, timezone

import requests
import pandas as pd

# Create your views here.
def index(request):

    today = datetime.today()
    tomorrow = today + timedelta(days=1)

    today = today.strftime("%Y-%m-%dT00:00:00Z")
    tomorrow = tomorrow.strftime("%Y-%m-%dT04:00:00Z")

    todays_games = GameOdds.objects.filter(date_time__range=(today, tomorrow))
    todays_games_cnt = todays_games.count()
    context = {"games" : todays_games}

    games = []
    if todays_games_cnt == 0:
        resp = requests.get("https://api.the-odds-api.com/v4/sports/basketball_nba/odds",
                        params={
                            "api_key" : "18d4f5a57823e4304f11070456e9b30e",
                            "regions" : "us",
                            "markets" : "h2h,spreads,totals",
                            "oddsFormat" : "american",
                            "dateFormat" : "iso",
                            "bookmakers" : "fanduel",
                            "commenceTimeFrom" : today,
                            "commenceTimeTo" : tomorrow
                        })
        
        if resp.status_code != 200:
            print(f'Failed to get odds: status_code {resp.status_code}, response body {resp.text}')

        else:
            odds_json = resp.json()
            #print('Number of events:', len(odds_json))
            # Check the usage quota
            #print('Remaining requests', resp.headers['x-requests-remaining'])
            #print('Used requests', resp.headers['x-requests-used'])

            est_offset = timedelta(hours=-4)
            original_timezone = timezone.utc

            for json in odds_json:
                home_team = json['home_team']
                away_team = json['away_team']
                date_time = datetime.fromisoformat(json['commence_time']).astimezone(original_timezone) + est_offset
                bm = json['bookmakers']

                # Will need to change [0] if more sports books are added
                bookmaker = bm[0]['title']
                markets = bm[0]['markets']

                for m in markets:
                    key = m['key']
                    for team in m['outcomes']:
                        if team['name'] == home_team:
                            if key == 'h2h':
                                home_h2h_price = team['price']
                            elif key == 'spreads':
                                home_spread_price = team['price']
                                home_spread_point = team['point']
                        elif team['name'] == away_team:
                            if key == 'h2h':
                                away_h2h_price = team['price']
                            elif key == 'spreads':
                                away_spread_price = team['price']
                                away_spread_point = team['point']
                        elif team['name'] == "Over":
                            over_price = team['price']
                            over_point = team['point']
                        else:
                            under_price = team['price']
                            under_point = team['point']
                
                home_team = Team.objects.get(team_name = home_team)
                away_team = Team.objects.get(team_name = away_team)

                gameOddsObj = GameOdds(date_time = date_time,
                                        home_team = home_team,
                                        away_team = away_team,
                                        home_h2h_price = home_h2h_price,
                                        home_spread_price = home_spread_price,
                                        home_spread_point = home_spread_point,
                                        away_h2h_price = away_h2h_price,
                                        away_spread_price = away_spread_price,
                                        away_spread_point = away_spread_point,
                                        over_price = over_price,
                                        over_point = over_point,
                                        under_price = under_price,
                                        under_point =  under_point)
                gameOddsObj.save()
                games.append(gameOddsObj)
        context["games"] = games
    else:
        context["games"] = todays_games

    return render(request, 'index.html', context=context)

def game_summary(request):

    #context = {"team_name1" : team_name1,
    #           "team_name2" : team_name2}
    
    return render(request, 'game_summary.html')

def player_props(request):

    return render(request, 'player_props.html')