from app import app
from flask import render_template
from app.JsonManager import JsonManager
from app.models import User
from app.JsonManager import JsonManager
from app.NameConverter import NameConverter
from app.GhapicManager import GraphicManager

def index():
    user = {'username': 'Miguel'}

    users = User.query.all()
    for u in users:
        print(u.id, u.username, u.email)
    
    return render_template('home.html', title='Home', user=user)

@app.route('/')
@app.route('/index')
@app.route('/list')
def countries_list():

    countries=[]
    country_names = JsonManager.get_country_name_list()
    for country_name in country_names:
        name = country_name[0]
        countries.append(
            {
                'country_name': NameConverter.convert_to_display_name(name),
                'country_route': name
            }
        )

    return render_template('list.html', countries=countries)

@app.route('/alcohol_area/<country_name>/<alcohol_type>')
def alcohol_area(country_name, alcohol_type):

    results = JsonManager.get_alcohol_per_area(country_name, alcohol_type)
    alcohol_area = results["alcohol_area"]
    alcohol_area_string = f"{alcohol_area: .2f}"
    country_display_name = NameConverter.convert_to_display_name(country_name)
    return render_template(
        'alcohol_area.html', 
        country_name=country_display_name, 
        alcohol_type= alcohol_type,
        lcohol_area= alcohol_area_string
    )

@app.route('/info/<country_name>')
def country_info(country_name):

    results = JsonManager.get_info(country_name)
    country_display_name = NameConverter.convert_to_display_name(country_name)

    return render_template(
        'country_info.html',
        country_name= country_display_name,
        beer = results["beer_servings"],
        spirit = results["spirit_servings"],
        wine = results["wine_servings"],
        total = results["total_litres_of_pure_alcohol"],
        population=results["population"], 
        area = results["area"],
        gpd = results["gpd_capita"]
    )

def convertJSONToPresentation(jsonItem):
    return {
        'order_index': jsonItem['order_index'],
        'country_name': NameConverter.convert_to_display_name(jsonItem["country_name"]),
        'country_route': jsonItem["country_name"],
        'criteria': "{criteria: .2f}".format(criteria= jsonItem["criteria"])
    }

@app.route('/ranking/<criteria>/<order>', defaults={'limit': "none", 'filter': 'all'})
@app.route('/ranking/<criteria>/<order>/<limit>', defaults={'filter': "all"})
@app.route('/ranking/<criteria>/<order>/<limit>/<filter>')
def rank_countries(criteria, order, limit, filter):
    results = JsonManager.rank_countries(criteria, order, limit, filter)
    results = map(convertJSONToPresentation, results)
    return render_template('rank.html', countries= results)

@app.route('/correlation/<criteria1>/<criteria2>')
def get_correlation(criteria1, criteria2):
    
    results = JsonManager.get_two_criteria_all_countries(criteria1, criteria2)
    
    vector1 = []
    vector2 = []

    for result in results:
        vector1.append(result["criteria1"])
        vector2.append(result["criteria2"])

    image_url = f"/app/images/correlation_{criteria1}_{criteria2}.png"
    pngImageB64String = GraphicManager.correlate(vector1, vector2, image_url, criteria1, criteria2)
    criteria1_title = NameConverter.convert_to_display_name(criteria1)
    criteria2_title = NameConverter.convert_to_display_name(criteria2)

    return render_template(
        'correlation.html', 
        title= f"Correlation between {criteria1_title} and {criteria2_title}", 
        image= pngImageB64String
    )
