from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html

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
}


def find_food(age, gender, country):
    if not (age and gender and country):
        return ""
    if age < 5:
        return "Milk"

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
        dbc.Label("=> Recommendation:", html_for="recommendation"),
        html.Div(
            id="recommendation",
            style={"margin-top": "5px"},
        ),
    ],
    style={"margin-top": "30px"},
)


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


form = dbc.Form(
    [title, ageDropdown, genderDropdown, countryDropdown, recommendation],
    style={"width": "500px", "margin": "30px auto auto auto"},
)

app.layout = form

if __name__ == "__main__":
    app.run_server(debug=True)
