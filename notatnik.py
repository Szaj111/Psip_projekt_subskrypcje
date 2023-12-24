
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
def dodaj_uzytkownika_bazadanych(name, city, nick, subscription, film_category, movies_watched):
    query_text = "INSERT INTO public.my_table (nick, name, city, subscription, film_category, movies_watched) VALUES ('{}','{}','{}','{}','{}','{}')".format(nick, name, city, subscription, film_category, movies_watched)
    sql_query_1 = sqlalchemy.text(query_text)
    connection.execute(sql_query_1)
    connection.commit()
def dodaj_użytkownika():
    nick = input('Podaj nick uzytkownika - ')
    name = input ("podaj imie? - ")
    city = input('Podaj miasto - ')
    subscription = input('Podaj rodzaj subskrypcji - ')
    film_category = input('Podaj rodzaj obejrzanego filmu DO ZMIANY####')
    movies_watched = input('Podaj filmy oberzane przez uzytkownika')
    sql_query_1 = sqlalchemy.text(f"SELECT FROM my_table WHERE nick='{nick}'")
    result= connection.execute(sql_query_1).all()
    if result == []:
        dodaj_uzytkownika_bazadanych(nick, name, city, subscription, film_category, movies_watched)
    else:
        print('Podany nick już istnieje')
        dodaj_użytkownika()

dodaj_użytkownika()