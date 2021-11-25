
from app.models import Countries, CountryDrinksInfo
import json
from app.NameConverter import NameConverter
from app import db
#from app.AlcoholType import AlcoholType

# class that does all queries and transforms to json
class JsonManager:

    def get_country_name_list():
        query = """
        SELECT ROW_NUMBER() OVER(ORDER BY country_name), country_name FROM
        (
            SELECT country_name FROM countries
            UNION
            SELECT country_name FROM country_drinks_info
        ) AS subquery
        ORDER BY country_name
        """
        results = db.engine.execute(query)
        output_json = []
        for result in results:
            output_json.append(
                {
                    'order_index': result[0],
                    'country_name': result[1],
                }
            )
        return output_json

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
    
    def get_filter_statement(filter, criteria, table):
        
        empty_statement = "WHERE {criteria} {operator} (SELECT AVG({criteria}) FROM {table})\n"
        if filter == "all":
            return ""
        if filter == "gt_avg":
            return empty_statement.format(criteria=criteria, operator=">", table=table)
        if filter == "lt_avg":
            return empty_statement.format(criteria=criteria, operator="<", table=table)
        if filter == "gte_avg":
            return empty_statement.format(criteria=criteria, operator=">=", table=table)
        if filter == "lte_avg":
            return empty_statement.format(criteria=criteria, operator="<=", table=table)
        if filter == "eq_avg":
            return empty_statement.format(criteria=criteria, operator="==", table=table)
        else:
            return ""

    def get_table_name(criteria):
        if (criteria == "wine_servings" or 
        criteria == "beer_servings" or 
        criteria == "spirit_servings" or 
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
    # order: ASC, DESC
    # limit: none valid number
    # filter: all, gt_avg, gte_avg, lt_avg, lte_avg, eq_avg
    def rank_countries(criteria, order, limit, filter):
        
        table_name = JsonManager.get_table_name(criteria)
        if not table_name:
            return []

        order_statement = f"ORDER BY {criteria} {order}"
        limit_statement = JsonManager.get_limit_statement(limit)
        filter_statement = JsonManager.get_filter_statement(filter, criteria, table_name)

        query = f"""
        SELECT ROW_NUMBER() OVER(ORDER BY {criteria} {order}), country_name, {criteria} FROM {table_name}
        {filter_statement}
        {order_statement}
        {limit_statement}
        """

        results = db.engine.execute(query)

        output_json = []
        for result in results:
            output_json.append(
                {
                    'order_index': result[0],
                    'country_name': result[1],
                    'criteria': result[2]
                }
            )
        return output_json

    def get_two_criteria_all_countries(criteria1, criteria2):
        
        table1 = JsonManager.get_table_name(criteria1)
        table2 = JsonManager.get_table_name(criteria2)
        if not table1 or not table2:
            return []

        query = f"""
        SELECT countries.country_name, {table1}.{criteria1}, {table2}.{criteria2} FROM country_drinks_info
        INNER JOIN countries
        ON countries.country_name = country_drinks_info.country_id
        """

        results = db.engine.execute(query)
        output_json = []
        for result in results:
            output_json.append(
                {
                    'country_name': result[0],
                    'criteria1': result[1],
                    'criteria2': result[2]
                }
            )
        return output_json


