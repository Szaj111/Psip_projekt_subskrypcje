import requests
import folium
import sqlalchemy
from bs4 import BeautifulSoup
from dane import Horrors , Actions , Comedy , Sci_Fictions
from sqlalchemy import func, text, case

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
# Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

#--------dodawanie filmów GIT------------
def dodaj_film_baza_danych(movie_name, category):
    movie = Movie(movie_name=movie_name, category=category)
    session.add(movie)
    session.commit()
    dodaj_subkrypcje_baza_danych(movie.id)

def dodaj_subkrypcje_baza_danych(movie_id):
    subscription_type = input("Typ subskrypcji: ")
    subscription = Subscription(subscription=subscription_type, movie_id=movie_id)
    session.add(subscription)
    session.commit()


def wyswietl_dostepne_subskrypcje():
    subscriptions = (
        session.query(
            Subscription.subscription,
            Movie.category,
            func.STRING_AGG(Movie.movie_name, ', ').label('film_names')
        )
        .outerjoin(Movie, Subscription.movie_id == Movie.id)
        .group_by(Subscription.subscription, Movie.category)
        .order_by(Subscription.subscription, Movie.category)
        .all()
    )

    current_subscription = None

    for subscription, category, film_names in subscriptions:
        if subscription != current_subscription:
            if current_subscription is not None:
                print('\n' + '-' * 50)  # oddzielanie roznych subrypcji
            print(f"Subskrypcja: {subscription}")
            current_subscription = subscription

        if category:
            print(f"  Kategoria: {category}, Filmy: {film_names}")
        else:
            print(f"  Kategoria: Brak przypisanego filmu")

#wyswietl_dostepne_subskrypcje()
def usun_subskrypcje_baza_danych(subscription_name):
    subscriptions = session.query(Subscription).filter_by(subscription=subscription_name).all()

    if subscriptions:
        for subscription in subscriptions:
            session.delete(subscription)
        session.commit()
        print(f"Wszystkie subskrypcje o nazwie {subscription_name} zostały usunięte.")
    else:
        print(f"Nie znaleziono subskrypcji o nazwie {subscription_name}.")


def usun_subskrypcje():
    wyswietl_dostepne_subskrypcje()
    sub_to_delete = input("Podaj subskrypcje do usunięcia: ")
    usun_subskrypcje_baza_danych(sub_to_delete)

def zmien_typ_subskrypcji_baza_danych(subscription_name, nowy_typ):
    subscriptions = session.query(Subscription).filter_by(subscription=subscription_name).all()

    if subscriptions:
        for subscription in subscriptions:
            subscription.subscription = nowy_typ
        session.commit()
        print(f"Wszystkie subskrypcje o nazwie {subscription_name} zostały zmienione na {nowy_typ}.")
    else:
        print(f"Nie znaleziono subskrypcji o nazwie {subscription_name}.")

def zmien_typ_subskrypcji():
    wyswietl_dostepne_subskrypcje()
    nazwa_subkrypcji = input("Podaj nazwę subkrypcji, której chcesz zmienić typ: ")
    nowy_typ = input("Podaj nowy typ subkrypcji: ")
    zmien_typ_subskrypcji_baza_danych(nazwa_subkrypcji, nowy_typ)
    wyswietl_dostepne_subskrypcje()
#zmien_typ_subskrypcji()


def dodaj_film():
    movie_name = input("Nazwa filmu: ")
    category = input("Nazwa kategori:")
    dodaj_film_baza_danych(movie_name, category)
#dodaj_film()

#dodaj_film()
#^ działa


