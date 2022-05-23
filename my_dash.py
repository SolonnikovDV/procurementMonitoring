import logging
import webbrowser
from functools import lru_cache

import component as component
import dash
import gif as gif
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.io as poi
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_gif_component as gif
from dash import dash_table

# local import
from dash.exceptions import CallbackException

import util
from graph_analytic import GraphAnalytic
import config as cfg
import my_test

logging.basicConfig(level=logging.DEBUG,
                    filename="mylog.log",
                    format="%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
                    datefmt='%H:%M:%S'
                    )

poi.renderers.default = 'browser'
# LUX themes
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY])


# refresh csv every time when dash starts and return data frame
@lru_cache(maxsize=200)
def read_csv_file():
    csv_file = GraphAnalytic.db_to_csv()
    df = pd.read_csv(csv_file, parse_dates=['Год решения'])
    df['Год'] = df['Год решения'].dt.strftime('%Y')
    return df


# preparing data for dropdown menu : names for menu + new field in data frame
def price_selector_list(df: []):
    bins = [1 * 10 ** 6, 100 * 10 ** 6, 200 * 10 ** 6, 300 * 10 ** 6, 400 * 10 ** 6, 500 * 10 ** 6, 600 * 10 ** 6,
            max(df['НМЦД']) - 1]
    names = ['от 1 млн', 'от 100 млн', 'от 200 млн', 'от 300 млн', 'от 400 млн', 'от 500 млн', 'от 600 млн']
    df['price_selector'] = pd.cut(df['НМЦД'], bins, labels=names)

    options = []
    for k in names:
        options.append({'label': k, 'value': k})
    arr = [df, options]

    return arr


# dropdown menu
def price_selector(df: []):
    options = price_selector_list(df)[1]
    selector = dcc.Dropdown(
        id='id_price_selector',
        options=options,
        value=['от 1 млн', 'от 100 млн', 'от 200 млн', 'от 300 млн', 'от 400 млн', 'от 500 млн', 'от 600 млн'],
        multi=True
    )
    return selector


# slider selector design
def slider_selector(df: []):
    slider = dcc.RangeSlider(
        id='id_price_slider',
        min=min(df['НМЦД']),
        max=max(df['НМЦД']),
        marks={1 * 10 ** 6: '1', 100 * 10 ** 6: '100', 200 * 10 ** 6: '200', 300 * 10 ** 6: '300', 400 * 10 ** 6: '400',
               500 * 10 ** 6: '500',
               600 * 10 ** 6: '600', max(df['НМЦД']) - 1: 'MAX'},
        step=10 ** 6,
        value=[min(df['НМЦД']), max(df['НМЦД'])]
    )
    return slider


# filter
@app.callback(
    [Output(component_id='id_price_dash_layout', component_property='children'),
     Output(component_id='time_line_plot', component_property='children'),
     Output(component_id='id_owner_withdraw_timeline', component_property='children'),
     Output(component_id='id_owner_timeline_price', component_property='children'),
     Output(component_id='id_table_content_short', component_property='children'),
     Output(component_id='id_table_content', component_property='children')],
    [Input(component_id='id_price_slider', component_property='value'),
     Input(component_id='id_price_selector', component_property='value')]
)
def update_plots(price_slider_var, price_selector_var):
    df = price_selector_list(read_csv_file())[0]
    data = df[
        (df['НМЦД'] > price_slider_var[0]) &
        (df['НМЦД'] < price_slider_var[1]) &
        (df['price_selector'].isin(price_selector_var))
        ]

    # check for empty data
    if len(data) == 0:
        return html.Div(dbc.Row(
            [
                dbc.Col([
                    html.Div("Choose any values in the filters"),
                    util.image_to_div('images/cancel.png')
                    # gif.GifPlayer(gif='images/weeds.gif', still='images/cancel.png')
                ], style={'width': '30%', 'height': '30%'})
            ], style={'text-align': 'center'})
        ), html.Div(), html.Div(), html.Div(), html.Div(), html.Div()

    # build figure
    fig1 = px.scatter(data,
                      x='Решение по жалобе',
                      y='НМЦД',
                      color='price_selector')
    html1 = [html.Div('Dashboard of procurement monitoring'), dcc.Graph(figure=fig1)]

    fig2 = px.scatter(data,
                      x='Год решения',
                      y='НМЦД',
                      size='НМЦД',
                      color="Решение по жалобе")
    html2 = [html.Div('Time line'), dcc.Graph(figure=fig2)]

    fig3 = px.ecdf(data,
                   x='НМЦД',
                   facet_row='Год',
                   facet_col='Решение по жалобе',
                   color='Блок, value_stream заказчика',
                   markers=True,
                   marginal='histogram')
    html3 = [html.Div('Owner + withdraw + timeline'), dcc.Graph(figure=fig3)]

    fig4 = px.strip(data,
                    x='НМЦД',
                    y='Год решения',
                    facet_col='Решение по жалобе',
                    color='Блок, value_stream заказчика')
    html4 = [html.Div('Owner + timeline + price'), dcc.Graph(figure=fig4)]

    html5 = [html.P('Short result'), my_test.tab_data_table_short()]
    html6 = [html.P('Monitoring results table'), tab_data_table(df=read_csv_file())]

    return html1, html2, html3, html4, html5, html6


