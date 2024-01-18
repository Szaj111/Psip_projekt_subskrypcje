import requests
import folium
import sqlalchemy
from bs4 import BeautifulSoup

db_params = sqlalchemy.URL.create(
    drivername='postgresql+psycopg2',
    username= 'postgres',
    password= 'psip2023',
    host= 'localhost',
    database='postgres',
    port=5432
)

engine = sqlalchemy.create_engine(db_params)

connection = engine.connect()

def dodaj_obejrzany_film():

    movie_name = input("Podaj nazwe obejrzanego filmu: ")
    movie_category = input("Podaj nawe kategorii filmu: ")
