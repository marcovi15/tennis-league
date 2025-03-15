import gspread
import os
import pandas as pd
from google.oauth2.service_account import Credentials
from gspread_dataframe import set_with_dataframe


BASEDIR = os.path.join(os.path.dirname(__file__), '..')
FILE_NAME = "tennis_league"


def connect_to_sheet():

    creds = Credentials.from_service_account_file(os.path.join(BASEDIR, 'data', 'tennis-league-key.json'), scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"])
    client = gspread.authorize(creds)

    return client


def read_sheet(sheet_name):

    client = connect_to_sheet()

    worksheet = client.open(FILE_NAME).worksheet(sheet_name)

    data = worksheet.get_all_records()
    df = pd.DataFrame(data)

    return df


def read_sign_up():
    """
    Reads who signed up for the event.
    """

    sheet_name = "sign_up"

    df = read_sheet(sheet_name)
    if df.empty:
        df = pd.DataFrame(columns=['player', 'playing'])

    return df


def get_players_pool(df):
    """
    Filters for active players and returns a list of these
    :param df:
    :return:
    """
    signed_up_mask = df['playing'].str.match(r'^y', case=False, na=False)
    players_pool = df.loc[signed_up_mask, "player"].to_list()

    return players_pool


def read_latest_results():
    """
    Reads latest results
    :return:
    """

    sheet_name = "match_ups"

    df = read_sheet(sheet_name)

    if df.empty:
        df = pd.DataFrame(columns=['player 1', 'player 2', 'score 1', 'score 2'])

    return df


def read_register():

    sheet_name = "points"
    df = read_sheet(sheet_name)

    return df


def read_all_results():
    """
    Reads archive of results
    :return:
    """

    sheet_name = "past_results"
    df = read_sheet(sheet_name)

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

    df = df.reset_index(drop=True)

    return df, current_week


def read_ranking():

    sheet_name = "ranking"

    df = read_sheet(sheet_name)

    if df.empty:
        df = pd.DataFrame(columns=['player', 'points', 'games_played'])

    return df


def publish_data(df, sheet):

    client = connect_to_sheet()
    worksheet = client.open(FILE_NAME).worksheet(sheet)
    worksheet.clear()

    df_no_index = df.reset_index(drop=True)
    set_with_dataframe(worksheet, df_no_index)


def backup_data(df, file):
    file_path = os.path.join(BASEDIR, 'archive', file)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    df.to_csv(file_path)


def publish_all_tables(publishing_map):

    for sheet, df in publishing_map.items():
        df = df.astype(str)
        publish_data(df, sheet)


def backup_all_tables(publishing_map):
    for file, df in publishing_map.items():
        file_name = file + '.csv'
        df = df.astype(str)
        backup_data(df, file_name)
