import pandas as pd
import numpy as np
import re


def assign_points(results, ranking):

    points_df = pd.DataFrame(
        index = results['player 1'].to_list() + results['player 2'].to_list(),
    )
    points_df['points'] = 0

    for pair in results.index:
        p1 = results.loc[pair, 'player 1']
        p2 = results.loc[pair, 'player 2']

        # Add new players to rankings
        if ranking['points'].isna().all():
            min_points = 0
        else:
            min_points = ranking['points'].min()
        if p1 not in ranking['player']:
            ranking.loc[len(ranking), ['player', 'points', 'games_played']] = [p1, min_points, 0]
        if p2 not in ranking['player']:
            ranking.loc[len(ranking), ['player', 'points', 'games_played']] = [p2, min_points, 0]

        if results.loc[pair, 'score 1'] > results.loc[pair, 'score 2']:
            if ranking.loc[ranking['player']==p1, 'points'].values < ranking.loc[ranking['player']==p2, 'points'].values:
                points_df.loc[p1, 'points'] = 100 + 0.2 * ranking.loc[ranking['player']==p2, 'points']
            else:
                points_df.loc[p1, 'points'] = 100
            points_df.loc[p2, 'points'] = 20

        if results.loc[pair, 'score 1'] < results.loc[pair, 'score 2']:
            if ranking.loc[ranking['player']==p1, 'points'].values > ranking.loc[ranking['player']==p2, 'points'].values:
                points_df.loc[p2, 'points'] = 100 + 0.2 * ranking.loc[ranking['player']==p2, 'points']
            else:
                points_df.loc[p2, 'points'] = 100
            points_df.loc[p1, 'points'] = 20

    return points_df


def update_points_register(new_df, old_df, week):

    if old_df.empty:
        df = new_df.T
        df.index.rename('week')
        df = df.set_index(pd.Index([week]))
    else:
        df = old_df.copy()
        df.loc[week, new_df.index] = new_df.T.values
        # Replace those pesky b'' that appear sometimes
        df = df.map(lambda x: np.nan if isinstance(x, bytes) else x)

    df[df.isna()] = 0

    return df


def calculate_rankings(points, old_rank):

    points_halved = 6
    points_removed = 12

    if len(points) > points_halved:
        points.iloc[:-points_halved] = points.iloc[:-points_halved] / 2
    if len(points) > points_removed:
        points = points.iloc[-points_removed:]

    points = points.sum().T

    rank = pd.DataFrame(
        index=points.index,
        columns=old_rank.columns
    )

    for player in points.index:
        if player in old_rank['player']:
            tot_games = old_rank.loc[old_rank['player']==player, 'games_played'] + 1
        else:
            tot_games = 1

        rank.loc[player, ['points', 'games_played']] = [points[player], tot_games]

    rank.index.rename('player')
    rank = rank.reset_index()
    rank.sort_values(['points', 'games_played'])

    return rank