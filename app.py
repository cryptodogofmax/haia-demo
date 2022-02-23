from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, dash_table
import pandas as pd
import base64
import datetime
import io
import random

genders = ["F", "M"]
ages = [i for i in range(1, 130)]
countries = [
    "Singapore",
    "United States of America",
    "China",
    "France",
    "Germany",
    "Japan",
]
foods = [
    "Fried Chicken",
    "Korean Barbecue",
    "Cheese Burger",
    "Roast Peking Duck",
    "Mutton in Hot Pot",
    "Macaron",
    "Stout Beer",
    "Kaya Toast",
    "Milk",
    "Coffee",
    "Minced Pork Congee with Preserved Egg",
    "Massage",
    "Gym",
    "Spa",
    "Laundry Service",
]
foods_pic = {
    "Fried Chicken": "https://thestayathomechef.com/wp-content/uploads/2016/06/Fried-Chicken-4-1.jpg",
    "Korean Barbecue": "https://i.ytimg.com/vi/_zqmjkXrYbM/maxresdefault.jpg",
    "Cheese Burger": "https://www.foodrepublic.com/wp-content/uploads/2012/03/033_FR11785.jpg",
    "Roast Peking Duck": "https://cuisint.com/wp-content/uploads/2020/10/FinishedDish-5Edited.jpg",
    "Mutton in Hot Pot": "https://pbs.twimg.com/media/D44WEM5UEAAimEM.jpg",
    "Macaron": "https://sugargeekshow.com/wp-content/uploads/2018/01/french-macaron-recipe.jpg",
    "Stout Beer": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fe/Stadin_Panimo_Double_Oat_Malt_Stout.jpg/1200px-Stadin_Panimo_Double_Oat_Malt_Stout.jpg",
    "Kaya Toast": "https://whattocooktoday.com/wp-content/uploads/2016/07/Singapore-kaya-toast-16.jpg",
    "Milk": "https://chriskresser.com/wp-content/uploads/raw-milk-1-e1563894986431.jpg",
    "Coffee": "https://images.immediate.co.uk/production/volatile/sites/30/2020/08/flat-white-d8ada0f.jpg",
    "Minced Pork Congee with Preserved Egg": "https://www.wokandkin.com/wp-content/uploads/2020/02/Century-Egg-and-Pork-Congee-saved-for-web-500x500.png",
    "Ice Cream": "https://blog.thermoworks.com/wp-content/uploads/2021/06/Ice_Cream_Compressed-43.jpg",
    "Massage": "https://www.verywellmind.com/thmb/CmLHdpJtnYEufXl-I3MDeEJpdvA=/2119x1414/filters:fill(ABEAC3,1)/massagetable-7306e2120fe04d078ac1212bd6929e2b.jpg",
    "Gym": "https://www.ucf.edu/news/files/2021/08/ucf-employee-gym.jpeg",
    "Spa": "https://visionrcl.org.uk/wp-content/uploads/2021/11/053_Vision_Fullwell_Cross_Friday_13th_21-1024x683.jpg",
    "Laundry Service": "https://www.centralpalms-hotel.com.np/wp-content/uploads/2020/01/Laundry-Service.jpg",
}


def find_food(age, gender, country):
    if not (age and gender and country):
        return ""
    if age < 5:
        return "Milk"

    if age > 25 and age <= 30:
        if gender == "F":
            return "Spa"
        else:
            return "Gym"

    if age > 30 and age < 50:
        if gender == "F":
            return "Laundry Service"
        else:
            return "Massage"

    if age > 80:
        return "Coffee"

    if country == "Singaopre":
        if age > 40:
            food = "Kaya Toast"
        elif gender == "F":
            food = "Fried Chicken"
        else:
            food = "Korean Barbecue"

    if country == "United States of America":
        food = "Cheese Burger"

    if country == "China":
        if age > 60:
            food = "Minced Pork Congee with Preserved Egg"
        elif gender == "F":
            food = "Roast Peking Duck"
        else:
            food = "Mutton in Hot Pot"

    if country == "France":
        food = "Macaron"

    if country == "Germany":
        food = "Stout Beer"

    if country == "Japan":
        food = "Sushi"

    else:
        food = "Ice Cream"
    return food


app = Dash(__name__)

