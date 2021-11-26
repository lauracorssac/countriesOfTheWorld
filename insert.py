from app import db
from app.models import Chocolate, CountryDrinksInfo, Countries
import csv
from app.NameConverter import NameConverter
from sqlalchemy import exc
from copy import deepcopy

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

def get_chocolate_no_foreign_key(chocolate):
    return Chocolate(
        id = chocolate.id,
        company_location = chocolate.company_location,
        country_of_bean_origin = chocolate.country_of_bean_origin,
        cocoa_percent = chocolate.cocoa_percent,
        rating = chocolate.rating,
        country_of_bean_origin_id = None,
        company_location_id = None

    )

def insert_chocolate():

    infos = []
    with open("data/chocolate.csv", 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            info = Chocolate(
                id = row[0],
                company_location = NameConverter.convert_country_name(row[3]),
                country_of_bean_origin = NameConverter.convert_country_name(row[5]),
                cocoa_percent = row[7],
                rating = row[8],
                country_of_bean_origin_id = NameConverter.convert_country_name(row[5]),
                company_location_id = NameConverter.convert_country_name(row[3])
            )
            infos.append(info)

    for info in infos:

        new_info = deepcopy(info)

        if new_info.country_of_bean_origin == 'blend':
            continue

        if db.session.query(Countries.country_name).filter_by(country_name=info.company_location_id).count() == 0:
            new_info.company_location_id = None
        if db.session.query(Countries.country_name).filter_by(country_name=info.country_of_bean_origin_id).count() == 0:
            new_info.country_of_bean_origin_id = None

        db.session.add(new_info)
        db.session.commit()

Chocolate.query.delete()
insert_chocolate()
#insert_countries()
#insert_drinks()
