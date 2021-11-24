from app import app
from flask import render_template
from app.JsonManager import JsonManager
from app.models import User
from app.JsonManager import JsonManager

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}

    users = User.query.all()
    for u in users:
        print(u.id, u.username, u.email)
    
    return render_template('home.html', title='Home', user=user)

@app.route('/list')
def countries_list():

    country_names = JsonManager.get_country_name_list()
    return render_template('list.html', countries=country_names)



