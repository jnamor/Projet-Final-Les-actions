import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import pymysql
from secrets import ACCESS_DB
import plotly.graph_objects as go
import dash_table

# Connection à l'instance de database
def connect_to_instance_db():
    try:
        conn = pymysql.connect(
                host='db-company.cwm601wtiqo3.eu-west-3.rds.amazonaws.com',
                user='admin',
                password=ACCESS_DB,
                charset='utf8mb4')
    except pymysql.err.OperationalError as e:
        raise e
    else:
        print("Connection Successful!")
    return conn

connection = connect_to_instance_db()
cursor = connection.cursor()
query = "USE db_company"
cursor.execute(query)
connection.commit()

# Application dash
app = dash.Dash(__name__, suppress_callback_exceptions=True, title='Analytics', update_title=None)

def get_capital(df, inv=1000):
    liste = []

    index = 0
    variable = inv
    variable2 = inv
    variable3 = inv
    variable4 = inv
    variable5 = inv
    variable6 = inv
    variable7 = inv
    variable8 = inv
    variable9 = inv

    z = 'name'
    for i in df[z]:
        if i == 'Margaret Peacock':
            variable += df.loc[df[z] == i, 'amount'][index]
            liste.append(variable)
            index += 1
            
        elif i == 'Andrew Fuller':
            variable2 += df.loc[df[z] == i, 'amount'][index]
            liste.append(variable2)
            index += 1
            
        elif i == 'Laura Callahan':
            variable3 += df.loc[df[z] == i, 'amount'][index]
            liste.append(variable3)
            index += 1
            
        elif i == 'Anne Dodsworth':
            variable4 += df.loc[df[z] == i, 'amount'][index]
            liste.append(variable4)
            index += 1
            
        elif i == 'Steven Buchanan':
            variable5 += df.loc[df[z] == i, 'amount'][index]
            liste.append(variable5)
            index += 1
            
        elif i == 'Janet Leverling':
            variable6 += df.loc[df[z] == i, 'amount'][index]
            liste.append(variable6)
            index += 1
            
        elif i == 'Nancy Davolio':
            variable7 += df.loc[df[z] == i, 'amount'][index]
            liste.append(variable7)
            index += 1
        
        elif i == 'Michael Suyama':
            variable8 += df.loc[df[z] == i, 'amount'][index]
            liste.append(variable8)
            index += 1
            
        elif i == 'Robert King':
            variable9 += df.loc[df[z] == i, 'amount'][index]
            liste.append(variable9)
            index += 1
    
    df['capital'] = liste

    return df

def get_bar(df, x, y):
    fig = go.Figure()
    if y == 'employees_k':
        fig.add_trace(go.Bar(x=df[y], y=df[x], text=df[y].map('{:.2f}'.format), orientation='h'))
    else:
        fig.add_trace(go.Bar(x=df[y], y=df[x], text=df[y].map('${:.2f}'.format), orientation='h'))

    fig.update_layout(margin=dict(l=10, r=10, t=10, b=10),
                    template="plotly_white",
                    showlegend=False,
                    barmode='group',
                    yaxis={'categoryorder':'total ascending'},
                    uniformtext_minsize=8, 
                    uniformtext_mode='hide',
                    xaxis_title=None,
                    yaxis_title=None
                    )

    fig.update_traces(textposition='outside')
    return fig

def get_multi_pie(df, x, z):
    fig = go.Figure()

    variable = 0
    for column in df.columns.to_list():
        df = df.sort_values(column, ascending=False).head(5)
        if variable == 0:
            variable += 1
            fig.add_trace(
                go.Pie(labels=df[x], values=df[column], name=column, textinfo='label+percent', hole=.3)
            )
        else:
            fig.add_trace(
                go.Pie(labels=df[x], values=df[column], name=column, textinfo='label+percent', hole=.3, visible=False)
            )

    def create_layout_button(column):
        return dict(label = column.capitalize().replace('_',' '),
                    method = 'update',
                    args = [{'visible': df.columns.isin([column]),
                             'showlegend': True}])

    fig.update_traces(marker=dict(line=dict(color='#FFFFFF', width=2)))
    fig.update_layout(
        margin=dict(l=10, r=10, t=10, b=10), 
        showlegend=False,
        updatemenus=[
            go.layout.Updatemenu(
                active = 0,
                buttons = list(df.loc[:, :z].columns.map(lambda column: create_layout_button(column))),
                direction="down", x=0, y=1.2, xanchor="left", yanchor="top"
            )
        ])
    
    return fig

