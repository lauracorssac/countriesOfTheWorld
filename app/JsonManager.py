
from app.models import Countries, CountryDrinksInfo
import json
from app.NameConverter import NameConverter
from app import db

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

        result = []
        for country_name in country_names:
            country_display_name = NameConverter.convert_to_display_name(country_name[0])
            result.append({'country_name': country_display_name})
        return result

