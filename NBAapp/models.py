from django.db import models

class Team(models.Model):
    team_name = models.CharField(max_length=75)
    team_abbr = models.CharField(max_length=3)

    def __str__(self):
        return self.team_name

class PlayerStats(models.Model):
    date = models.DateField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team")
    # against_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="against_team")
    player_name = models.CharField(max_length=30)

    mp = models.CharField(max_length=5)
    fg = models.IntegerField(default=0)
    fga = models.IntegerField(default=0)
    fg_pct = models.FloatField(default=0)
    fg3 = models.IntegerField(default=0)
    fg3a = models.IntegerField(default=0)
    fg3_pct = models.FloatField(default=0)
    ft = models.IntegerField(default=0)
    fta = models.IntegerField(default=0)
    ft_pct = models.FloatField(default=0.0)
    orb = models.IntegerField(default=0)
    drb = models.IntegerField(default=0)
    trb = models.IntegerField(default=0)
    ast = models.IntegerField(default=0)
    stl = models.IntegerField(default=0)
    blk = models.IntegerField(default=0)
    tov = models.IntegerField(default=0)
    pf = models.IntegerField(default=0)
    pts = models.IntegerField(default=0)
    plus_minus = models.FloatField(default=0)
    ts_pct = models.FloatField(default=0)
    efg_pct = models.FloatField(default=0)
    fg3a_per_fga_pct = models.FloatField(default=0)
    fta_per_fga_pct = models.FloatField(default=0)
    orb_pct = models.FloatField(default=0)
    drb_pct = models.FloatField(default=0)
    trb_pct = models.FloatField(default=0)
    ast_pct = models.FloatField(default=0)
    stl_pct = models.FloatField(default=0)
    blk_pct = models.FloatField(default=0)
    tov_pct = models.FloatField(default=0)
    usg_pct = models.FloatField(default=0)
    off_rtg = models.FloatField(default=0)
    def_rtg = models.FloatField(default=0)
    bpm = models.FloatField(default=0)

class BoxScore(models.Model):
    date = models.DateField()

    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team1")
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team2")

    team1_q1_points = models.IntegerField()
    team1_q2_points = models.IntegerField()
    team1_q3_points = models.IntegerField()
    team1_q4_points = models.IntegerField()
    team1_total = models.IntegerField()

    team2_q1_points = models.IntegerField()
    team2_q2_points = models.IntegerField()
    team2_q3_points = models.IntegerField()
    team2_q4_points = models.IntegerField()
    team2_total = models.IntegerField()

    team1_pace = models.FloatField()
    team1_efg = models.FloatField()
    team1_tov = models.FloatField()
    team1_orb = models.FloatField()
    team1_ft_per_fg = models.FloatField()
    team1_off_rtg = models.FloatField()

    team2_pace = models.FloatField()
    team2_efg = models.FloatField()
    team2_tov = models.FloatField()
    team2_orb = models.FloatField()
    team2_ft_per_fg = models.FloatField()
    team2_off_rtg = models.FloatField()


class GameOdds(models.Model):
    id = models.UUIDField(primary_key=True)
    date_time = models.DateTimeField()

    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="home_team")
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="away_team")

    home_h2h_price = models.IntegerField()
    home_spread_price = models.IntegerField()
    home_spread_point = models.FloatField()

    away_h2h_price = models.IntegerField()
    away_spread_price = models.IntegerField()
    away_spread_point = models.FloatField()

    over_price = models.IntegerField()
    over_point = models.FloatField()

    under_price = models.IntegerField()
    under_point = models.FloatField()

class Player(models.Model):
    player_name = models.CharField(max_length=30)
    number = models.IntegerField()
    position = models.CharField(max_length=2)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

class PlayerOdds(models.Model):
    game = models.ForeignKey(GameOdds, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    
    date_time = models.DateTimeField()
    last_update = models.DateTimeField()
    over_under = models.CharField(max_length=5)
    
    points_price = models.IntegerField(default=0)
    points_point = models.FloatField(default=0)

    rebounds_price = models.IntegerField(default=0)
    rebounds_point = models.FloatField(default=0)

    assists_price = models.IntegerField(default=0)
    assists_point = models.FloatField(default=0)

    threes_price = models.IntegerField(default=0)
    threes_point = models.FloatField(default=0)

    points_assists_price = models.IntegerField(default=0)
    points_assists_point = models.FloatField(default=0)

    points_rebounds_assists_price = models.IntegerField(default=0)
    points_rebounds_assists_point = models.FloatField(default=0)