def init_dash(df: []):
    slider = slider_selector(df)
    selector = price_selector(df)
    app.layout = html.Div(
        [
            # header
            dbc.Row([
                html.H1('Procurement Monitoring Dashboard'),
                html.Hr()
            ], style={'margin-bottom': '40px', 'text-align': 'center'}),
            # filters
            dbc.Row([
                # slider selector
                dbc.Col([
                    html.Div('Price slider selector (million, RUR)'),
                    html.Div(slider),
                ], width={'size': 6}),
                # dropdown selector
                dbc.Col([
                    html.Div('Price dropdown menu selector'),
                    html.Div(selector),
                ], width={'size': 6, 'offset': 0.5})
            ], style={'margin-bottom': '40px'}),
            # plots
            dbc.Tabs([
                dbc.Tab(tab_figures(), label='Figures'),
                dbc.Tab([
                    dbc.Row([
                        html.Div(id='id_table_content_short')
                    ]),
                    dbc.Row([
                        html.Div(id='id_table_content')])
                ], label='Tables'),
                dbc.Tab([
                    dbc.Row(
                        html.A('All data we used in dashboard was taken from here', href='https://br.fas.gov.ru/')
                    )], label='About')
            ])
        ],
        style={'margin-left': '80px', 'margin-right': '80px'}
    )


def tab_figures():
    # tab 1
    figures = [dbc.Row([
        # fig1
        dbc.Col([
            html.Div(id='id_price_dash_layout')
        ], width={'size': 6}),
        # fig2
        dbc.Col([
            html.Div(id='time_line_plot')
        ], width={'size': 6})
    ], style={'text-align': 'center'}),
        dbc.Row([
            # fig 3
            dbc.Col(
                html.Div('Owner + withdraw + timeline', id='id_owner_withdraw_timeline'),
                width={'size': 12}),
            # fig 4
            dbc.Col(
                html.Div('Owner + timeline + price', id='id_owner_timeline_price'),
                width={'size': 12})
        ])]
    return figures


def tab_data_table(df: []):
    # tab 2
    data = df.drop(['price_selector', 'Лот закупки', 'Нарушенная норма права', 'Комментарий', 'Год решения'], axis=1)
    data_table = dash_table.DataTable(id='id_table_content',
                                      data=data.to_dict('records'),
                                      columns=[{'name': i, 'id': i} for i in data.columns],
                                      style_data={'width': '100px}', 'maxWidth': '100px', 'minWidth': '100px'},
                                      style_header={'textAlign': 'center'})
    return data_table


def tab_data_table_short(df: []):
    # tab 2
    drop_fields = ['№ пп',
                   'Номер закупки',
                   'Лот закупки',
                   'Предмет закупки',
                   'НМЦД',
                   'Предмет жалобы',
                   'Год решения',
                   'Заявитель',
                   'Нарушенная норма права',
                   'Комментарий',
                   'Ссылка на решение ФАС']
    data_drop = df.drop(drop_fields, axis=1)
    data_group = df.groupby(['Блок, value_stream заказчика', 'Решение по жалобе'])\
        .agg({'Решение по жалобе': 'count', 'НМЦД': 'sum'})

    # data_group = pd.pivot_table(data_drop,
    #                             index=['Блок, value_stream заказчика'],
    #                             # values=['НМЦД'],
    #                             columns=['Решение по жалобе'],
    #                             aggfunc=[len])
    data_table = dash_table.DataTable(id='id_table_content_short',
                                      data=data_group.to_dict('records'),
                                      columns=[{'name': i, 'id': i} for i in data_group.columns],
                                      style_data={'width': '10px}', 'maxWidth': '10px', 'minWidth': '10px'},
                                      style_header={'textAlign': 'center'})
    return data_table


init_dash(read_csv_file())

webbrowser.open(cfg.dev_server_link, new=2)
if __name__ == '__main__':
    # TODO try to run app on public hosting
    # host = 'public_html'
    app.run_server(debug=True)
    logging.info(f'start server at http://127.0.0.1:8050')
