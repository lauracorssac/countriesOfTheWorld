from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

class CountryDrinksInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country_name = db.Column(db.String(64), unique=True)
    beer_servings = db.Column(db.Float, unique=False)
    spirit_servings = db.Column(db.Float, unique=False)
    wine_servings = db.Column(db.Float, unique=False)
    total_litres_of_pure_alcohol = db.Column(db.Float, unique=False)

    def __repr__(self):
        string = "country = " + self.country_name
        string += "beer = " + self.beer_servings
        string += "spirit = " + self.spirit_servings
        string += "total = " + self.total_litres_of_pure_alcohol
        return string