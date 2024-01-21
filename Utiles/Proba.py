import requests
import folium
import sqlalchemy
from bs4 import BeautifulSoup
from dane import Horrors , Actions , Comedy , Sci_Fictions







from orm.ddl import Movie, Base , User, Subscription
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
Base.metadata.create_all(bind=engine)
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


# # Horrors
# for horror_movie in Horrors:
#     nazwa = horror_movie.get("movie_name")
#     kategoria = "Horror"
#     dodaj_film_baza_danych(nazwa, kategoria)
#
# # Actions
# for action_movie in Actions:
#     nazwa = action_movie.get("movie_name")
#     kategoria = "Action"
#     dodaj_film_baza_danych(nazwa, kategoria)
#
# # Comedy
# for comedy_movie in Comedy:
#     nazwa = comedy_movie.get("movie_name")
#     kategoria = "Comedy"
#     dodaj_film_baza_danych(nazwa, kategoria)
#
# # Sci_Fictions
# for sci_fi_movie in Sci_Fictions:
#     nazwa = sci_fi_movie.get("movie_name")
#     kategoria = "Sci-Fi"
#     dodaj_film_baza_danych(nazwa, kategoria)





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

dodaj_film_baza_danych("Mission: Impossible","Actions")

def dodaj_rodzaj_subskrypcji_baza_danych(subcricption):
    sub = Subscription(subcription=subcricption,)
    session.add(sub)
    session.commit()




#---------------dodawanie użytkowniak_________
def dodaj_użytkownika_baza_danych(nick, name, subscription, city):
    user = User(nick=nick, name=name, subscription=subscription, city= city)
    session.add(user)
    session.commit()
def dodaj_użytkownika():
    nick = input('Podaj nick użytkownika: ')
    name = input('Podaj imie uzytkwonika: ')
    subscription = input('Podaj subskrypcje uzytkownika: ')
    city = input('Podaj miasto uzytkownika: ')
    dodaj_użytkownika_baza_danych(nick, name, subscription, city)
#dodaj_użytkownika()

def wyświetl_użytkownika_baza_danych():
    users_list =session.query(User).all()
    session.commit()
    for user in users_list:
        print("Nick: " + user.nick,"Imię: " + user.name,"Subskrypcja: " + user.subscription, "Miasto: " + user.city)
#wyświetl_dodaj_użytkownika_baza_danych()
def usuń_użytkownika_baza_danych(nick):
    while True:
        nick_del = session.query(User).filter_by(nick=nick).first()
        if nick == "1":
            break
        if nick_del:
            session.delete(nick_del)
            session.commit()
            print(f'Użytkownik {nick} został usunięty')
            break
        else:
            print(f'Użytkownik {nick} nie istnieje')
            nick = input('Podaj poprawna nazwe filmu: \n'
                  'Wpisz - 1 aby wyjść \n')
            if nick == "1":
                break
def usuń_użytkownika():
    wyświetl_użytkownika_baza_danych()
    user_to_delete = input("Podaj nick użytkownika do usunięcia - ")
    usuń_użytkownika_baza_danych(user_to_delete)
#usuń_użytkownika()
def modyfikuj_użytkownika():
    wyświetl_użytkownika_baza_danych()
