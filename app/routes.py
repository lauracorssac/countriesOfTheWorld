from app import app
from app import nav
from flask import render_template
from flask import request
from app.JsonManager import JsonManager
from app.JsonManager import JsonManager
from app.NameConverter import NameConverter
from app.GhapicManager import GraphicManager
from app.SelectionOptionsManager import SelectionOptionsManager

nav.Bar('top', [
    nav.Item('Home', 'countries_list'),
    nav.Item('Correlation', 'get_correlation'),
])

@app.route('/')
@app.route('/index')
@app.route('/list')
def countries_list():

    countries = JsonManager.get_country_name_list()

    return render_template(
        'rank.html', 
        countries=map(convertJSONToPresentation,countries), 
        selections=SelectionOptionsManager.get_ranking_selections()
    )

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
        'criteria_ranked': "{criteria: .2f}".format(criteria= jsonItem["criteria"]) if "criteria" in jsonItem else ""
    }

@app.route('/ranking/')
# @app.route('/ranking/<criteria>/', defaults={'order':'ASC', 'limit': "none", 'filter': 'all'})
# @app.route('/ranking/<criteria>/<order>', defaults={'limit': "none", 'filter': 'all'})
# @app.route('/ranking/<criteria>/<order>/<limit>', defaults={'filter': "all"})
# @app.route('/ranking/<criteria>/<order>/<limit>/<filter>')
def rank_countries():

    criteria_arg = request.args.get('chosen_criteria')
    order_arg = request.args.get('order')
    limit_arg = request.args.get('limit')
    filter_arg = request.args.get('filter')

    if not criteria_arg:
        return

    criteria = criteria_arg
    order = order_arg if order_arg is not None else "ASC"
    filter = filter_arg if filter_arg is not None else "all"
    limit = limit_arg if limit_arg is not None else "none"

    results = JsonManager.rank_countries(criteria, order, limit, filter)
    results = map(convertJSONToPresentation, results)
    return render_template(
        'rank.html', 
        countries= results,
        criterias= SelectionOptionsManager.get_criterias(),
        orders= SelectionOptionsManager.get_options(),
        filters= SelectionOptionsManager.get_filters()
    )

@app.route('/correlation/')
def get_correlation():
    
    criteria1 = request.args.get('criteria1')
    criteria2 = request.args.get('criteria2')

    if not criteria1 or not criteria2:
        return render_template(
            'correlation.html', 
            selections=SelectionOptionsManager.get_correlation_selections())

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
        selections=SelectionOptionsManager.get_correlation_selections(),
        image= pngImageB64String,
        title = f"Correlation between {criteria1_title} and {criteria2_title}"
    )
