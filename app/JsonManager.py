
from app.models import Countries, CountryDrinksInfo
import json
from app.NameConverter import NameConverter

# class that does all queries and transforms to json
class JsonManager:

    def get_country_name_list():
        countries = Countries.query.all()
        result = []
        for country in countries:
            country_display_name = NameConverter.convert_to_display_name(country.country_name)
            result.append({'country_name': country_display_name})
        return result

