import pytest
import pandas as pd
from src.scoring import *


@pytest.mark.parametrize(
"new_df, old_df, week, expected_out", [
        (pd.DataFrame(
            index=['A', 'B', 'T'],
            data=
            {
                'points': [20, 100, 0],
            }
        ),
        pd.DataFrame(
            index=[1, 2],
            data=
            {
                'A': [20, 20],
                'C': [20, 20],
                'D': [100, 100]
            }
        ),
        3,
        pd.DataFrame(
            index=[0, 1, 2],
            data=
            {
                'A': [20, 20, 20],
                'C': [20, 20, 0],
                'D': [100, 100, 0],
                'B': [0, 0, 100],
                'T': [0, 0, 0]
            },
            dtype=float,
        ),
        )
    ]
)
def test_update_points_register(new_df, old_df, week, expected_out):

    output = update_points_register(new_df, old_df, week)

    assert output.equals(expected_out), 'Results do not match expectations.'


# Test cases:
# 1- Rankings with >12 weeks
@pytest.mark.parametrize(
"points, expected_out", [
        (pd.DataFrame(
            index=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
            data=
            {
                'A': [20] * 13,
                'B': [100] * 13,
                'C': [0] * 13
            }
        ),
        pd.DataFrame(
            index=[0, 1, 2],
            data=
            {
                'position': [1, 2, 3],
                'player': ['B', 'A', 'C'],
                'points': [100*6 + 50*6, 20*6 + 10*6, 0],
                'games_played': [13, 13, 0]
            },
        ),
        )
    ]
)
def test_calculate_rankings(points, expected_out):

    output = calculate_rankings(points)

    expected_out = expected_out.astype(
        {'position': int, 'player': object, 'points': object, 'games_played': object}
    )

    assert output.equals(expected_out), 'Results do not match expectations.'