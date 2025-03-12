import gspread
import os
import pandas as pd
from google.oauth2.service_account import Credentials


BASEDIR = os.path.join(os.path.dirname(__file__), '..')

def read_sheet(file_name, sheet_name):
    creds = Credentials.from_service_account_file(os.path.join(BASEDIR, 'data', 'tennis-league-key.json'), scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"])
    client = gspread.authorize(creds)

    worksheet = client.open(file_name).worksheet(sheet_name)

    data = worksheet.get_all_records()
    df = pd.DataFrame(data)

    return df

def read_sign_up():
    """
    Reads who signed up for the event.
    """

    file_name = "sign_up_form"
    sheet_name = "sign_up"

    df = read_sheet(file_name, sheet_name)

    return df


def get_players_pool(df):
    """
    Filters for active players and returns a list of these
    :param df:
    :return:
    """
    signed_up_mask = df['Playing'].str.match(r'^y', case=False, na=False)
    players_pool = df.loc[signed_up_mask, "Player"].to_list()

    return players_pool


def read_latest_results():
    """
    Reads latest results
    :return:
    """

    file_name = "sign_up_form"
    sheet_name = "results"

    df = read_sheet(file_name, sheet_name)

    return df


def read_all_results():
    """
    Reads archive of results
    :return:
    """

    try:
        df = pd.read_csv(os.path.join(BASEDIR, 'data', 'results_archive.csv'))
    except pd.errors.EmptyDataError:
        df = pd.DataFrame()

    return df


def update_results(old_results, new_results):
    """
    Integrates latest results with old ones
    :param old_results:
    :param new_results:
    :return:
    """

    if old_results.empty:
        current_week = 1
        new_results['week'] = current_week
        df = new_results
    else:
        current_week = old_results['week'].max() + 1
        new_results['week'] = current_week
        df = pd.concat([old_results, new_results])

    return df, current_week


def read_ranking():

    file_name = "sign_up_form"
    sheet_name = "ranking"

    df = read_sheet(file_name, sheet_name)

    if df.empty:
        df = pd.DataFrame(columns=['player', 'points', 'games_played'])

    return df

