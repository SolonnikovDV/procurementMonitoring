import csv
import logging

import matplotlib
from matplotlib import pyplot as plt
import sqlite3
import pandas as pd
import seaborn as sns
import config as cfg


class GraphAnalytic:

    @staticmethod
    def db_to_csv_one_owner(owner, year):
        conn = sqlite3.connect(cfg.db_file_name)
        cur = conn.cursor()
        print(f'csv input : {owner} , {year}')
        cur.execute(
            'SELECT "Блок, value_stream заказчика", "Год решения", "НМЦД", "Решение по жалобе" '
            'FROM ' + cfg.dB_table_name + ' '
            'WHERE '
            '"Блок, value_stream заказчика"="' + owner + '" '
            'AND '
            'strftime("%Y", "Год решения")="' + year + '"')

        with open('csv_files/One_owner_csv_file.csv', 'w') as csv_file:
            csv_writer = csv.writer(csv_file, dialect='excel')
            csv_writer.writerow([i[0] for i in cur.description])
            csv_writer.writerows(cur)

    @staticmethod
    def db_to_csv_result(year, result):
        conn = sqlite3.connect(cfg.db_file_name)
        cur = conn.cursor()
        print(f'csv input : {year} , {result}')
        cur.execute(
                'SELECT "Блок, value_stream заказчика", "Год решения", "НМЦД", "Решение по жалобе" '
                'FROM ' + cfg.dB_table_name + ' '
                'WHERE '
                '"Решение по жалобе"="' + result + '" '
                'AND '
                'strftime("%Y", "Год решения")="' + year + '"')

        with open('csv_files/Result_csv_file.csv', 'w') as csv_file:
            csv_writer = csv.writer(csv_file, dialect='excel')
            csv_writer.writerow([i[0] for i in cur.description])
            csv_writer.writerows(cur)

    @classmethod
    def db_to_csv(cls):
        conn = sqlite3.connect(cfg.db_file_name)
        cur = conn.cursor()
        cur.execute(f'SELECT * FROM {cfg.dB_table_name}')

        csv_file_name = 'csv_files/Full_csv_file.csv'

        with open(csv_file_name, 'w') as csv_file:
            csv_writer = csv.writer(csv_file, dialect='excel')
            csv_writer.writerow([i[0] for i in cur.description])
            csv_writer.writerows(cur)
        return csv_file_name

    @classmethod
    def graph_one_owner(cls, owner, year):
        # get csv file
        cls.db_to_csv_one_owner(owner, year)
        # data set from csv file with drop nulls
        df = pd.read_csv('csv_files/One_owner_csv_file.csv', sep=',', quotechar='"', parse_dates=['Год решения'])
        # date format from DD-MM-YYYY HH:MM:SS.SSSSSS to YYYY-MM
        cls.date_format(df, 'Год решения', 'Месяц, год приемки')

        # set seaborn style
        sns.set_style('whitegrid')
        # graphic of result of acceptance with total sum on a time line
        g_rel = sns.relplot(x='Год решения', y='НМЦД', size='НМЦД', sizes=(15, 200), hue='Решение по жалобе', data=df)
        # set xlabels orientation
        cls.xticks_label_rotation(g_rel, 45)
        # set left adjust
        plt.subplots_adjust(left=0.10)
        # set title
        g_rel.fig.suptitle(owner)

        # init line plot
        sns.lineplot(x='Год решения', y='НМЦД', hue='Решение по жалобе', data=df, ci='sd', legend=False)
        # set Y axis limits
        try:
            plt.ylim(min(df['НМЦД']), max(df['НМЦД']))
        except ValueError:
            logging.error(cfg.value_error)
            return print(cfg.value_error)
        # set X axis limits
        try:
            plt.xlim(df['Год решения'].iloc[0], df['Год решения'].iloc[-1])
        except IndexError:
            return print('IndexError: single positional indexer is out-of-bounds')
        # set axis format
        plt.gca().get_yaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
        # set Y axis ticks frequency
        plt.gca().get_yaxis().set_major_locator(matplotlib.ticker.MultipleLocator(20000000))

        plt.show()

    @classmethod
    def graph_result(cls, year, result):
        # get csv file
        cls.db_to_csv_result(year, result)
        # data set from csv file with drop nulls
        df = pd.read_csv('csv_files/Result_csv_file.csv', sep=',', quotechar='"', parse_dates=['Год решения'])
        # date format from DD-MM-YYYY HH:MM:SS.SSSSSS to YYYY-MM
        # cls.date_format(df, 'Дата обращения', 'Месяц, год приемки')

        # set seaborn style
        sns.set_style('whitegrid')
        # graphic of result of acceptance with total sum on a time line
        g_rel = sns.relplot(x='Год решения', y='НМЦД', size='НМЦД', hue='Блок, value_stream заказчика', sizes=(15, 200), data=df)
        # set xlabels orientation
        cls.xticks_label_rotation(g_rel, 45)
        # set left adjust
        plt.subplots_adjust(left=0.10)
        # set title
        g_rel.fig.suptitle(result)

        # init line plot
        sns.lineplot(x='Год решения', y='НМЦД', data=df, ci='sd', legend=False)
        # set Y axis limits
        try:
            plt.ylim(min(df['НМЦД']), max(df['НМЦД']))
        except ValueError:
            return print(cfg.value_error)
        # set X axis limits
        try:
            plt.xlim(df['Год решения'].iloc[0], df['Год решения'].iloc[-1])
        except IndexError:
            return print('IndexError: single positional indexer is out-of-bounds')

        # set axis format
        plt.gca().get_yaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
        # set Y axis ticks frequency
        plt.gca().get_yaxis().set_major_locator(matplotlib.ticker.MultipleLocator(20000000))

        plt.show()

    @classmethod
    def graph_all_owners(cls):
        # get csv file
        cls.db_to_csv()
        # data set from csv file with drop nulls
        df = pd.read_csv('csv_files/Full_csv_file.csv',
                         sep=',',
                         quotechar='"',
                         parse_dates=['Год решения'])
        # date format from DD-MM-YYYY HH:MM:SS.SSSSSS to YYYY-MM
        cls.date_format(df, 'Год решения', 'Месяц, год приемки')

        # seaborn style
        sns.set_style('whitegrid')
        # graphic of result of acceptance with total sum on a time line
        g_rel = sns.relplot(x='Год решения',
                            y='НМЦД',
                            size='НМЦД',
                            sizes=(15, 200),
                            hue='Блок, value_stream заказчика',
                            col='Решение по жалобе',
                            legend='brief',
                            data=df)

        # set xlabels orientation
        cls.xticks_label_rotation(g_rel, 45)
        # set left adjust
        plt.subplots_adjust(left=0.09)

        # set Y axis limits
        plt.ylim(min(df['НМЦД']),
                 max(df['НМЦД']))
        # set X axis limits
        print(f'{df["Год решения"]}')
        
        plt.xlim(df['Год решения'].iloc[0],
                 df['Год решения'].iloc[-1])
        # set axis format
        plt.gca().get_yaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
        # set Y axis ticks frequency
        plt.gca().get_yaxis().set_major_locator(matplotlib.ticker.MultipleLocator(20000000))

        plt.show()

    @classmethod
    def date_format(cls, data_frame, column_name, new_column_name):
        data_frame[new_column_name] = data_frame[column_name].dt.strftime('%Y-%m')

    @classmethod
    def xticks_label_rotation(cls, plot_name, value):
        for axis in plot_name.axes.flat:
            for label in axis.get_xticklabels():
                label.set_rotation(value)
