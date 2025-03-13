import pandas as pd
from itertools import combinations


def get_archive_of_matchups(past_matches, pool):
    # Filter matches where both players are in the pool
    filtered_df = past_matches[past_matches['player 1'].isin(pool) & past_matches['player 2'].isin(pool)]

    # Create a normalized pair column to avoid order issues
    filtered_df['matchup'] = filtered_df.apply(lambda row: tuple(sorted([row['player 1'], row['player 2']])), axis=1)

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


def pick_next_matchups(match_count, pool):
    available_players = set(pool)
    match_count = match_count.sort_values('count')
    next_matchups = []

    for matchup in match_count['matchup']:
        if matchup[0] in available_players and matchup[1] in available_players:
            next_matchups.append(matchup)
            available_players.remove(matchup[0])
            available_players.remove(matchup[1])

        if len(available_players) <= 1:
            break  # Stop if we have an odd player left out

    return next_matchups, available_players