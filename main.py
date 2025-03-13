import pandas as pd
from src.data_paths import *
from src.scheduling import *
from src.scoring import *


# RUNS EVERY SATURDAY
# TODO: Deploy on AWS and run automatically

# Read sign ups (every Saturday)
signed_up = read_sign_up()
players_pool = get_players_pool(signed_up)

# Read & save results (from previous week)
latest_results = read_latest_results()
old_results = read_all_results()
all_results, current_week = update_results(old_results, latest_results)

# Calculate & publish match-ups (every Saturday)
match_count = get_archive_of_matchups(all_results, players_pool)
next_pairs, odd_player = pick_next_matchups(match_count, players_pool)
if len(odd_player) > 0:
    print(odd_player)
# TODO: write into sheet

# Calculate points
ranking = read_ranking()
points_register = read_points_reg()
new_points = assign_points(latest_results, ranking)
all_points = update_points_register(new_points, points_register, current_week)

# Update & publish rankings
new_ranks = calculate_rankings(all_points)

# Generate sign up sheet (with all players in db)