def get_multi_bar(df, x, z):
    fig = go.Figure()

    variable = 0
    for column in df.loc[:, :z].columns.to_list():
        if column == 'employees_k':
            variable += 1
            fig.add_trace(
                go.Bar(x=df[x], y=df[column], name=column.capitalize().replace('_',' '), text=df[column].map('{:.1f}'.format))
            )
        else:
            variable += 1
            fig.add_trace(
                go.Bar(x=df[x], y=df[column], name=column.capitalize().replace('_',' '), text=df[column].map('${:.1f}'.format))
            )

    if variable > 2:
        l = True
    else:
        l = False

    fig.update_traces(textposition='outside')
    fig.update_layout(
            margin=dict(l=10, r=10, t=10, b=10), 
            template="plotly_white",
            showlegend=l,
            legend=dict(
                orientation="h",
                xanchor="right", yanchor="bottom", x=1, y=1.02
            ),
            barmode='group',
            yaxis={'categoryorder':'total descending'},
            uniformtext_minsize=8, 
            uniformtext_mode='hide',
        )

    return fig

def get_multi_scatter(df, z):
    fig = go.Figure()

    for i in list(reversed(df[z].unique())):
        test = df[df[z] == i]
        variable = 0
        for j in df.loc[:, 'opens':'volumes'].columns.to_list():
            if variable == 0:
                variable += 1
                fig.add_traces(go.Scatter(x=test['times'], y = test[j],
                                          mode='lines',
                                          opacity=0.7,
                                          name=i,
                                          textposition='bottom center'))
            else:
                fig.add_traces(go.Scatter(x=test['times'], y = test[j], 
                                          mode='lines',
                                          opacity=0.7,
                                          name=i,
                                          textposition='bottom center',
                                          visible=False))

    def create_layout_button(column):
        return dict(label = column.capitalize().replace('_',' '),
                    method = 'update',
                    args = [{'visible': df.loc[:, 'opens':'volumes'].columns.isin([column]),
                             'showlegend': True}])    

    fig.update_layout(margin=dict(l=10, r=10, t=10, b=10),
                    template="plotly_white",
                    showlegend=True,
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1),
                    xaxis_title=None,
                    yaxis_title=None,
                    updatemenus=[
                        go.layout.Updatemenu(
                            active = 0,
                            buttons = list(df.loc[:, 'opens':'volumes'].columns.map(lambda column: create_layout_button(column))),
                            direction="down", x=0, y=1.2, xanchor="left", yanchor="top"
                        )
                    ])

    return fig

def get_data_from_sql(query):
    # Set SQL query as a comment / Use pandas to pass sql query using connection form SQLite3
    df = pd.read_sql(query, connection)

    # Show the resulting DataFrame
    return df

df_investors = get_data_from_sql(
    ''' SELECT times, amount, O.id_investor, CONCAT(first_name, " ", last_name) as name
            FROM orders O
                LEFT JOIN investor I ON O.id_investor = I.id_investor
            WHERE id_type = 1
            ORDER BY times ASC; ''')

