
from app.models import Countries, CountryDrinksInfo
import json
from app.NameConverter import NameConverter
from app import db
from sqlalchemy.inspection import inspect
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

    
    # get columns that country_name is in the top X when listing in descending order
    def get_categories_top_X(country_name, limiar):
        query = f"""
        SELECT row_number FROM (
            SELECT ROW_NUMBER() OVER(ORDER BY * DESC), country_name FROM country_drinks_info
            LIMIT {limiar}
        ) 
        WHERE {country_name} IN 
        
        
        """


    def get_info(country_name):
        query = f"""
        SELECT countries.country_name, \
            beer_servings, \
            spirit_servings, \
            wine_servings, \
            total_litres_of_pure_alcohol, \
            population, \
            area, \
            gpd_capita \
            FROM country_drinks_info
        FULL OUTER JOIN countries
        ON country_drinks_info.country_name = countries.country_name
        WHERE countries.country_name = '{country_name}' OR country_drinks_info.country_name = '{country_name}'
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

        countries_columns = [column.name for column in inspect(Countries).c]
        if criteria in countries_columns:
            return "countries"

        drinks_columns = [column.name for column in inspect(CountryDrinksInfo).c]
        if criteria in drinks_columns:
            return "country_drinks_info"

        if criteria in ["country_of_bean_origin", "company_location"]: 
            return "chocolate"
        return ""

    # criteria: country_of_bean_origin, company_location
    # order: ASC, DESC
    # limit: none valid number
    # filter: all, gt_avg, gte_avg, lt_avg, lte_avg, eq_avg
    def rank_avg_rating_choco(criteria, order, limit, filter):

        order_statement = f"ORDER BY AVG(rating) {order}"
        limit_statement = JsonManager.get_limit_statement(limit)
        filter_statement = JsonManager.get_filter_statement(filter, "avg_score", "chocolate")

        query= f"""
        DROP VIEW IF EXISTS sub_view;
        CREATE VIEW sub_view AS
        SELECT {criteria}, AVG(rating) AS avg_score
        FROM chocolate
        GROUP BY {criteria}
        {filter_statement}
        {order_statement}
        {limit_statement};
        SELECT ROW_NUMBER() OVER(), {criteria}, avg_score FROM sub_view;
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
        SELECT ROW_NUMBER() OVER(), country_name, {criteria} FROM {table_name}
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

        query = ""
        if table1 == "chocolate":
            query += JsonManager.create_view(criteria1, "view1") 
            table1 = "view1"
            criteria1 = "avg_rating"
        if table2 == "chocolate":
            query += JsonManager.create_view(criteria2, "view2") 
            table2 = "view2"
            criteria2 = "avg_rating"

        from_statement = ""
        if table1 == table2:
            from_statement = f"{table1}"
        else:
            from_statement = f"""
            {table1}
            INNER JOIN {table2}
            ON {table1}.country_name = {table2}.country_name
            """
        
        query += f"""
        SELECT {table1}.country_name, {table1}.{criteria1}, {table2}.{criteria2} 
        FROM {from_statement}
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

    def create_view(criteria_country, view_name):
        query= f"""
        DROP VIEW IF EXISTS {view_name};
        CREATE VIEW {view_name} AS
        SELECT {criteria_country} AS country_name, AVG(rating) AS avg_rating
        FROM chocolate
        GROUP BY {criteria_country};
        """
        return query

    
    

