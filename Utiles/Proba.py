import requests
import folium
import sqlalchemy
from bs4 import BeautifulSoup

# from notatnik import Category
from orm.ddl import Movie, Base , User
from sqlalchemy.orm import sessionmaker
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
# Base.metadata.drop_all(bind=engine)
# Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

#--------dodawanie filmów GIT------------
def dodaj_film_baza_danych(movie_name,category):
    movie = Movie(movie_name=movie_name,category=category)
    session.add(movie)
    session.commit()
def dodaj_film():
    movie_name = input("Nazwa filmu: ")
    category = input("Nazwa kategori:")
    dodaj_film_baza_danych(movie_name,category)
#dodaj_film()
#^ działa


#--------wyświetalnie listy filmów wraz z kategoriami- GIT----------
def wyświetl_wszystkie_filmy():
    movie_list = session.query(Movie).all()
    session.commit()
    for movie in movie_list:
        print(movie.movie_name +str(" -"), movie.category)
#wyświetl_wszystkie_filmy()

# ---------------usuwanie filmow - GIT ----------------------
def usuń_film_baza_danych (movie_name):
    while True:
        movie = session.query(Movie).filter_by(movie_name=movie_name).first()
        if movie_name == "1":
            break
        if movie:
            session.delete(movie)
            session.commit()
            print(f'Film {movie_name} został usunięty')
            break
        else:
            print(f'Film {movie_name} nie istnieje')
            movie_name = input('Podaj poprawna nazwe filmu: \n'
                  'Wpisz - 1 aby wyjść \n')
            if movie_name == "1":
                break

# def usuń_film():
#     movie_name = input("Podaj nazwe filmu do usunięcia ")
#     usuń_film_baza_danych(movie_name=movie_name)

def usuń_film():
    wyświetl_wszystkie_filmy()
    movie_name_to_delete = input("Podaj film do usunięcia - ")
    usuń_film_baza_danych(movie_name_to_delete)
#usuń_film()

#-------Modyfikuj film--------------
def modyfikuj_film():
    wyświetl_wszystkie_filmy()

    movie_name_to_change = input("Podaj film do zmiany - ")
    movie = session.query(Movie).filter_by(movie_name=movie_name_to_change).first()

    if movie:
        nowa_nazwa_filmu = input("Podaj nową nazwę filmu - ")
        nowa_kategoria = input("Podaj nową kategorię filmu - ")

        movie.movie_name = nowa_nazwa_filmu
        movie.category = nowa_kategoria
        session.commit()
        print(f'Film {movie_name_to_change} został zmieniony na {nowa_nazwa_filmu}.')
        print(f'Kategoria filmu {movie_name_to_change} została zmieniona na {nowa_kategoria}.')
    else:
        print(f'Film {movie_name_to_change} nie istnieje w bazie danych.')

#modyfikuj_film()

dodaj_film()