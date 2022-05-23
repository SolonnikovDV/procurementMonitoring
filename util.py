import sqlite3

import dash_bootstrap_components
from dash import html

import config as cfg
import base64
from graph_analytic import GraphAnalytic
from my_dash import read_csv_file

# we could add in the func args a tuple with sqlite table fields names
def create_sqlite_table(db_file_name: str):
    conn = sqlite3.connect(db_file_name)
    cur = conn.cursor()
    conn.commit()
    # insert athe tuple here
    cur.execute(f"""CREATE TABLE {cfg.dB_table_name} 
    (
    "№ пп" INTEGER PRIMARY KEY AUTOINCREMENT,
    "Блок, value_stream заказчика" TEXT,
    "Номер закупки" TEXT,
    "Лот закупки" TEXT,
    "Предмет закупки" TEXT,
    "НМЦД" DOUBLE,
    "Предмет жалобы" TEXT,
    "Год решения" DATE,
    "Заявитель" TEXT,
    "Решение по жалобе" TEXT,
    "Нарушенная норма права" TEXT,
    "Комментарий" TEXT,
    "Ссылка на решение ФАС" TEXT
    )""")


def image_to_div(file_name: str):
    encoded_file = base64.b64encode(open(file_name, 'rb').read())
    return html.Img(
        src='data:image/png;base64,{}'.format(encoded_file.decode()),
        style={'width': '30%', 'height': '30%'})


def gif_to_div(gif_name: str):
    pass


def group_data_to_dictionary(data_frame: [], drop_fields: [], filtered_fields: []):
    raw_data = data_frame.drop(drop_fields, axis=1)
    group_data = raw_data.groupby(by=filtered_fields).count()
    group_data = group_data.to_dict('records')
    return group_data


drop = ['№ пп',
                   'Номер закупки',
                   'Лот закупки',
                   'Предмет закупки',
                   'НМЦД',
                   'Предмет жалобы',
                   'Год решения',
                   'Заявитель',
                   'Нарушенная норма права',
                   'Комментарий',
                   'Ссылка на решение ФАС',
                   'Год']
filtered = ['Блок, value_stream заказчика',
                       'Решение по жалобе']
df = read_csv_file()

table = group_data_to_dictionary(df, drop, filtered)
print(table)

if __name__=='__main__':
    print(f'running {__name__}')