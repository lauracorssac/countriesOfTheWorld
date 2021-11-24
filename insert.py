from app import db
from app.models import User, CountryDrinksInfo
import csv

# u = User(username='laura', email='la@example.com')
# db.session.add(u)
# db.session.commit()

# users = User.query.all()
# for u in users:
#     print(u.id, u.username, u.email)

def insert_drinks():

    infos = []

    with open("data/drinks.csv", 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            
            info = CountryDrinksInfo(
                country_name= row[0],
                beer_servings= row[1],
                spirit_servings= row[2],
                wine_servings= row[3],
                total_litres_of_pure_alcohol= row[4]
            )

            infos.append(info)
    
    for info in infos:
        db.session.add(info)
        db.session.commit()

insert_drinks()