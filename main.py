import pandas as pd
from src.data_paths import *


# RUNS EVERY SATURDAY
# TODO: Deploy on AWS and run automatically

# Read sign ups (every Saturday)
signed_up = read_sign_up()
players_pool = get_players_pool(signed_up)

# Calculate & publish match-ups (every Saturday)


# Read & save results (from previous week)


# Update & publish rankings


# Generate sign up sheet (with all players in db)