from app import db

class CountryDrinksInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    country_name = db.Column(db.String(64), unique=True)
    beer_servings = db.Column(db.Float, unique=False)
    spirit_servings = db.Column(db.Float, unique=False)
    wine_servings = db.Column(db.Float, unique=False)
    total_litres_of_pure_alcohol = db.Column(db.Float, unique=False)
    country_id = db.Column(db.String(), db.ForeignKey('countries.country_name'), nullable=True)

    def __repr__(self):
        string = "country = " + self.country_name
        string += " beer = " + self.beer_servings
        string += " spirit = " + self.spirit_servings
        string += " total = " + self.total_litres_of_pure_alcohol
        string += " id = " + self.country_id
        return string

class Countries(db.Model):
    country_name = db.Column(db.String(64), unique=True, primary_key=True, nullable=False)
    population = db.Column(db.Integer, unique=False, nullable=True)
    area = db.Column(db.Float, unique=False, nullable=True)
    population_density = db.Column(db.Float, unique=False, nullable=True)
    gpd_capita = db.Column(db.Float, unique=False, nullable=True)


class Chocolate(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    company_location = db.Column(db.String(64), unique=False, nullable=False)
    country_of_bean_origin = db.Column(db.String(64), unique=False, nullable=False)
    company_location_id = db.Column(db.String(), db.ForeignKey('countries.country_name'), nullable=True)
    country_of_bean_origin_id = db.Column(db.String(), db.ForeignKey('countries.country_name'), nullable=True)
    cocoa_percent = db.Column(db.Float, unique=False, nullable=True)
    rating = db.Column(db.Float, unique=False, nullable=True)
    
    def __repr__(self):
        string = "id = " + self.id
        string += " company location = " + self.company_location
        string += " country of bean origin = " + self.country_of_bean_origin
        string += " cocoa percent = " + self.cocoa_percent
        string += " rating = " + self.rating
        return string
    