def tab_portfolio():
    return html.Div(
            className="twelve columns dashboard_panel",
            children=[
                html.Div(
                    className="row chart_position",
                    children = [
                        html.Div(
                            className="row",
                            children=[
                                dcc.Dropdown(
                                    id="markets",
                                    className="two columns dropdown_menu",
                                    options=[{'label': i, 'value': i} for i in df_investors['name'].unique()],
                                    value=[df_investors['name'].sort_values()[0]],
                                    clearable=False,
                                    multi=True
                                ),
                            ],
                        ),
                        html.Div(
                            className="twelve columns chart_div",
                            children=[
                                html.P("Suivi du capital de l'investisseur"),
                                dcc.Graph(
                                    id="graph-figure-capital",
                                    style={"height": "85%", "width": "100%"},
                                    config=dict(displayModeBar=False),
                                )
                            ]
                        )
                    ]
                ),
                html.Div(
                    className="row chart_position",
                    children = [
                        html.Div(
                            className="nine columns volume_div",
                            children=[
                                html.P("Performance des investisseurs"),
                                dcc.Graph(
                                    id="map",
                                    style={"height": "81%", "width": "100%"},
                                    config=dict(displayModeBar=False),
                                    figure=get_bar(
                                        get_data_from_sql(
                                            ''' SELECT times, amount, O.id_investor, CONCAT(first_name, " ", last_name) as name
                                                FROM orders O
                                                    LEFT JOIN investor I ON O.id_investor = I.id_investor
                                                WHERE id_type = 1
                                                ORDER BY times ASC; '''
                                        ).groupby('name', as_index=False).sum()[['name', 'amount']].sort_values('amount')
                                        ,  'name', 'amount'
                                    )
                                ),
                            ],
                        ),
                        html.Div(
                            className="three columns volume_div",
                            children=[
                                html.P("Performance par pays"),
                                dcc.Graph(
                                    id="pie",
                                    style={"height": "81%", "width": "100%"},
                                    config=dict(displayModeBar=False),
                                    figure=get_multi_bar(
                                        get_data_from_sql(
                                            ''' SELECT SUM(amount) AS amount, 
                                                id_area
                                            FROM orders O
                                                LEFT JOIN investor I ON O.id_investor = I.id_investor
                                            WHERE id_type = 1
                                            GROUP BY id_area ; '''
                                        ),  'id_area', 'amount'
                                    )
                                )
                            ]
                        )
                    ]
                )
            ]
        )

def get_dataframe(df):
    return dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        filter_action="native",
        sort_action="native",
        page_action="native",
        page_current= 0,
        page_size= 15
    )

def tab_action():
    return html.Div(
            className="twelve columns dashboard_panel",
            children=[
                html.Div(
                    className="row chart_position",
                    children = [
                        html.Div(
                            className="twelve columns",
                            children=[
                                get_dataframe(
                                    get_data_from_sql(
                                        ''' SELECT times, closes AS last_price, 
                                            operating_income, net_income, total_assets, total_equity, CAST(employees_k AS FLOAT) AS employees_k, market_cap,
                                            C.id_company, company, sector, area
                                            FROM market_value M
                                                LEFT JOIN company C ON C.id_company = M.id_company
                                                LEFT JOIN sector S ON S.id_sector = C.id_sector
                                                LEFT JOIN area A ON A.id_area = C.id_area
                                            WHERE id_info IN (
                                                SELECT MAX(id_info)
                                                FROM market_value
                                                GROUP BY id_company)'''
                                    )
                                )
                            ]
                        )
                    ]
                ),
                html.Div(
                    className="row chart_position",
                    children = [
                        html.Div(
                            className="four columns volume_div",
                            children=[
                                html.P("Entreprises comptant la capitalisation boursière la plus élevée"),
                                dcc.Graph(
                                    id="live-update-graph",
                                    style={"height": "91%", "width": "100%"},
                                    config=dict(displayModeBar=False, scrollZoom= False),
                                    figure=get_bar(
                                        get_data_from_sql(
                                            ''' SELECT id_company, market_cap FROM company ORDER BY market_cap DESC LIMIT 10;'''
                                        ), 'id_company', 'market_cap'
                                    )
                                )
                            ]
                        ),
                        html.Div(
                            className="four columns volume_div",
                            children=[
                                html.P("Entreprises comptant le chiffre d'affaire le plus élevé"),
                                dcc.Graph(
                                    id="live-update-graph",
                                    style={"height": "91%", "width": "100%"},
                                    config=dict(displayModeBar=False, scrollZoom= False),
                                    figure=get_bar(
                                        get_data_from_sql(
                                            ''' SELECT id_company, revenue FROM company ORDER BY revenue DESC LIMIT 10;'''
                                        ), 'id_company', 'revenue'
                                    )
                                )
                            ]
                        ),
                        html.Div(
                            className="four columns volume_div",
                            children=[
                                html.P("Entreprises comptant le plus d'employés"),
                                dcc.Graph(
                                    id="live-update-graph",
                                    style={"height": "91%", "width": "100%"},
                                    config=dict(displayModeBar=False, scrollZoom= False),
                                    figure=get_bar(
                                        get_data_from_sql(
                                        ''' SELECT id_company, employees_k FROM company ORDER BY employees_k DESC LIMIT 10;'''
                                        ), 'id_company', 'employees_k'
                                    )
                                )
                            ]
                        )
                    ],
                ),
            ]
        )

