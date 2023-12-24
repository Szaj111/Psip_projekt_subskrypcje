
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
    query_text = """
    INSERT INTO public.my_table (nick, name, city, subscription, film_category, movies_watched) 
    VALUES (:nick, :name, :city, :subscription, :film_category, :movies_watched)
    """
    sql_query = sqlalchemy.text(query_text)

    connection.execute(sql_query, {
        'nick': nick,
        'name': name,
        'city': city,
        'subscription': subscription,
        'film_category': film_category,
        'movies_watched': movies_watched
    })

    connection.commit()

def dodaj_użytkownika():
    nick = input('Podaj nick użytkownika - ')
    name = input('Podaj imię - ')
    city = input('Podaj miasto - ')
    subscription = input('Podaj rodzaj subskrypcji - ')
    film_category = input('Podaj rodzaj obejrzanego filmu - ')
    movies_watched = input('Podaj filmy oberzane przez użytkownika - ')

    sql_query = sqlalchemy.text("SELECT * FROM my_table WHERE nick=:nick")

    result = connection.execute(sql_query, {'nick': nick}).all()

    if not result:
        dodaj_uzytkownika_bazadanych(name, city, nick, subscription, film_category, movies_watched)
    else:
        print('Podany nick już istnieje')


dodaj_użytkownika()

# def pokaz_liste_uzytkownikow():
#     sql_query_1 = sqlalchemy.text(f"SELECT * FROM my_table")
#     result= connection.execute(sql_query_1).all()
#     for user in result:
#         print(user[0] + " nick " +user[3]+" jest z miasta "+ user[1] + " liczba jego postów - "+ str(user[2])   )
