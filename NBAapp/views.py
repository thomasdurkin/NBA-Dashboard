from django.shortcuts import render
from django.db.models import Q
from .models import GameOdds, Team, BoxScore, PlayerOdds, Player
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

                gameOddsObj = GameOdds(id = json['id'],
                                        date_time = date_time,
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

def game_summary(request, id):
    game = GameOdds.objects.get(id = id)

    home_team_recent = BoxScore.objects.filter(Q(team1=game.home_team) | Q(team2=game.home_team))\
                                        .order_by('-date')[:5]
    
    away_team_recent = BoxScore.objects.filter(Q(team1=game.away_team) | Q(team2=game.away_team))\
                                        .order_by('-date')[:5]
    
    context = {"game" : game,
               "home_team_recent" : home_team_recent,
               "away_team_recent" : away_team_recent}

    return render(request, 'game_summary.html', context=context)


def player_props(request):
    today = datetime.today()
    tomorrow = today + timedelta(days=1)

    today = today.strftime("%Y-%m-%dT04:00:00Z")
    tomorrow = tomorrow.strftime("%Y-%m-%dT04:00:00Z")

    todays_games = GameOdds.objects.filter(date_time__range=(today, tomorrow))

    print(today, tomorrow)
    todays_player_odds = PlayerOdds.objects.filter(Q(date_time__range=(today, tomorrow)) & Q(over_under="over"))
    todays_player_odds_cnt = todays_player_odds.count()
    print(todays_player_odds_cnt)
    context = {"games" : todays_games}

    if todays_player_odds_cnt == 0:
        player_odds = []
        for game in todays_games:
            game_id = str(game.id).replace("-", "")
            resp = requests.get(f"https://api.the-odds-api.com/v4/sports/basketball_nba/events/{game_id}/odds?",
                        params={
                            "api_key" : "18d4f5a57823e4304f11070456e9b30e",
                            "regions" : "us",
                            "markets" : "player_points,player_rebounds,player_assists,player_threes,player_points_rebounds_assists,player_points_assists",
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
                est_offset = timedelta(hours=-4)
                original_timezone = timezone.utc

                players = {}
                for bm in resp.json()['bookmakers']:
                    for m in bm['markets']:
                        for o in m['outcomes']:
                            if o['description'] not in players:
                                players[o['description']] = {"over" : {}, "under" : {}}
                                players[o['description']]['last_update'] = m['last_update']

                            if o['name'] == "Over":
                                players[o['description']]["over"][m['key']] = (o['price'], o['point'])  
                            else:
                                players[o['description']]["under"][m['key']] = (o['price'], o['point']) 

                for player, v in players.items(): 
                    player = Player.objects.filter(player_name__contains = player).first()

                    for over_under, over_under_v in v.items():
                        if over_under in ['over', 'under']:
                            obj = PlayerOdds() 
                            obj.player = player
                            obj.date_time = odds_json['commence_time']
                            obj.last_update = datetime.fromisoformat(str(v['last_update'])).astimezone(original_timezone) + est_offset
                            obj.game = game

                            if over_under == "over":
                                obj.over_under = "over"
                                for prop, prop_v in over_under_v.items():
                                    if (prop == "player_points"):
                                        obj.points_price = prop_v[0]
                                        obj.points_point = prop_v[1]
                                    elif (prop == "player_rebounds"):
                                        obj.rebounds_price = prop_v[0]
                                        obj.rebounds_point = prop_v[1]
                                    elif (prop == "player_assists"):
                                        obj.assists_price = prop_v[0]
                                        obj.assists_point = prop_v[1]
                                    elif (prop == "player_threes"):
                                        obj.threes_price = prop_v[0]
                                        obj.threes_point = prop_v[1]
                                    elif (prop == "player_points_assists"):
                                        obj.points_assists_price = prop_v[0]
                                        obj.points_assists_point = prop_v[1]
                                    elif (prop == "player_points_rebounds_assists"):
                                        obj.points_rebounds_assists_price = prop_v[0]
                                        obj.points_rebounds_assists_point = prop_v[1]
                                player_odds.append(obj)

                            if over_under == "under": 
                                obj.over_under = "under"
                                for prop, prop_v in over_under_v.items():
                                    if (prop == "player_points"):
                                        obj.points_price = prop_v[0]
                                        obj.points_point = prop_v[1]
                                    elif (prop == "player_rebounds"):
                                        obj.rebounds_price = prop_v[0]
                                        obj.rebounds_point = prop_v[1]
                                    elif (prop == "player_assists"):
                                        obj.assists_price = prop_v[0]
                                        obj.assists_point = prop_v[1]
                                    elif (prop == "player_threes"):
                                        obj.threes_price = prop_v[0]
                                        obj.threes_point = prop_v[1]
                                    elif (prop == "player_points_assists"):
                                        obj.points_assists_price = prop_v[0]
                                        obj.points_assists_point = prop_v[1]
                                    elif (prop == "player_points_rebounds_assists"):
                                        obj.points_rebounds_assists_price = prop_v[0]
                                        obj.points_rebounds_assists_point = prop_v[1]
                            obj.save()

        context["player_odds"] = player_odds
    else:
        context["player_odds"] = todays_player_odds

    return render(request, 'player_props.html', context=context)

def player_props_summary(request, id):
    player = PlayerOdds.objects.get(id = id)
    context = {"player" : player}

    return render(request, 'player_props_summary.html', context = context)