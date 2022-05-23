import pandas as pd
import sqlite3
import subprocess
from pathlib import Path
import config as cfg
import re
import openpyxl


class Reports:

    # get excel with all value from DB
    @staticmethod
    def full_report():
        file_name = 'reports/Full_Report.xlsx'
        conn = sqlite3.connect(cfg.db_file_name)
        df = pd.read_sql(f'SELECT * FROM {cfg.dB_table_name}', conn)

        # check for file exists
        if Path(file_name).is_file():
            print(f'File {file_name} is exists')
        else:
            df.to_excel(file_name, index=False)
            print(f'File {file_name} is created')
            subprocess.run(['open', file_name], check=True)

    # report by owner
    @staticmethod
    def owner_report(owner):
        file_name = f'reports/Report_Owner_{owner}.xlsx'
        print(f'Name of owner:  {owner}')

        # set in query owner name
        conn = sqlite3.connect(cfg.db_file_name)
        df = pd.read_sql(f' SELECT * FROM {cfg.dB_table_name} WHERE "Блок, value_stream заказчика"='
                         + '"'
                         + owner
                         + '"',
                         conn)
        if Path(file_name).is_file():
            print(f'File {file_name} is exists')
        else:
            df.to_excel(file_name, index=False)
            print(f'File {file_name} is created')
            subprocess.run(['open', file_name], check=True)

    # report by year
    @staticmethod
    def year_report(year):
        file_name = f'reports/Report_year_{year}.xlsx'
        print(f'Selected year : {year}')

        # set in query owner name
        conn = sqlite3.connect(cfg.db_file_name)
        df = pd.read_sql(
            f'SELECT * FROM {cfg.dB_table_name} WHERE strftime("%Y", "Год решения")='
            + '"'
            + year
            + '"',
            conn)
        if Path(file_name).is_file():
            print(f'File {file_name} is exists')
        else:
            df.to_excel(file_name, index=False)
            print(f'File {file_name} is created')
            subprocess.run(['open', file_name], check=True)

    @staticmethod
    def withdraw_result_report(withdraw_result):
        file_name = f'reports/Report_Owner_{withdraw_result}.xlsx'
        print(f'Name of owner:  {withdraw_result}')

        # set in query owner name
        conn = sqlite3.connect(cfg.db_file_name)
        df = pd.read_sql(f' SELECT * FROM {cfg.dB_table_name} WHERE "Решение по жалобе"='
                         + '"'
                         + withdraw_result
                         + '"',
                         conn)
        if Path(file_name).is_file():
            print(f'File {file_name} is exists')
            subprocess.run(['open', file_name], check=True)
        else:
            df.to_excel(file_name, index=False)
            print(f'File {file_name} is created')
            subprocess.run(['open', file_name], check=True)


    # report by owner
    @staticmethod
    def get_owner_list():
        conn = sqlite3.connect(cfg.db_file_name)
        cursor = conn.cursor()
        cursor.execute(f'SELECT distinct "Блок, value_stream заказчика" FROM {cfg.dB_table_name}')
        data = cursor.fetchall()
        # convert tuple data to string list
        data_str = []
        for row in data:
            # check for None
            if re.sub('[''"{},()]', '', str(row)) != 'None':
                data_str.append(re.sub('[''"{},()]', '', str(row)).split("'")[1])

        print(f'data_string : {data_str}')
        return data_str

    # report by year
    @staticmethod
    def get_year_list():
        conn = sqlite3.connect(cfg.db_file_name)
        cursor = conn.cursor()
        cursor.execute(f'SELECT distinct strftime("%Y", "Год решения") FROM {cfg.dB_table_name}')
        data = cursor.fetchall()
        # convert tuple data to string list
        data_str = []
        for row in data:
            # check for None
            if re.sub('[''"{},()]', '', str(row)) != 'None':
                data_str.append(re.sub('[''"{},()]', '', str(row)).split("'")[1])

        print(f'data_string : {data_str}')
        return data_str

    @staticmethod
    def get_result_list():
        conn = sqlite3.connect(cfg.db_file_name)
        cursor = conn.cursor()
        cursor.execute(f'SELECT distinct "Решение по жалобе" FROM {cfg.dB_table_name}')
        data = cursor.fetchall()
        data_str = []
        for row in data:
            # check for None
            if re.sub('[''"{},()]', '', str(row)) != 'None':
                data_str.append(re.sub('[''"{},()]', '', str(row)).split("'")[1])

        print(f'data_string : {data_str}')
        return data_str
