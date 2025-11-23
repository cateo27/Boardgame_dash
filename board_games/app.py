import dash
from dash import html, dcc, Output, Input
import choix1, choix2, choix3
import pandas as pd
from dash.exceptions import PreventUpdate


games = pd.read_csv("games.csv")

# importe themes
themes = pd.read_csv("themes.csv")
themes.columns = themes.columns.str.replace(r"^Theme_", "", regex=True)

# importe subcategories
subcategories = pd.read_csv("subcategories.csv")

# importe mechanics
mechanics = pd.read_csv("mechanics.csv")

# regroupe toutes les tables à partir de l'identifiant BGGId
games_all = (
    games
    .merge(themes, on="BGGId", how="left")         
    .merge(subcategories, on="BGGId", how="left")   
    .merge(mechanics, on="BGGId", how="left")       
)

app = dash.Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div([
    html.Div([
        html.H2("Options"),
        dcc.RadioItems(
            id="choix",
            options=[
                {"label": "Visualisation des données", "value": "choix1"},
                {"label": "Choix 2", "value": "choix2"},
                {"label": "Choix 3", "value": "choix3"},
            ],
            value="choix1",  # choix1 par défaut
            labelStyle={"display": "block"}
        )
    ], style={"width": "20%", "display": "inline-block",
              "verticalAlign": "top", "backgroundColor": "#d3d3d3", "height": "100vh"}),

    # Initialiser avec choix1 pour que les IDs existent au démarrage
    html.Div(
        id="page-content",
        children=choix1.layout(games_all),
        style={"width": "75%", "display": "inline-block", "padding": "20px"}
    )
])


# Déclaration de rous les IDs possibles
app.validation_layout = html.Div([
    app.layout,
    choix1.layout(games_all),
    choix2.layout(),
    choix3.layout(),
])


# Callback pour changer de page
@app.callback(
    Output("page-content", "children"),
    Input("choix", "value")
)
def update_page(choix):
    contenu = []
    if "choix1" in choix:
        contenu.append(choix1.layout(games_all))
    if "choix2" in choix:
        contenu.append(choix2.layout())
    if "choix3" in choix:
        contenu.append(choix3.layout())
    if not contenu:
        return html.P("Veuillez sélectionner une option à gauche.")
    return contenu

# Callback pour filtrer le tableau
@app.callback(
    [Output("games-table", "data"),
     Output("row-count", "children")],
    [Input("max-players-choice", "value"),
     Input("min-players-choice", "value"),
     Input("choix", "value")]
)
def update_table(max_players, min_players, choix):
    if choix != "choix1":
        raise PreventUpdate

    # Vérification des valeurs saisies
    if min_players is None or max_players is None or min_players < 1 or max_players < 1:
        return [{"Name": "⚠️ Entrez des entiers positifs non nuls"}], "0 ligne"

    if min_players > max_players:
        return [{"Name": "⚠️ Erreur : le minimum est supérieur au maximum"}], "0 ligne"

    # Filtrage du DataFrame
    filtered = games_all[(games_all["MinPlayers"] >= min_players) &
                     (games_all["MaxPlayers"] <= max_players)]
    filtered["Playtime"] = filtered["MfgPlaytime"].astype(str) + " (Min "+filtered["ComMinPlaytime"].astype(str)+")"
    # Arrondir à l'unité avant conversion en texte
    
    filtered["ComAgeRec"] = filtered["MfgAgeRec"].fillna(0)
    filtered["Age"] = filtered.apply(lambda row: f"{int(round(row['MfgAgeRec']))} (Mean rec. {int(round(row['ComAgeRec']))})", axis=1 )

    return filtered.to_dict("records"), f"{len(filtered)} lignes répondent à ces filtres"

if __name__ == "__main__":
    app.run(debug=True)