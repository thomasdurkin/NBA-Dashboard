# Set up environment
sh env_setup.sh

# Configure local database in NBAProject/settings.py

# Seed Postgres Database
python manage.py seedTeams\
python manage.py seedBoxScores

# Run App
python manage.py runserver
