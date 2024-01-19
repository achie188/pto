import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
import streamlit as st
from gspread_dataframe import set_with_dataframe


sheet_name = "GKL_example"


SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

skey = st.secrets["gsheet_credentials"]
credentials = Credentials.from_service_account_info(
    skey,
    scopes=SCOPES,
)
gc = gspread.authorize(credentials)
sh =  gc.open(sheet_name)




def import_gsheet(sheet):
    wks = sh.worksheet(sheet)
    df = pd.DataFrame(wks.get_all_records())

    return df


def send_to_gsheet(df, sheet):
    wks = sh.worksheet(sheet)
    wks.clear()
    set_with_dataframe(wks, df, include_index=False, include_column_header=True, resize=True)
                        
