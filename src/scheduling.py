import pandas as pd
import random
from itertools import combinations


def get_archive_of_matchups(past_matches, pool):
    # Filter matches where both players are in the pool
    filtered_df = past_matches[past_matches['player 1'].isin(pool) & past_matches['player 2'].isin(pool)].copy()

    # Create a normalized pair column to avoid order issues
    filtered_df['matchup'] = None
    for idx in filtered_df.index:
        row = filtered_df.loc[idx, :]
        filtered_df.at[idx, 'matchup'] = tuple(sorted([row['player 1'], row['player 2']]))

    # Count occurrences of each matchup
    match_counts = filtered_df['matchup'].value_counts().to_dict()

    # Generate all possible matchups
    all_matchups = {tuple(sorted(pair)): 0 for pair in combinations(pool, 2)}

    # Merge counts with all possible matchups
    for matchup, count in match_counts.items():
        all_matchups[matchup] = count

    # Convert to DataFrame
    result_df = pd.DataFrame(list(all_matchups.items()), columns=['matchup', 'count'])

    return result_df


def pick_next_matchups(match_count, pool, ranking):
    available_players = set(pool)
    match_count = match_count.sort_values('count')
    next_matchups = []

    if len(available_players) % 2 != 0:
        if len(available_players.intersection(set(ranking['player']))) > 0:
            # Filter by players already in ranking, if any
            filtered_df = ranking[ranking['player'].isin(available_players)]
            odd_player =  filtered_df.loc[filtered_df['games_played'].idxmax(), 'player']
        else:
            odd_player = random.choice(list(available_players))

        available_players.remove(odd_player)
    else:
        odd_player = []

    for matchup in match_count['matchup']:
        if matchup[0] in available_players and matchup[1] in available_players:
            next_matchups.append(matchup)
            available_players.remove(matchup[0])
            available_players.remove(matchup[1])

        if len(available_players) <= 1:
            break  # Stop if we have an odd player left out

    return next_matchups, odd_player


def create_matchup_table(matchups):

    df = pd.DataFrame(
        columns=['player 1', 'player 2', 'score 1', 'score 2']
    )
    for pair in matchups:
        df.loc[len(df), ['player 1', 'player 2', 'score 1', 'score 2']] = \
            [pair[0], pair[1], '', '']

    return df


def generate_sign_up_table(ranks, pool):

    all_players = list(set(list(ranks['player']) + list(pool)))
    signup_df = pd.DataFrame()
    signup_df['player'] = all_players
    signup_df['playing'] = ''

    signup_df = signup_df.sort_values('player')

    return signup_df
