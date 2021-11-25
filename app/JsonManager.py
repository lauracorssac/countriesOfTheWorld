
from app.models import Countries, CountryDrinksInfo
import json
from app.NameConverter import NameConverter
from app import db
#from app.AlcoholType import AlcoholType

# class that does all queries and transforms to json
class JsonManager:

    def get_country_name_list():
        query = """
        SELECT country_name FROM countries
        UNION
        SELECT country_name FROM country_drinks_info
        ORDER BY country_name
        """
        country_names = db.engine.execute(query)
        return country_names

    # {alcoholType}_doses * population / area
    def get_alcohol_per_area(country_name, alcohol_type):
        query = """
        SELECT country_drinks_info.country_name, country_drinks_info.{alcohol_type}, countries.population, countries.area FROM country_drinks_info
        INNER JOIN countries
        ON country_drinks_info.country_id = countries.country_name
        WHERE country_drinks_info.country_name = '{country_name}'
        """.format(alcohol_type=alcohol_type+"_servings", country_name=country_name)

        result = db.engine.execute(query).first()
        servings = result[1]
        population = result[2]
        area = result[3]
        alcohol_area = servings * population / area
        result_json = {
            'country_name': country_name,
            'alcohol_area': alcohol_area
            }
        return result_json

    def get_info(country_name):
        query = f"""
        SELECT country_drinks_info.country_name, \
            country_drinks_info.beer_servings, \
            country_drinks_info.spirit_servings, \
            country_drinks_info.wine_servings, \
            country_drinks_info.total_litres_of_pure_alcohol, \
            countries.population, countries.area, countries.gpd_capita \
        FROM country_drinks_info
        INNER JOIN countries
        ON country_drinks_info.country_id = countries.country_name
        WHERE country_drinks_info.country_name = '{country_name}'
        """

        result = db.engine.execute(query).first()
        
        result_json = {
            'country_name': result[0],
            'beer_servings': result[1],
            'spirit_servings':result[2],
            'wine_servings': result[3],
            'total_litres_of_pure_alcohol': result[4],
            'population': result[5],
            'area': result[6],
            'gpd_capita': result[7]
            }
        
        return result_json


