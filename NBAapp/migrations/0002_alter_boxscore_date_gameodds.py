# Generated by Django 4.1 on 2024-05-09 17:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('NBAapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boxscore',
            name='date',
            field=models.DateTimeField(),
        ),
        migrations.CreateModel(
            name='GameOdds',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField()),
                ('home_h2h_price', models.IntegerField()),
                ('home_spread_price', models.IntegerField()),
                ('home_spread_point', models.FloatField()),
                ('away_h2h_price', models.IntegerField()),
                ('away_spread_price', models.IntegerField()),
                ('away_spread_point', models.FloatField()),
                ('over_price', models.IntegerField()),
                ('over_point', models.FloatField()),
                ('under_price', models.IntegerField()),
                ('under_point', models.FloatField()),
                ('away_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='away_team', to='NBAapp.team')),
                ('home_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='home_team', to='NBAapp.team')),
            ],
        ),
    ]
