# 🌍 Countries of the World

Hi there! This project was made for Databases Project lecture of Universidade Federal do Rio Grande do Sul (UFRGS).
It consists on a website to analize data from csv that provides us with different data from countries of the world.

[Demo in Portuguese](https://drive.google.com/file/d/14PMDriyEvsqVwKilHfRtaRd1klYZ1Fhs/view)

## ⚙️ How to install

#### - Clone this repository and open the folder on terminal
  
#### - Install PostgresSQL
- On mac: `$ brew install postgresql`

#### - Start PostgresSQL
- On mac: `$ brew services start postgresql`
 
#### - Create a database on PostgresSQL named "countries"

- `$ /usr/local/opt/postgres/bin/createdb countries -p 5432 -h localhost`
- Or, open a Postgres client (such as Postbird) and create using the platform

#### - Create a username on PostgresSQL named "postgres"

`$ /usr/local/opt/postgres/bin/createuser -s postgres`
  
#### - Create a virtual environment
  `$ python3 -m venv countries_venv`

#### - Activate the virtual environment
  `$ source nba_env/bin/activate`
  
#### - Install project's dependencies

`(countries_venv)$ pip install -r requirements.txt`
  
#### - Tell flask how to import project
  `(countries_venv)$ export FLASK_APP=countries.py`

#### - Start flask's database

`(countries_venv)$ flask db init`
  
#### - Create columns on database (located on `app/models.py`)

`(countries_venv)$ flask db migrate`

#### - Updates Postgres with records 

`(countries_venv)$ flask db upgrade`

#### - Insert all values on database
  `(countries_venv)$ python insert.py`


## 🏃‍♀️ How to run

#### 1. Execute the project

`(countries_venv)$ flask run`

#### 2. The website will be displayed on 

http://127.0.0.1:5000/

Obs.: every time you are open a new terminal window, you should also run these two steps, also on the root of this repository:

- `$ source nba_env/bin/activate`
- `(countries_venv)$ export FLASK_APP=countries.py`

