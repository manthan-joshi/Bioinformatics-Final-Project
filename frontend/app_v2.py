from dash import Dash, dcc, html, Input, Output, State, dash_table
import requests
import pandas as pd

app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server

API_URL = "http://127.0.0.1:8000"
theme_color = "#48AAAD"
palet = {
     "fontFamily": "Arial",
     "padding": "40px",
     "backgroundColor": "#f0f6ff",
     "color": "#002b5c"
 }

app.layout = html.Div(
    style=palet,
    children=[
        html.H2("Taxon Search", style={"color": theme_color}),

        # Keyword Search Section
        html.Div([
            html.H4("🔍 Search by Keyword", style={"color": theme_color}),
            html.Div([
                dcc.Input(
                    id='keyword-input',
                    type='text',
                    placeholder='Enter keyword...',
                    style={
                        "padding": "10px", "marginRight": "10px", "borderRadius": "6px",
                        "border": f"1px solid {theme_color}"
                    }
                ),
                dcc.Dropdown(
                    id='search-mode',
                    options=[
                        {'label': 'Contains', 'value': 'contains'},
                        {'label': 'Starts With', 'value': 'starts with'},
                        {'label': 'Ends With', 'value': 'ends with'}
                    ],
                    placeholder="Select search mode",
                    style={
                        "width": "200px", "padding": "10px",
                        "borderRadius": "6px", "border": f"1px solid {theme_color}"
                    }
                ),
            ], style={"marginBottom": "10px"}),

            html.Button(
                'Search',
                id='search-button',
                n_clicks=0,
                style={
                    "backgroundColor": theme_color, "color": "white", "padding": "10px 20px",
                    "border": "none", "borderRadius": "6px", "cursor": "pointer"
                }
            ),

            html.Div(id='table-container', style={"marginTop": "20px"})
        ], style={"marginBottom": "40px", "padding": "20px", "backgroundColor": palet['backgroundColor'], "borderRadius": "10px"}),

        # Taxon ID Search Section
        html.Div([
            html.H4("🔎 Lookup by Taxon ID", style={"color": theme_color}),
            html.Div([
                dcc.Input(
                    id='taxon-id-input',
                    type='number',
                    placeholder='Enter Taxon ID...',
                    style={
                        "padding": "10px", "marginRight": "10px",
                        "borderRadius": "6px", "border": f"1px solid {theme_color}"
                    }
                ),
                html.Button(
                    'Get Details',
                    id='taxon-search-button',
                    n_clicks=0,
                    style={
                        "backgroundColor": theme_color, "color": "white", "padding": "10px 20px",
                        "border": "none", "borderRadius": "6px", "cursor": "pointer"
                    }
                ),
            ], style={"marginBottom": "10px"}),

            html.Div(id='taxon-details-container', style={"marginTop": "20px"})
        ], style={"padding": "20px", "backgroundColor": palet['backgroundColor'], "borderRadius": "10px"})
    ]
)

# Keyword-based search
@app.callback(
    Output('table-container', 'children'),
    Input('search-button', 'n_clicks'),
    State('keyword-input', 'value'),
    State('search-mode', 'value')
)
def search_taxa(n_clicks, keyword, mode):
    if not n_clicks or not keyword or not mode:
        return ""

    try:
        response = requests.get(f"{API_URL}/search", params={
            "keyword": keyword,
            "mode": mode
        })

        if response.ok:
            data = response.json()["results"]
            if not data:
                return "No results found."

            df = pd.DataFrame(data)
            df['taxon_id'] = df['taxon_id'].apply(lambda tid: f"[{tid}](#{tid})")

            return dash_table.DataTable(
                data=df.to_dict('records'),
                columns=[{"name": i, "id": i, "presentation": "markdown"} for i in df.columns],
                page_size=10,
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'left'},
                style_header={'backgroundColor': 'lightgrey'}
            )
        else:
            return f"Error: {response.status_code}"
    except Exception as e:
        return f"Error: {e}"


# Taxon details page
@app.callback(
    Output('taxon-details-container', 'children'),
    Input('taxon-search-button', 'n_clicks'),
    State('taxon-id-input', 'value')
)
def get_taxon_details(n_clicks, tax_id):
    if not n_clicks or not tax_id:
        return ""

    try:
        response = requests.get(f"{API_URL}/taxa", params={"tax_id": tax_id})
        if not response.ok:
            return f"❌ Taxon ID {tax_id} not found."

        data = response.json()

        # Parent info
        parent = data.get("parent", {})
        parent_link = html.A(f"{parent.get('name')} ({parent.get('id')})", href="#", id='parent-link') if parent else "None"

        # Children table
        children = data.get("children", [])
        children_df = pd.DataFrame(children) if children else pd.DataFrame(columns=["id", "name", "rank"])
        if not children_df.empty:
            children_df['id'] = children_df['id'].apply(lambda x: f"[{x}](#{x})")
            children_table = dash_table.DataTable(
                data=children_df.to_dict('records'),
                columns=[{"name": i, "id": i, "presentation": "markdown"} for i in children_df.columns],
                page_size=10,
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'left'},
                style_header={'backgroundColor': 'lightblue'}
            )
        else:
            children_table = "No children found."

        # Names table
        names = data.get("names", [])
        names_df = pd.DataFrame(names) if names else pd.DataFrame(columns=["name", "class"])
        names_table = dash_table.DataTable(
            data=names_df.to_dict('records'),
            columns=[{"name": i, "id": i} for i in names_df.columns],
            page_size=10,
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'left'},
            style_header={'backgroundColor': 'lightgreen'}
        )

        return html.Div([
            html.H3(f"Taxon ID: {data['id']}"),
            html.P(f"Rank: {data.get('rank', 'Unknown')}"),
            html.P(["Parent: ", parent_link]),
            html.H4("Children:"),
            children_table,
            html.H4("Names:"),
            names_table,
            html.Br(),
            html.A("⬅ Back to Search", href="#")
        ])
    except Exception as e:
        return f"Error retrieving taxon: {e}"


if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