def tab_entreprise():
    return html.Div(
            className="twelve columns dashboard_panel",
            children=[
                html.Div(
                    className="row chart_position",
                    children = [
                        html.Div(
                            className="four columns chart_div",
                            children=[
                                html.P(id="market_title"),
                                dcc.Graph(
                                    id="live-update-graph",
                                    style={"height": "91%", "width": "100%"},
                                    config=dict(displayModeBar=False, scrollZoom= False),
                                    figure=get_multi_bar(
                                        get_data_from_sql(
                                            ''' SELECT SUM(revenue) as revenue, 
                                                    SUM(employees_k) as employees_k, 
                                                    SUM(market_cap) as market_cap, 
                                                    id_area
                                                FROM company
                                                GROUP BY id_area 
                                                ORDER BY market_cap DESC; '''
                                        ),  'id_area', 'market_cap'
                                    )
                                )
                            ]
                        ),
                        html.Div(
                            className="four columns chart_div",
                            children=[
                                html.P(id="market_title"),
                                dcc.Graph(
                                    id="live-update-graph",
                                    style={"height": "91%", "width": "100%"},
                                    config=dict(displayModeBar=False, scrollZoom= False),
                                    figure=get_multi_pie(
                                        get_data_from_sql(
                                            ''' SELECT SUM(operating_income) as operating_income, 
                                                    SUM(net_income) as net_income, 
                                                    SUM(total_assets) as total_assets, 
                                                    SUM(total_equity) as total_equity, 
                                                    SUM(market_cap) as market_cap, 
                                                    id_area
                                                FROM company
                                                GROUP BY id_area; '''
                                        ), 'id_area', 'total_equity'
                                    )
                                )
                            ]
                        ),
                        html.Div(
                            className="four columns chart_div",
                            children=[
                                html.P(""),
                                dcc.Graph(
                                    id="live-update-graph",
                                    style={"height": "91%", "width": "100%"},
                                    config=dict(displayModeBar=False, scrollZoom= False),
                                    figure=get_multi_scatter(
                                        get_data_from_sql(
                                            ''' SELECT times, AVG(opens) AS opens, AVG(closes) AS closes, AVG(highs) AS highs, AVG(lows) AS lows, AVG(volumes) AS volumes, id_area
                                                FROM market_value M
                                                    LEFT JOIN company C ON C.id_company = M.id_company
                                                GROUP BY times, id_area
                                                ORDER BY times ASC; '''
                                        ), 'id_area'
                                    )
                                )
                            ]
                        )
                    ]
                ),
                html.Div(
                    className="row chart_position",
                    children = [
                        html.Div(
                            className="four columns volume_div",
                            children=[
                                html.P("Entreprises comptant la capitalisation boursière la plus élevée"),
                                dcc.Graph(
                                    id="live-update-graph",
                                    style={"height": "91%", "width": "100%"},
                                    config=dict(displayModeBar=False, scrollZoom= False),
                                    figure=get_bar(
                                        get_data_from_sql(
                                            ''' SELECT id_area, SUM(market_cap) AS market_cap
                                                FROM company
                                                GROUP BY id_area
                                                ORDER BY market_cap DESC 
                                                LIMIT 10;'''
                                        ), 'id_area', 'market_cap'
                                    )
                                )
                            ]
                        ),
                        html.Div(
                            className="four columns volume_div",
                            children=[
                                html.P("Entreprises comptant le chiffre d'affaire le plus élevé"),
                                dcc.Graph(
                                    id="live-update-graph",
                                    style={"height": "91%", "width": "100%"},
                                    config=dict(displayModeBar=False, scrollZoom= False),
                                    figure=get_bar(
                                        get_data_from_sql(
                                            ''' SELECT id_area, SUM(revenue) AS revenue
                                                FROM company
                                                GROUP BY id_area
                                                ORDER BY revenue DESC 
                                                LIMIT 10;'''
                                        ), 'id_area', 'revenue'
                                    )
                                )
                            ]
                        ),
                        html.Div(
                            className="four columns volume_div",
                            children=[
                                html.P("Entreprises comptant le plus d'employés"),
                                dcc.Graph(
                                    id="live-update-graph",
                                    style={"height": "91%", "width": "100%"},
                                    config=dict(displayModeBar=False, scrollZoom= False),
                                    figure=get_bar(
                                        get_data_from_sql(
                                            ''' SELECT id_area, SUM(employees_k) AS employees_k
                                                FROM company
                                                GROUP BY id_area
                                                ORDER BY employees_k DESC 
                                                LIMIT 10;'''
                                        ), 'id_area', 'employees_k'
                                    )
                                )
                            ]
                        )
                    ],
                ),
            ]
        )

