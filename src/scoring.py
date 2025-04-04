import pandas as pd
import numpy as np


def calculate_points(winner: str,
                     loser: str,
                     ranking: pd.DataFrame
                     ) -> tuple[float, float]:
    """
    Calculate points of winner and loser. If loser is higher in ranking, winner gets 20% of their points as a bonus.
    :param winner: Name of winner
    :param loser: Name of loser
    :param ranking: Table with current ranking (including number of points)
    :return: Points earned by winner and loser
    """

    if ranking.loc[ranking['player'] == winner, 'points'].values < ranking.loc[ranking['player'] == loser, 'points'].values:
        win_points = np.round(100 + 0.2 * ranking.loc[ranking['player'] == loser, 'points'].values, 0)
    else:
        win_points = 100
    los_points = 30

    return win_points, los_points


def assign_points(results: pd.DataFrame,
                  ranking: pd.DataFrame
                  ) -> pd.DataFrame:
    """
    Check who won and assign points accordingly to each player
    """

    points_df = pd.DataFrame(
        index = results['player 1'].to_list() + results['player 2'].to_list(),
    )
    points_df['points'] = 0.0

    for pair in results.index:
        p1 = results.loc[pair, 'player 1']
        p2 = results.loc[pair, 'player 2']

        # Add new players to rankings
        if ranking['points'].isna().all():
            min_points = 0
        else:
            min_points = ranking['points'].min()
        if (ranking['player'] == p1).sum() == 0:
            ranking.loc[len(ranking), ['player', 'points', 'games_played']] = [p1, min_points, 0]
        if (ranking['player'] == p2).sum() == 0:
            ranking.loc[len(ranking), ['player', 'points', 'games_played']] = [p2, min_points, 0]

        sets_p1 = results.loc[pair, 'score 1']
        sets_p2 = results.loc[pair, 'score 2']
        # P1 won
        if sets_p1 > sets_p2:
            points_df.loc[p1, 'points'], points_df.loc[p2, 'points'] = calculate_points(p1, p2, ranking)
        # P2 wn
        elif sets_p1 < sets_p2:
            points_df.loc[p2, 'points'], points_df.loc[p1, 'points'] = calculate_points(p2, p1, ranking)
        # Draw
        elif bool(sets_p1) & bool(sets_p2):
            points_df.loc[p1, 'points'] = 50
            points_df.loc[p2, 'points'] = 50
            print(f'Match between {p1} & {p2} was a draw.')
        # Not played (scores are blank)
        else:
            print(f'Match between {p1} & {p2} was not played.')

    return points_df


def update_points_register(new_df: pd.DataFrame,
                           old_df: pd.DataFrame,
                           week: int
                           ) -> pd.DataFrame:
    """
    Adds latest points to historical register of points, in the form of a new row.
    """
    if old_df.empty:
        df = new_df.T
        df['week'] = week
        df = df.set_index('week')
    else:
        df = old_df.copy()
        df.loc[week, new_df.index] = new_df.T.values
        # Replace those pesky b'' that appear sometimes
        df = df.map(lambda x: np.nan if isinstance(x, bytes) else x)

    df[df.isna()] = 0

    df = df.reset_index(drop=True)

    return df


def calculate_rankings(points: pd.DataFrame
                       ) -> pd.DataFrame:
    """
    Calculates total points (time-weighed) and updates rankings and counter of games played
    """
    # Set number of weeks after which points are halved and reset
    points_halved = 6
    points_removed = 12

    points_weighted = points.copy()

    if len(points) > points_halved:
        points_weighted.iloc[:-points_halved] = points_weighted.iloc[:-points_halved] / 2
    if len(points) > points_removed:
        points_weighted = points_weighted.iloc[-points_removed:]

    sum_points = points_weighted.sum().T

    rank = pd.DataFrame(
        index=sum_points.index,
        columns=['points', 'games_played']
    )

    for player in sum_points.index:
        rank.loc[player, 'points'] = sum_points[player]
        rank.loc[player, 'games_played'] = (points[player] > 0).sum()

    rank = rank.reset_index()
    rank = rank.rename(columns={'index': 'player'})
    rank = rank.sort_values(['points', 'games_played'], ascending=False)

    rank.insert(0, 'position', np.array(range(1, len(rank) + 1)))

    rank = rank.reset_index(drop=True)

    return rank