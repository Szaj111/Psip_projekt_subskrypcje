import requests
import folium
import sqlalchemy
from bs4 import BeautifulSoup

from notatnik import Category
from orm.ddl import Movie, Base
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
# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine) -
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
    movie = session.query(Movie).filter_by(movie_name=movie_name).first()
    if movie:
        session.delete(movie)
        session.commit()
        print(f'Film {movie_name} został usunięty')
    else:
        print(f'Film {movie_name} nie istnieje taki film')


def usuń_film():
    movie_name = input("Podaj nazwe filmu do usunięcia ")
    usuń_film_baza_danych(movie_name=movie_name)

def usuń_film():
    wyświetl_wszystkie_filmy()
    movie_name_to_delete = input("Podaj film do usunięcia - ")
    usuń_film_baza_danych(movie_name_to_delete)
#usuń_film()

#----------------------------




#wyświetl_wszystkie_filmy()
# movie_list = session.query(Movie).filter(Movie.category=="Horror").all() WYŚWIETLANIE PO FILTRZE
# movie_list[0].movie_name="Zycie pchora" zamiana
#
# dodaj_film_baza_danych('Kiler','Komedia')
