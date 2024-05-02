from django.db import models

class Team(models.Model):
    team_name = models.CharField(max_length=75)
    team_abbr = models.CharField(max_length=3)

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


