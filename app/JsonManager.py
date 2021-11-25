
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
    
    def get_filter_statement(filter, criteria):
        
        empty_statement = "WHERE {{criteria}} {{operator}} AVG({{criteria}})"
        if filter == "all":
            return ""
        if filter == "gt_avg":
            return empty_statement.format(criteria=criteria, operator=">")
        if filter == "lt_avg":
            return empty_statement.format(criteria=criteria, operator="<")
        if filter == "gte_avg":
            return empty_statement.format(criteria=criteria, operator=">=")
        if filter == "lte_avg":
            return empty_statement.format(criteria=criteria, operator="<=")
        if filter == "eq_avg":
            return empty_statement.format(criteria=criteria, operator="==")
        else:
            return ""

    def get_from_statement(criteria):
        if (criteria == "wine_servings" or 
        criteria == "beer_servings" or 
        criteria == "spit_servings" or 
        criteria == "total_litres_of_pure_alcohol"):
            return "country_drinks_info"
        if (criteria == "gpd_capita" or 
        criteria == "population" or 
        criteria == "area"):
            return "countries"
        return ""

    def get_limit_statement(limit):

        limit_int = -1
        try:
            limit_int = int(limit)
        except ValueError:
            limit_int = -1
        
        return f"LIMIT {limit_int}" if limit_int != -1 else ""

    # criteria: gpd_capita, wine_servings,...
    # order: "", ASC, DESC
    # limit: none valid number
    # filter: all, gt_avg, gte_avg, lt_avg, lte_avg, eq_avg
    def rank_countries(criteria, order, limit, filter):
        
        from_statement = JsonManager.get_from_statement(criteria)
        if not from_statement:
            return []

        order_statement = f"ORDER BY {criteria} {order}" if order else "ORDER BY country_name"
        limit_statement = JsonManager.get_limit_statement(limit)
        filter_statement = JsonManager.get_filter_statement(filter, criteria)

        query = f"""
        SELECT country_name, {criteria} FROM {from_statement}
        {filter_statement}
        {order_statement}
        {limit_statement}
        """

        results = db.engine.execute(query)

        output_json = []
        for result in results:
            output_json.append(
                {
                    'country_name': result[0],
                    'criteria': result[1]
                }
            )
        return output_json


