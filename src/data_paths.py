import gspread
import os
import pandas as pd
from google.oauth2.service_account import Credentials


BASEDIR = os.path.dirname(__file__)

def read_sign_up():
    """
    Reads who signed up for the event.
    """
    creds = Credentials.from_service_account_file(os.path.join(BASEDIR, '..', 'data', 'tennis-league-key.json'), scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"])
    client = gspread.authorize(creds)

    spreadsheet = client.open("sign_up_form")  # Change to your sheet name
    worksheet = spreadsheet.sheet1

    data = worksheet.get_all_records()
    df = pd.DataFrame(data)

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

