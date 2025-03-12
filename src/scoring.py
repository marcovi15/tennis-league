import pandas as pd


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

