import sqlite3
from sqlalchemy import create_engine
import pandas as pd
from datetime import datetime
import config as cfg
import util


# importing data from excel file to sqlite
class ImportDataToDb:
    @classmethod
    def import_data_from_excel(cls, file, db_path, db_table_name):
        #TODO first create table with autoincrement id
        # util.create_sqlite_table(db_table_name)
        df = pd.read_excel(file)
        engine = create_engine(db_path)

        df.to_sql(db_table_name, con=engine, if_exists='replace', index=False)

    # useless function with QTable
    @classmethod
    def insert_variable_into_table(
            cls,
            field_key_autoincrement,
            field_owner,
            field_procurement_number,
            field_procurement_item,
            field_procurement_subject,
            field_procurement_price,
            field_complainant_subject,
            field_complaint_date,
            field_applicant_name,
            field_withdraw_result,
            field_violated_article_of_law,
            field_comment,
            field_href_withdraw_result,
    ):
        try:
            sqlite_connection = sqlite3.connect(cfg.db_file_name)
            cursor = sqlite_connection.cursor()
            print("Connected to SQLite")

            sqlite_insert_with_param = f"""INSERT INTO {cfg.dB_table_name}
                    (
                        '№ пп',
                        'Блок, value_stream заказчика',
                        'Номер закупки',
                        'Лот закупки',
                        'Предмет закупки',
                        'НМЦД',
                        'Предмет жалобы',
                        'Год решения',
                        'Заявитель',
                        'Решение по жалобе',
                        'Нарушенная норма права',
                        'Комментарий',
                        'Ссылка на решение фас'
                    ) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""

            data_tuple = (
                field_key_autoincrement,
                field_owner,
                field_procurement_number,
                field_procurement_item,
                field_procurement_subject,
                field_procurement_price,
                field_complainant_subject,
                datetime.strptime(field_complaint_date, "%d-%m-%Y"),
                field_applicant_name,
                field_withdraw_result,
                field_violated_article_of_law,
                field_comment,
                field_href_withdraw_result
            )
            cursor.execute(sqlite_insert_with_param, data_tuple)
            sqlite_connection.commit()
            print("Python Variables inserted successfully into SqliteDb_developers table")

            cursor.close()

        except sqlite3.Error as error:
            print("Failed to insert Python variable into sqlite table", error)
        finally:
            if sqlite_connection:
                sqlite_connection.close()
                print("The SQLite connection is closed")