def tab_entreprise2():
    return html.Div(
            className="twelve columns dashboard_panel",
            children=[
                html.Div(
                    className="row chart_position",
                    children = [
                        html.Div(
                            className="four columns chart_div",
                            children=[
                                html.P(""),
                                dcc.Graph(
                                    id="live-update-graph",
                                    style={"height": "91%", "width": "100%"},
                                    config=dict(displayModeBar=False, scrollZoom= False),
                                    figure=get_multi_bar(
                                        get_data_from_sql(
                                            ''' SELECT SUM(revenue) as revenue, 
                                                    SUM(employees_k) as employees_k, 
                                                    SUM(market_cap) as market_cap,
                                                    C.id_sector,
                                                    sector
                                                FROM company C
                                                    LEFT JOIN sector S ON C.id_sector = S.id_sector
                                                GROUP BY id_sector 
                                                ORDER BY market_cap DESC
                                                LIMIT 5; '''
                                        ),  'sector', 'market_cap'
                                    )
                                )
                            ]
                        ),
                        html.Div(
                            className="four columns chart_div",
                            children=[
                                html.P(""),
                                dcc.Graph(
                                    id="live-update-graph",
                                    style={"height": "91%", "width": "100%"},
                                    config=dict(displayModeBar=False, scrollZoom= False),
                                    figure=get_multi_pie(
                                        get_data_from_sql(
                                            ''' SELECT SUM(operating_income) as operating_income, 
                                                    SUM(net_income) as net_income, 
                                                    SUM(total_assets) as total_assets, 
                                                    SUM(total_equity) as total_equity, 
                                                    C.id_sector,
                                                    sector
                                                FROM company C
                                                    LEFT JOIN sector S ON C.id_sector = S.id_sector
                                                GROUP BY id_sector; '''
                                        ),  'sector', 'total_equity'
                                    )
                                )
                            ]
                        ),
                        html.Div(
                            className="four columns chart_div",
                            children=[
                                html.P(""),
                                dcc.Graph(
                                    id="live-update-graph",
                                    style={"height": "91%", "width": "100%"},
                                    config=dict(displayModeBar=False, scrollZoom= False),
                                    figure=get_multi_scatter(
                                        get_data_from_sql(
                                            ''' SELECT times, AVG(opens) AS opens, AVG(closes) AS closes, AVG(highs) AS highs, AVG(lows) AS lows, AVG(volumes) AS volumes, sector
                                                FROM market_value M
                                                    LEFT JOIN company C ON C.id_company = M.id_company
                                                    LEFT JOIN sector S ON C.id_sector = S.id_sector
                                                WHERE sector IN ('Technology', 'Healthcare', 'Consumer Staples', 'Financials', 'Consumer Discretionary')
                                                GROUP BY times, sector
                                                ORDER BY times ASC; '''
                                        ), 'sector'
                                    )
                                )
                            ]
                        )
                    ]
                ),
                html.Div(
                    className="row chart_position",
                    children = [
                        html.Div(
                            className="four columns volume_div",
                            children=[
                                html.P("Secteurs comptant la capitalisation boursière la plus élevée"),
                                dcc.Graph(
                                    id="live-update-graph",
                                    style={"height": "91%", "width": "100%"},
                                    config=dict(displayModeBar=False, scrollZoom= False),
                                    figure=get_bar(
                                        get_data_from_sql(
                                            ''' SELECT SUM(market_cap) as market_cap,
                                                C.id_sector,
                                                sector
                                            FROM company C
                                                LEFT JOIN sector S ON C.id_sector = S.id_sector
                                            GROUP BY id_sector 
                                            ORDER BY market_cap DESC
                                            LIMIT 10;'''
                                        ), 'sector', 'market_cap'
                                    )
                                )
                            ]
                        ),
                        html.Div(
                            className="four columns volume_div",
                            children=[
                                html.P("Secteurs comptant le chiffre d'affaire le plus élevé"),
                                dcc.Graph(
                                    id="live-update-graph",
                                    style={"height": "91%", "width": "100%"},
                                    config=dict(displayModeBar=False, scrollZoom= False),
                                    figure=get_bar(
                                        get_data_from_sql(
                                            ''' SELECT SUM(revenue) as revenue,
                                                C.id_sector,
                                                S.sector
                                            FROM company C
                                                LEFT JOIN sector S ON C.id_sector = S.id_sector
                                            GROUP BY id_sector 
                                            ORDER BY revenue DESC
                                            LIMIT 10;'''
                                        ), 'sector', 'revenue'
                                    )
                                )
                            ]
                        ),
                        html.Div(
                            className="four columns volume_div",
                            children=[
                                html.P("Secteurs comptant le nombre d'employé le plus élevé"),
                                dcc.Graph(
                                    id="live-update-graph",
                                    style={"height": "91%", "width": "100%"},
                                    config=dict(displayModeBar=False, scrollZoom= False),
                                    figure=get_bar(
                                        get_data_from_sql(
                                            ''' SELECT SUM(employees_k) as employees_k,
                                                C.id_sector,
                                                S.sector
                                            FROM company C
                                                LEFT JOIN sector S ON C.id_sector = S.id_sector
                                            GROUP BY id_sector 
                                            ORDER BY employees_k DESC
                                            LIMIT 10;'''
                                        ), 'sector', 'employees_k'
                                    )
                                )
                            ]
                        )
                    ],
                ),
            ]
        )

