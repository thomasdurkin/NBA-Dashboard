# Generated by Django 4.1 on 2024-05-16 23:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('NBAapp', '0004_remove_playerodds_point_remove_playerodds_price_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayerStats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('player_name', models.CharField(max_length=30)),
                ('mp', models.CharField(max_length=5)),
                ('fg', models.IntegerField(default=0)),
                ('fga', models.IntegerField(default=0)),
                ('fg_pct', models.FloatField(default=0)),
                ('fg3', models.IntegerField(default=0)),
                ('fg3a', models.IntegerField(default=0)),
                ('fg3_pct', models.FloatField(default=0)),
                ('ft', models.IntegerField(default=0)),
                ('fta', models.IntegerField(default=0)),
                ('ft_pct', models.FloatField(default=0.0)),
                ('orb', models.IntegerField(default=0)),
                ('drb', models.IntegerField(default=0)),
                ('trb', models.IntegerField(default=0)),
                ('ast', models.IntegerField(default=0)),
                ('stl', models.IntegerField(default=0)),
                ('blk', models.IntegerField(default=0)),
                ('tov', models.IntegerField(default=0)),
                ('pf', models.IntegerField(default=0)),
                ('pts', models.IntegerField(default=0)),
                ('plus_minus', models.FloatField(default=0)),
                ('ts_pct', models.FloatField(default=0)),
                ('efg_pct', models.FloatField(default=0)),
                ('fg3a_per_fga_pct', models.FloatField(default=0)),
                ('fta_per_fga_pct', models.FloatField(default=0)),
                ('orb_pct', models.FloatField(default=0)),
                ('drb_pct', models.FloatField(default=0)),
                ('trb_pct', models.FloatField(default=0)),
                ('ast_pct', models.FloatField(default=0)),
                ('stl_pct', models.FloatField(default=0)),
                ('blk_pct', models.FloatField(default=0)),
                ('tov_pct', models.FloatField(default=0)),
                ('usg_pct', models.FloatField(default=0)),
                ('off_rtg', models.FloatField(default=0)),
                ('def_rtg', models.FloatField(default=0)),
                ('bpm', models.FloatField(default=0)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team', to='NBAapp.team'))
            ],
        ),
    ]
