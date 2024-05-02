# Set up environment
sh env_setup.sh

# Seed Postgres Database
python manage.py seedTeams\
python manage.py seedBoxScores

# Run App
python manage.py runserver
