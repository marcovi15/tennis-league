import pandas as pd
from src.data_paths import *
from src.scheduling import *
from src.scoring import *


# RUNS EVERY SATURDAY
# TODO: Deploy on AWS and run automatically

# Read sign ups (every Saturday)
signed_up = read_sign_up()
players_pool = get_players_pool(signed_up)

skip_flag = False
if len(players_pool) <= 1:
    print('Skipping round as not enough players signed up.')
    skip_flag = True

# Read & save results (from previous week)
latest_results = read_latest_results()
old_results = read_all_results()
all_results, current_week = update_results(old_results, latest_results)
ranking = read_ranking()

# Calculate & publish match-ups (every Saturday)
if skip_flag:
    matchup_table = pd.DataFrame(columns=[latest_results.columns[:-1]])
else:
    match_count = get_archive_of_matchups(all_results, players_pool)
    next_pairs, odd_player = pick_next_matchups(match_count, players_pool, ranking)
    if len(odd_player) > 0:
        print(f'Player resting this week: {odd_player}.')
    matchup_table = create_matchup_table(next_pairs)

# Calculate points
points_register = read_register()
new_points = assign_points(latest_results, ranking) # TODO: Fix bug that crashes if player plays twice in a week
all_points = update_points_register(new_points, points_register, current_week)

# Update rankings
new_ranks = calculate_rankings(all_points)

# Generate sign up table
sign_up_table = generate_sign_up_table(new_ranks, players_pool)

# Publish & backup everything
publishing_map = {
    'sign_up': sign_up_table,
    'match_ups': matchup_table,
    'ranking': new_ranks,
    'past_results': all_results,
    'points': all_points
}
backup_all_tables(publishing_map)
publish_all_tables(publishing_map)