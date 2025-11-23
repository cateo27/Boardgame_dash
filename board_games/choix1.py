import pandas as pd
from dash import html, dcc, dash_table

def layout(games):
    return html.Div([
        html.H3("Visualisation de la base de données"),
        html.P("Filtrer par nombre de joueurs"),

        html.Div([
            html.Div([
                html.Label("Nombre minimum de joueurs"),
                dcc.Input(
                    id="min-players-choice",
                    type="number",          
                    min=1,                  
                    step=1,
                    value=1, 
                    style={"width": "100%"}
                ),
            ], style={"flex": "1", "marginRight": "20px"}),

            html.Div([
                html.Label("Nombre maximum de joueurs"),
                dcc.Input(
                    id="max-players-choice",
                    type="number",
                    min=1,
                    step=1,
                    value=games["MaxPlayers"].max(),  
                    style={"width": "100%"}
                ),
            ], style={"flex": "1"})
        ], style={"display": "flex", "marginBottom": "30px"}),

        html.Div(id="row-count", style={"marginBottom": "20px"}),

        dash_table.DataTable(
            id="games-table",
            columns=[
                {"name": "BGGId", "id": "ID Game"},
                {"name": "Name", "id": "Name"},
                {"name": "Description", "id": "Description"},
                {"name": "Year Published", "id": "YearPublished"},
                {"name": "Game difficulty", "id": "GameWeight"},
                {"name": "Minimum number of players", "id": "MinPlayers"},
                {"name": "Maximum number of players", "id": "MaxPlayers"},
                {"name": "Age minimum (minimum estimated)", "id": "Age"},
                {"name": "Play time (minimum estimated)", "id": "Playtime"},
            ],
            page_size=5,
            style_table={"overflowX": "auto", "tableLayout": "fixed"},
            style_cell={"whiteSpace": "normal", "height": "auto"},
            style_cell_conditional=[
                {
                    "if": {"column_id": "Description"},
                    "width": "400px",
                    "minWidth": "400px",
                    "maxWidth": "400px",
                    "overflow": "hidden",
                    "textOverflow": "ellipsis"
                }
            ],
            css=[{
                "selector": ".dash-cell div.dash-cell-value",
                "rule": "white-space: normal; word-wrap: break-word;"
            }]
        )
    ])
