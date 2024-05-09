from django.db import models

class Team(models.Model):
    team_name = models.CharField(max_length=75)
    team_abbr = models.CharField(max_length=3)

    def __str__(self):
        return self.team_name

class BoxScore(models.Model):
    date = models.DateTimeField()

    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team1")
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team2")

    team1_q1_points = models.IntegerField()
    team1_q2_points = models.IntegerField()
    team1_q3_points = models.IntegerField()
    team1_q4_points = models.IntegerField()

    team2_q1_points = models.IntegerField()
    team2_q2_points = models.IntegerField()
    team2_q3_points = models.IntegerField()
    team2_q4_points = models.IntegerField()

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





