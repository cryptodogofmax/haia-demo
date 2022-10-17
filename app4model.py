import json
import random

import dash_bootstrap_components as dbc
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

f = open("modelData.json")
data = json.load(f)
customers = {
    "No Selection": {},
    "customer1": data["customer1"],
    "customer2": data["customer2"],
    "customer3": data["customer3"],
}
foods = data["food"]
drinks = data["drink"]
laundries = data["Laundry Service"]
retails = data["Retail"]

app = Dash(__name__)

title = html.H2(
    children="Hotel AI Assistant Model",
    style={"text-align": "center", "margin-bottom": "10px"},
)

customerProfile = html.Div(
    [
        dbc.Label("Customer", html_for="customerProfile"),
        dcc.Dropdown(
            id="customerProfile",
            options=[{"label": x, "value": x} for x in customers.keys()],
            style={"margin-top": "5px"},
        ),
    ],
    style={"margin": "10px"},
)

customerInfo = html.Div(id="customerInfo")


@app.callback(Output("customerInfo", "children"), Input("customerProfile", "value"))
def update_output(value):
    if value:
        customer = customers[value]
        return [dbc.Label(f"{k}: {customer[k]}; ") for k in customer.keys()]
    return html.Div()


recommendation = html.Div(
    [
        html.Div(
            id="recommendation",
            style={"margin-top": "5px"},
        ),
        html.Div(
            [
                html.Button(
                    "Generate items to recommend",
                    id="submit-val",
                    n_clicks=0,
                    style={
                        "margin-bottom": "20px",
                        "height": "50px",
                    },
                ),
                html.Div(
                    id="container-button-basic",
                    children="Enter a value and press submit",
                ),
            ],
            style={
                "text-align": "center",
            },
        ),
    ],
    style={"margin-top": "30px"},
)


def get_random_obj(d):
    return random.choice(list(d.items()))


def get_result():
    return {
        "food": get_random_obj(foods)[1],
        "drink": get_random_obj(drinks)[1],
        "laundry": get_random_obj(laundries)[1],
        "retail": get_random_obj(retails)[1],
    }


@app.callback(
    Output("container-button-basic", "children"),
    Input("submit-val", "n_clicks")
)
def click_recommendation_button(n_clicks):
    result = get_result()
    if n_clicks % 2 != 0:
        return html.Div(
            [
                html.Img(
                    src=img,
                    style={
                        "width": "500px",
                        "margin-top": "10px",
                    },
                )
                for img in result.values()
            ]
        )


form = dbc.Form(
    [
        title,
        customerProfile,
        customerInfo,
        recommendation,
    ],
    style={
        "width": "600px",
        "margin": "30px auto auto auto",
    },
)

app.layout = html.Div(
    [
        html.Div(
            style={
                "background": "url(https://cdn.pixabay.com/photo/2021/10/06/15/05/bedroom-6686061_1280.jpg) no-repeat center center fixed",
                "background-size": "cover",
                "position": "absolute",
                "left": "0",
                "right": "0",
                "top": "0",
                "bottom": "0",
                "opacity": "0.5",
                "z-index": "-1",
                "height": "1600px",
            },
        ),
        form,
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