title = html.H2(
    children="Hotel AI Assistant Mockup",
    style={"text-align": "center", "margin-bottom": "10px"},
)

ageDropdown = html.Div(
    [
        dbc.Label("Age", html_for="ageDropdown"),
        dcc.Dropdown(
            id="ageDropdown",
            options=[{"label": x, "value": x} for x in ages],
            style={"margin-top": "5px"},
        ),
    ],
    style={"margin": "10px"},
)

genderDropdown = html.Div(
    [
        dbc.Label("Gender", html_for="genderDropdown"),
        dcc.Dropdown(
            id="genderDropdown",
            options=[{"label": x, "value": x} for x in genders],
            style={"margin-top": "5px"},
        ),
    ],
    style={"margin": "10px"},
)

countryDropdown = html.Div(
    [
        dbc.Label("Country", html_for="countryDropdown"),
        dcc.Dropdown(
            id="countryDropdown",
            options=[{"label": x, "value": x} for x in countries],
            style={"margin-top": "5px"},
        ),
    ],
    style={"margin": "10px"},
)

foodDropdown = html.Div(
    [
        dbc.Label("Foods", html_for="foodDropdown"),
        dcc.Dropdown(
            id="foodDropdown",
            options=[{"label": x, "value": x} for x in foods],
            style={"margin-top": "5px"},
        ),
    ],
    style={"margin": "10px"},
)

recommendation = html.Div(
    [
        html.Div(
            id="recommendation",
            style={"margin-top": "5px"},
        ),
        html.Div(
            [
                html.Button(
                    "Generate Top 5 items to recommend",
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

uploadFilesDiv = html.Div(
    [
        dcc.Upload(
            id="upload-data",
            children=html.Div(
                ["(External Datasets) Drag and Drop or ", html.A("Select Files")]
            ),
            style={
                "width": "100%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "30px auto 20px auto",
                "background-color": "lightpink",
            },
            # Allow multiple files to be uploaded
            multiple=True,
        ),
        html.Div(id="output-data-upload"),
    ],
    style={
        "margin": "10px",
    },
)


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(",")

    decoded = base64.b64decode(content_string)
    try:
        if "csv" in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
        elif "xls" in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(filename, engine="openpyxl")
            df = df[
                [
                    "Gender",
                    "Nationality",
                    "Age",
                    "Food",
                    "Juice",
                    "Dessert",
                ]
            ]
    except Exception as e:
        print(e)
        return html.Div(["There was an error processing this file."])

    return html.Div(
        [
            html.H4(filename),
            html.H4(f"Upload time: {datetime.datetime.fromtimestamp(date)}"),
            dash_table.DataTable(
                df.to_dict("records"),
                [{"name": i, "id": i} for i in df.columns],
                style_as_list_view=True,
                style_table={
                    "overflowX": "scroll",
                    "height": "350px",
                },
            ),
        ]
    )


@app.callback(
    Output("output-data-upload", "children"),
    Input("upload-data", "contents"),
    State("upload-data", "filename"),
    State("upload-data", "last_modified"),
)
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d)
            for c, n, d in zip(list_of_contents, list_of_names, list_of_dates)
        ]
        return children


@app.callback(
    Output(component_id="recommendation", component_property="children"),
    Input(component_id="ageDropdown", component_property="value"),
    Input(component_id="genderDropdown", component_property="value"),
    Input(component_id="countryDropdown", component_property="value"),
)
def generate_recommendation(age, gender, country):
    if age and gender and country:
        food = find_food(age=age, gender=gender, country=country)
        print(food, foods_pic[food])
        src = foods_pic[food]
        return html.Img(src=src, style={"width": "500px"})
    else:
        return html.H3("The information provided is not enough.")


@app.callback(
    Output("container-button-basic", "children"),
    Input("submit-val", "n_clicks"),
)
def click_recommendation_button(n_clicks):
    top3 = random.sample(foods, 3)
    if n_clicks % 2 != 0:
        return html.Div(
            [
                html.Img(
                    src=foods_pic[img],
                    style={
                        "width": "500px",
                        "margin-top": "10px",
                    },
                )
                for img in top3
            ]
        )


form = dbc.Form(
    [
        title,
        ageDropdown,
        genderDropdown,
        countryDropdown,
        uploadFilesDiv,
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
