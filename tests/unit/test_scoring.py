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
            index=[1, 2, 3],
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