# # Horrors
# for horror_movie in Horrors:
#     nazwa = horror_movie.get("movie_name")
#     kategoria = "Horror"
#     dodaj_film_baza_danych(nazwa, kategoria)
#
# Actions
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

    user_to_change = input("Podaj nick użytkownika do zamiany -  ")
    user = session.query(User).filter_by(nick=user_to_change).first()

    if user:
        nowe_imie = input("Podaj nowe imię: ")
        nowa_subskrypcja = input("Podaj nazwę subskrypcji: ")
        nowe_miasto = input("Podaj nazwę nowego miasta: ")

        user.name = nowe_imie
        user.subscription = nowa_subskrypcja
        user.city = nowe_miasto

        session.commit()
        print(f'Imię użytkownika {user_to_change} zostało zmienione na {nowe_imie}.')
        print(f'Subskrypcja użytkownika {user_to_change} została zmieniona na {nowa_subskrypcja}.')
        print(f'Miasto użytkownika {user_to_change} zostało zmienione na {nowe_miasto}.')
    else:
        print(f'Nie ma takiego użytkownika o nicku {user_to_change}.')
#modyfikuj_użytkownika()

#-------------------- CRUD uzytkownikow na podstawie subkrypcji
def wyświetl_użytkownika_subkrypcja_baza_danych(subscription_name):

    users = session.query(User).filter_by(subscription=subscription_name).all()
    if users:
        print(f'Użytkownicy o subskrypcji {subscription_name}:')
        for user in users:
            print(f'Nick: {user.nick}, Imię: {user.name}, Miasto: {user.city}')
    else:
        print(f'Nie znaleziono użytkowników o subskrypcji {subscription_name}.')
def wyświetl_użytkownika_subkrypcja():
    nazwa_sub = input("Podaj nazwe subkrypcji")
    wyświetl_użytkownika_subkrypcja_baza_danych(nazwa_sub)
#wyświetl_użytkownika_subkrypcja()
def usun_uzytkownika_z_subskrypcji_baza_danych(subscription_name, nick_to_delete):
    user_to_delete = session.query(User).filter_by(subscription=subscription_name, nick=nick_to_delete).first()

    if user_to_delete:
        session.delete(user_to_delete)
        session.commit()
        print(f'Użytkownik o nicku {nick_to_delete} został usunięty z subskrypcji {subscription_name}.')
    else:
        print(f'Nie znaleziono użytkownika o nicku {nick_to_delete} i subskrypcji {subscription_name}.')

def usun_uzytkownika_z_subskrypcji():
    wyświetl_użytkownika_baza_danych()
    sub_to_delete = input("Podaj nazwe subkrypcji: ")
    user_to_delete = input("Podaj nick użytkownika do usunięcia: ")
    usun_uzytkownika_z_subskrypcji_baza_danych(sub_to_delete, user_to_delete)
    wyświetl_użytkownika_baza_danych()

def modyfikuj_uzytkownika_po_subskrypcji_baza_danych(subscription_name):
    users = session.query(User).filter_by(subscription=subscription_name).all()

    if users:
        print(f'Użytkownicy o subskrypcji {subscription_name}:')
        for user in users:
            print(f'Nick: {user.nick}, Imię: {user.name}, Miasto: {user.city}')

        nick_to_edit = input("Podaj nick użytkownika do edycji: ")
        user_to_edit = session.query(User).filter_by(subscription=subscription_name, nick=nick_to_edit).first()

        if user_to_edit:
            nowe_imie = input("Podaj nowe imię: ")
            nowe_miasto = input("Podaj nowe miasto: ")

            user_to_edit.name = nowe_imie
            user_to_edit.city = nowe_miasto

            session.commit()
            print(f'Dane użytkownika o nicku {nick_to_edit} zostały zaktualizowane.')
        else:
            print(f'Nie znaleziono użytkownika o nicku {nick_to_edit} i subskrypcji {subscription_name}.')
    else:
        print(f'Nie znaleziono użytkowników o subskrypcji {subscription_name}.')


def modyfikuj_uzytkownika_po_subskrypcji():
    wyświetl_użytkownika_baza_danych()
    sub = input("Podaj subkrypcje użytkownika do zamiany: ")
    modyfikuj_uzytkownika_po_subskrypcji_baza_danych(sub)
    wyświetl_użytkownika_baza_danych()
#modyfikuj_uzytkownika_po_subskrypcji()