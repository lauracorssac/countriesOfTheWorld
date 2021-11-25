from app import db
from app.models import CountryDrinksInfo, Countries
import csv
from app.NameConverter import NameConverter
from sqlalchemy import exc


def insert_drinks():

    infos = []

    with open("data/drinks.csv", 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            
            info = CountryDrinksInfo(
                country_name= NameConverter.convert_country_name(row[0]),
                beer_servings= row[1],
                spirit_servings= row[2],
                wine_servings= row[3],
                total_litres_of_pure_alcohol= row[4],
                country_id= NameConverter.convert_country_name(row[0])
            )

            infos.append(info)
    
    for info in infos:
        try:
            db.session.add(info)
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
            new_info = getCountryNoForeignKey(info)
            db.session.add(new_info)
            db.session.commit()

def getCountryNoForeignKey(info):
    return CountryDrinksInfo(
                country_name= info.country_name,
                beer_servings= info.beer_servings,
                spirit_servings= info.spirit_servings,
                wine_servings= info.wine_servings,
                total_litres_of_pure_alcohol= info.total_litres_of_pure_alcohol,
                country_id= None
            )

def get_float(my_string):
    float_value = 0
    try:
	    float_value = float(my_string)
    except ValueError:
	    float_value = 0
    return float_value        

def insert_countries():

    countries = []

    with open("data/countries_of_the_world.csv", 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            
            country = Countries(
                country_name= NameConverter.convert_country_name(row[0]),
                population= get_float(row[2]),
                area= get_float(row[3]),
                population_density= get_float(row[4]),
                gpd_capita= get_float(row[8])
            )

            countries.append(country)
    
    for country in countries:
        db.session.add(country)
        db.session.commit()

insert_countries()
insert_drinks()