df = get_data_from_sql(
    ''' SELECT times, opens, closes, highs, lows, volumes, company 
        FROM market_value M
            LEFT JOIN company C ON C.id_company = M.id_company; '''
    )

def tab_trading():
    return html.Div(
            className="twelve columns dashboard_panel",
            children=[
                html.Div(
                    className="row",
                    children=[
                        dcc.Dropdown(
                            id="markets",
                            className="two columns dropdown_menu",
                            options=[{'label': i, 'value': i} for i in df['company'].unique()],
                            value=[df['company'].sort_values()[0]],
                            clearable=False,
                            multi=True
                        ),
                    ],
                ),
                html.Div(
                    className="row chart_position",
                    children = [
                        html.Div(
                            className="twelve columns chart_div",
                            children=[
                                html.P("Cours du marché"),
                                dcc.Graph(
                                    id="live-update-graph",
                                    style={"height": "91%", "width": "100%"},
                                    config=dict(displayModeBar=False, scrollZoom= False)
                                ),
                            ],
                        )
                    ]
                ),
                html.Div(
                    className="row chart_position",
                    children = [
                        html.Div(
                            className="twelve columns volume_div",
                            children=[
                                html.P("Volume"),
                                dcc.Graph(
                                    id="live-update-graph-volume",
                                    style={"height": "81%", "width": "100%"},
                                    config=dict(displayModeBar=False)
                                ),
                            ],
                        )
                    ]
                )
            ]
        )


app.layout = html.Div(
    className="row",
    children=[
        html.Div(
            className="row tabs_div",
            children=[
                dcc.Tabs(
                    id="tabs",
                    style={"height":"20","verticalAlign":"middle"},
                    children=[
                        dcc.Tab(label="Cours", value="trading_tab"),
                        dcc.Tab(label="Portfolio", value="portfolio_tab"),
                        dcc.Tab(label="Action", value="tab_action"),
                        dcc.Tab(label="Pays", value="entreprise_tab"),
                        dcc.Tab(label="Secteurs", value="entreprise_tab2")

                    ],
                    value="trading_tab"
                )
            ],
        ),
        html.Div(id="tab_content", className="row"),
    ]
)

@app.callback(
    Output("tab_content", "children"), 
    [Input("tabs", "value")])
def render_content(tab):
    if tab == "trading_tab":
        return tab_trading()
    elif tab == "tab_action":
        return tab_action()
    elif tab == "entreprise_tab":
        return tab_entreprise()
    elif tab == "entreprise_tab2":
        return tab_entreprise2()
    elif tab == "portfolio_tab":
        return tab_portfolio()
    else:
        return tab_trading()

@app.callback(Output('live-update-graph', 'figure'),
              [Input('markets', 'value')])
