# Set up environment
sh env_setup.sh

# Configure local database in NBAProject/settings.py

# Seed Postgres Database
python manage.py migrate\
python manage.py seedTeams\
python manage.py seedBoxScores\
python manage.py seedPlayers

# Run App
python manage.py runserver
