import pandas as pd
from src.data_paths import *
from src.scoring import *


# RUNS EVERY SATURDAY
# TODO: Deploy on AWS and run automatically

# Read sign ups (every Saturday)
signed_up = read_sign_up()
players_pool = get_players_pool(signed_up)

# Calculate & publish match-ups (every Saturday)


# Read & save results (from previous week)
latest_results = read_latest_results()
old_results = read_all_results()
all_results, current_week = update_results(old_results, latest_results)

# Calculate points
ranking = read_ranking()
new_points = assign_points(latest_results, ranking)

# Update & publish rankings


# Generate sign up sheet (with all players in db)