def update_timeseries(selected_dropdown_value):
    ''' Draw traces of the feature 'value' based one the currently selected stocks '''
    # STEP 1
    trace = []  
    df_sub = df
    # STEP 2
    # Draw and append traces for each stock
    for stock in selected_dropdown_value:   
        trace.append(go.Scatter(x=df_sub[df_sub['company'] == stock]['times'],
                                 y=df_sub[df_sub['company'] == stock]['closes'],
                                 mode='lines',
                                 opacity=0.7,
                                 name=stock,
                                 textposition='bottom center'))
        trace.append(go.Candlestick(x=df_sub[df_sub['company'] == stock]['times'],
                                open=df_sub[df_sub['company'] == stock]['opens'],
                                high=df_sub[df_sub['company'] == stock]['highs'],
                                low=df_sub[df_sub['company'] == stock]['lows'],
                                close=df_sub[df_sub['company'] == stock]['closes'],
                                increasing_line_color='#17BECF',
                                decreasing_line_color='#808080',
                                name=stock,
                                visible=False))
    
    updatemenus = list([
        dict(type="buttons",
             buttons=list([
                dict(label = 'Line',
                     method = 'update',
                     args = [{'visible': [True, False]}]),
                dict(label = 'Candlestick',
                     method = 'update',
                     args = [{'visible': [False, True]}])
            ]),
            direction="right",
            x=0,
            xanchor="left",
            y=1.2,
            yanchor="top"
        )
    ])
    
    # STEP 3
    traces = [trace]
    data = [val for sublist in traces for val in sublist]
    # Define Figure
    # STEP 4

    figure = {'data': data,
              'layout': go.Layout(
                    xaxis_rangeslider_visible=False,
                    margin=dict(l=10, r=10, t=10, b=10),
                    template="plotly_white",
                    showlegend=True,
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1),
                    updatemenus=updatemenus
                )

                }

    return figure

@app.callback(Output('live-update-graph-volume', 'figure'),
              [Input('markets', 'value')])
def update_timeseries_volume(selected_dropdown_value):
    ''' Draw traces of the feature 'value' based one the currently selected stocks '''
    # STEP 1
    trace = []  
    df_sub = df
    # STEP 2
    # Draw and append traces for each stock
    for stock in selected_dropdown_value:  
        trace.append(go.Bar(x=df_sub[df_sub['company'] == stock]['times'],
                            y=df_sub[df_sub['company'] == stock]['volumes'], name=stock))
    
    # STEP 3
    traces = [trace]
    data = [val for sublist in traces for val in sublist]
    # Define Figure
    # STEP 4

    figure = {'data': data,
              'layout': go.Layout(
                    margin=dict(l=10, r=10, t=10, b=10),
                    template="plotly_white",
                    showlegend=True,
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1)
                )

                }

    return figure

@app.callback(Output('graph-figure-capital', 'figure'),
              [Input('markets', 'value')])
def update_timeseries(selected_dropdown_value):
    ''' Draw traces of the feature 'value' based one the currently selected stocks '''
    # STEP 1
    trace = []
    df_sub = get_capital(df_investors)

    # STEP 2
    # Draw and append traces for each stock
    for stock in selected_dropdown_value:   
        trace.append(go.Scatter(x=df_sub[df_sub['name'] == stock]['times'],
                                 y=df_sub[df_sub['name'] == stock]['capital'],
                                 mode='lines',
                                 opacity=0.7,
                                 name=stock,
                                 textposition='bottom center'))
    
    updatemenus = list([
        dict(type="buttons",
             buttons=list([
                dict(label = 'Line',
                     method = 'update',
                     args = [{'visible': [True, False]}]),
                dict(label = 'Candlestick',
                     method = 'update',
                     args = [{'visible': [False, True]}])
            ]),
            direction="right",
            x=0,
            xanchor="left",
            y=1.2,
            yanchor="top"
        )
    ])
    
    # STEP 3
    traces = [trace]
    data = [val for sublist in traces for val in sublist]
    # Define Figure
    # STEP 4

    figure = {'data': data,
              'layout': go.Layout(
                    xaxis_rangeslider_visible=False,
                    margin=dict(l=10, r=10, t=10, b=10),
                    template="plotly_white",
                    showlegend=True,
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1),
                )

                }

    return figure

if __name__ == "__main__":
    app.run_server(port='2000', debug=True, threaded=True, use_reloader=False)