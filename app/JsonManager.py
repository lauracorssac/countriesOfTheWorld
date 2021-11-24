
from app.models import CountryDrinksInfo
import json

# class that does all queries and transforms to json
class JsonManager:

    def get_country_name_list():
        countries = CountryDrinksInfo.query.all()
        result = []
        for country in countries:
            result.append({'country_name': country.country_name})
        return result

