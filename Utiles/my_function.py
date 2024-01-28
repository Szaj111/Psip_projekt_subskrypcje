import requests
import folium
import sqlalchemy
from bs4 import BeautifulSoup
from dane import Horrors , Actions , Comedy , Sci_Fictions
from sqlalchemy import func, text, case , select

from orm.ddl import Movie, Base , User, Subscription, Movies_watched
from sqlalchemy.orm import sessionmaker, aliased
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
#Base.metadata.drop_all(bind=engine)
#Base.metadata.create_all(bind=engine)
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
# # # Comedy
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
def usuń_film_baza_danych(session, movie_name):
    while True:
        # Znajdź film o podanej nazwie
        movie = session.query(Movie).filter_by(movie_name=movie_name).first()
        if movie_name == "1":
            break
        if movie:
            # Znajdź subskrypcje powiązane z filmem
            subscriptions_to_delete = session.query(Subscription).filter_by(movie_id=movie.id).all()

            # Usuń powiązane subskrypcje
            for subscription in subscriptions_to_delete:
                session.delete(subscription)

            # Usuń film
            session.delete(movie)
            session.commit()

            print(f'Film {movie_name} został usunięty wraz z powiązanymi subskrypcjami.')
            break
        else:
            print(f'Film {movie_name} nie istnieje')
            movie_name = input('Podaj poprawną nazwę filmu:\n'
                               'Wpisz - 1 aby wyjść\n')
            if movie_name == "1":
                break

# def usuń_film():
#     movie_name = input("Podaj nazwe filmu do usunięcia ")
#     usuń_film_baza_danych(movie_name=movie_name)

def usuń_film():
    wyświetl_wszystkie_filmy()
    movie_name_to_delete = input("Podaj film do usunięcia - ")
    usuń_film_baza_danych(session, movie_name_to_delete)
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

def get_coordinates_of_(city:str)->list[float, float]:

    adres_URL = f'https://pl.wikipedia.org/wiki/{city}'

    response = requests.get(url=adres_URL)
    response_html = BeautifulSoup(response.text,'html.parser')


    response_html_latitude = response_html.select('.latitude')[1].text
    response_html_latitude = float(response_html_latitude.replace(',','.'))

    response_html_longitude = response_html.select('.longitude')[1].text
    response_html_longitude = float(response_html_longitude.replace(',','.'))

    return [response_html_latitude, response_html_longitude]
    print(response_html_latitude, response_html_longitude)


def get_map_one_user():
    nick = input('Podaj nick uzytkownika do generowania mapy - ')
    sql_query_1 = sqlalchemy.text(f"SELECT * FROM user2323 WHERE nick = '{nick}'")
    result = connection.execute(sql_query_1).first()
    city_str = result[4]

    city =get_coordinates_of_(city_str)
    map = folium.Map(
        location = city,
        tiles="OpenStreetMap",
        zoom_start=14
    )
    folium.Marker(
       location=city,
        popup=f"Użytkownik - {result[2]}\n"
              f"Miejscowość - {str(result[4])}\n"
              f"Rodzaj subskrypcji - {result[3]}\n"
    ).add_to(map)
    map.save(f"mapka_{result[1]}.html")

def get_map_of():
    sql_query_1 = sqlalchemy.text("SELECT * FROM user2323")
    result = connection.execute(sql_query_1).all()

    map = folium.Map(
        location=[52.3, 21.0],
        tiles="OpenStreetmap",
        zoom_start=7,
    )

    for user in result:
        city_str = user[4]
        city = get_coordinates_of_(city_str)

        folium.Marker(
            location=city,
            popup= f"Użytkownik: {user[0]}\n"
                   f"Miejscowość: {city_str}\n"
                   f"Rodzaj subskrypcji: {user[3]}\n"
        ).add_to(map)

    map.save('mapka.html')
get_map_of()
def gui_users():
    while True:
        print( f'Menu: \n'
            f'0: Wyjdz \n'
            f'1: Wyświetl uztkowników \n'
            f'2: Dodaj użytkownika \n'
            f'3: Usuń uńytkownika \n'
            f'4: Modyfikuj użytkownika \n'

           )
        menu_option = input("Podaj funkcje do wywołania - ")
        print(f'Wybrano funkcje {menu_option}')

        match menu_option:
            case "0":
                print("Kończę prace")
                break
            case "1":
                print("Wyswietlam użytkowników")
                wyświetl_użytkownika_baza_danych()
            case "2":

                print("Dodaje uzytkownika")
                dodaj_użytkownika()

            case "3":
                print("Usuwam użytkownika")
                usuń_użytkownika()
            case "4":
                print("Modyfikuj użytkownika")
                modyfikuj_użytkownika()


def guisubkrypcje():
    while True:
        print( f'Menu: \n'
            f'0: Wyjdz \n'
            f'1: Wyświetl rodzaje subkrypcji \n'
            f'2: Dodaj rodzaj subkrypcji \n'
            f'3: Usuń subkrypcje \n'
            f'4: Modyfikuj subkrypcje \n'
           )
        menu_option = input("Podaj funkcje do wywołania - ")
        print(f'Wybrano funkcje {menu_option}')

        match menu_option:
            case "0":
                print("Kończę prace")
                break
            case "1":
                print("Wyswietlam rodzaje subkrypcjj")
                wyswietl_dostepne_subskrypcje()
            case "2":
                print("Dodaje subkrypcje")
                dodaj_film()
            case "3":
                print("Usuwam subkrypcje")
                usun_subskrypcje()
            case "4":
                print("Modyfikuje subkrypcje")
                zmien_typ_subskrypcji()

#sub_gui()
def gui_movies():
    while True:
        print( f'Menu: \n'
            f'0: Wyjdz \n'
            f'1: Wyświetl filmy \n'
            f'2: Dodaj film \n'
            f'3: Usuń film \n'
            f'4: Modyfikuj film \n'
           )
        menu_option = input("Podaj funkcje do wywołania - ")
        print(f'Wybrano funkcje {menu_option}')

        match menu_option:
            case "0":
                print("Kończę prace")
                break
            case "1":
                print("Wyswietlam filmy: ")
                wyświetl_wszystkie_filmy()
            case "2":
                print("Dodaje film: ")
                dodaj_film()
            case "3":
                print("Usuwam film")
                usuń_film()
            case "4":
                print("Modyfikuje film")
                modyfikuj_film()
#movies_gui()

def gui_users_sub_():
    while True:
        print( f'Menu: \n'
            f'0: Wyjdz \n'
            f'1: Wyświetl użytkownika o danej subkrypcji \n'
            f'2: Dodaj użytkownika \n'
            f'3: Usuń użytkownika o danej subkrypcji \n'
            f'4: Modyfikuj użytkownika o danej subkrypcji \n'
           )
        menu_option = input("Podaj funkcje do wywołania - ")
        print(f'Wybrano funkcje {menu_option}')

        match menu_option:
            case "0":
                print("Kończę prace")
                break
            case "1":
                print("Wyswietlam użytkowników o danej subkrypcji: ")
                wyświetl_użytkownika_subkrypcja()
            case "2":
                print("Dodaje użytkownika: ")
                dodaj_użytkownika()
            case "3":
                print("Usuwam użytkownika o danej subkrypcji")
                usun_uzytkownika_z_subskrypcji()
            case "4":
                print("Modyfikuje użytkownika o danej subkrypcji")
                modyfikuj_uzytkownika_po_subskrypcji()

# CRUD OBEJRZAL KLIENT \/
def dodaj_obejrzany_film_baza_danych(session, user, movie, category=None):
    watched_movie = Movies_watched(movie=movie, user=user, category=category)
    session.add(watched_movie)
    session.commit()

def dodaj_obejrzany_film():
    nick = input("Podaj nick użytkownika, który obejrzał film: ")
    movie_name = input("Podaj film, który obejrzał: ")
    category = input("Podaj kategorię obejrzanego filmu: ")
    user = session.query(User).filter_by(nick=nick).first()
    movie = session.query(Movie).filter_by(movie_name=movie_name).first()

    if user and movie:
        dodaj_obejrzany_film_baza_danych(session, user, movie, category=category)
    else:
        print("Użytkownik lub film nie istnieje.")

def usuń_obejrzany_film(movie):
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
# usuń_użytkownika()

def usun_film_obejrzany_z_bazy_danych(session, user, movie):
    obejrzany_film = session.query(Movies_watched).filter_by(user=user, movie=movie).first()

    if obejrzany_film:
        session.delete(obejrzany_film)
        session.commit()
        print("Film został usunięty z listy obejrzanych.")
    else:
        print("Podany film nie jest na liście obejrzanych użytkownika.")

def usun_film_obejrzany():
    nick = input("Podaj nick użytkownika, któremu chcesz usunąć film: ")
    nazwa_filmu = input("Podaj nazwę filmu, który chcesz usunąć: ")

    uzytkownik = session.query(User).filter_by(nick=nick).first()
    film = session.query(Movie).filter_by(movie_name=nazwa_filmu).first()

    if uzytkownik and film:
        usun_film_obejrzany_z_bazy_danych(session, uzytkownik, film)
    else:
        print("Użytkownik lub film nie istnieje.")


#usun_film_obejrzany()

def wyswietl_liste_filmow_obejrzanych_baza_danych(session, user):
    filmy_obejrzane = session.query(Movies_watched).filter_by(user=user).all()

    if filmy_obejrzane:
        print(f"Lista filmów obejrzanych przez użytkownika {user.nick}:")
        for film in filmy_obejrzane:
            print(f"Film: {film.movie.movie_name}, Kategoria: {film.category}")
    else:
        print(f"Użytkownik {user.nick} nie obejrzał jeszcze żadnych filmów.")

#Klientow ktorzy obejrzeli dany film \/
def wyswietl_liste_filmow_obejrzanych_dla_uzytkownika():
    wyświetl_użytkownika_baza_danych()
    nick = input("Podaj nick użytkownika, którego listę filmów obejrzanych chcesz wyświetlić: ")
    uzytkownik = session.query(User).filter_by(nick=nick).first()

    if uzytkownik:
        wyswietl_liste_filmow_obejrzanych_baza_danych(session, uzytkownik)
    else:
        print("Użytkownik o podanym nicku nie istnieje.")

#wyswietl_liste_filmow_obejrzanych_dla_uzytkownika()

def modyfikuj_obejrzany_film_baza_danych(session, user, movie, nowa_nazwa=None, nowa_kategoria=None):
    watched_movie = session.query(Movies_watched).filter_by(user=user, movie_id=movie.id).first()

    if watched_movie:
        if nowa_nazwa is not None:
            watched_movie.movie.movie_name = nowa_nazwa
        if nowa_kategoria is not None:
            watched_movie.category = nowa_kategoria
            watched_movie.movie.category = nowa_kategoria
        session.commit()
        print("Film został pomyślnie zaktualizowany.")
    else:
        print("Użytkownik nie obejrzał jeszcze tego filmu.")


def modyfikuj_obejrzane_filmy():
    nick = input("Podaj nick użytkownika, którego filmy chcesz zaktualizować: ")

    user = session.query(User).filter_by(nick=nick).first()

    if user:

        watched_movies = session.query(Movies_watched).filter_by(user=user).all()

        if watched_movies:

            print(f"Filmy obejrzane przez użytkownika {nick}:")
            for idx, watched_movie in enumerate(watched_movies, start=1):
                print(f"{idx}. {watched_movie.movie.movie_name}")

            # Wybierz numer filmu do modyfikacji
            movie_choice = int(input("Podaj numer filmu do zaktualizowania: "))

            if 1 <= movie_choice <= len(watched_movies):
                selected_movie = watched_movies[movie_choice - 1]

                nowa_nazwa = input("Podaj nową nazwę filmu (jeśli chcesz ją zmienić): ")
                nowa_kategoria = input("Podaj nową kategorię filmu (jeśli chcesz ją zmienić): ")

                modyfikuj_obejrzany_film_baza_danych(session, user, selected_movie.movie, nowa_nazwa, nowa_kategoria)
            else:
                print("Nieprawidłowy numer filmu.")
        else:
            print("Użytkownik nie obejrzał jeszcze żadnych filmów.")
    else:
        print("Użytkownik o podanym nicku nie istnieje.")

#modyfikuj_obejrzane_filmy()


def wyswietl_uzytkownikow_ktorzy_obejrzeli_film_baza_danych(session, movie_name):
    query = session.query(User).join(Movies_watched).join(Movie).filter(Movie.movie_name == movie_name)
    users = query.all()

    if users:
        print(f"Lista użytkowników, którzy obejrzeli film '{movie_name}':")
        for user in users:
            print(f"- {user.nick}")
    else:
        print(f"Brak danych o użytkownikach, którzy obejrzeli film '{movie_name}'.")

def wyswietl_uzytkownikow_ktorzy_obejrzeli_film():
    movie_name = input("Podaj film aby wyświetlić użytkowników, którzy go oglądali: ")
    wyswietl_uzytkownikow_ktorzy_obejrzeli_film_baza_danych(session, movie_name)

#wyswietl_uzytkownikow_ktorzy_obejrzeli_film()

def dodaj_uzytkownika_ktory_obejrzal_film_baza_danych(session, user, movie):
    # Sprawdzenie, czy użytkownik już obejrzał ten film
    existing_entry = session.query(Movies_watched).filter_by(user=user, movie=movie).first()

    if not existing_entry:
        new_entry = Movies_watched(movie=movie, user=user)
        session.add(new_entry)
        session.commit()
        print(f"Użytkownik {user.nick} został dodany do listy obejrzanych filmów.")
    else:
        print(f"Użytkownik {user.nick} już obejrzał ten film.")

def dodaj_uzytkownika_ktory_obejrzal_film_baza_danych(session, user, movie, category=None):
    existing_entry = session.query(Movies_watched).filter_by(user=user, movie=movie).first()

    if not existing_entry:

        if category is None and movie.category:
            category = movie.category

        new_entry = Movies_watched(movie=movie, user=user, category=category)
        session.add(new_entry)
        session.commit()
        print(f"Użytkownik {user.nick} został dodany do listy obejrzanych filmów.")
    else:
        print(f"Użytkownik {user.nick} już obejrzał ten film.")

def dodaj_uzytkownika_ktory_obejrzal_film():
    nick = input("Podaj nick użytkownika, który obejrzał film: ")
    movie_name = input("Podaj nazwę filmu, który został obejrzany: ")

    user = session.query(User).filter_by(nick=nick).first()
    movie = session.query(Movie).filter_by(movie_name=movie_name).first()

    if user and movie:
        category = input(f"Podaj kategorię filmu (opcjonalnie, naciśnij Enter, aby użyć kategorii '{movie.category}'): ")
        if not category and movie.category:
            category = movie.category

        dodaj_uzytkownika_ktory_obejrzal_film_baza_danych(session, user, movie, category)
    else:
        print("Użytkownik lub film nie istnieje.")


def usun_uzytkownika_z_obejrzanych_filmow_baza_danych(session, movie_name):
    movie = session.query(Movie).filter_by(movie_name=movie_name).first()

    if movie:
        users_watched_movie = session.query(User).join(Movies_watched).filter_by(movie=movie).all()

        if users_watched_movie:
            print(f"Lista użytkowników, którzy obejrzeli film '{movie_name}':")
            for idx, user in enumerate(users_watched_movie, start=1):
                print(f"{idx}. {user.nick}")

            user_choice = int(input("Wybierz numer użytkownika do usunięcia: "))

            if 1 <= user_choice <= len(users_watched_movie):
                selected_user = users_watched_movie[user_choice - 1]

                watched_movie = session.query(Movies_watched).filter_by(user=selected_user, movie=movie).first()

                if watched_movie:
                    session.delete(watched_movie)
                    session.commit()
                    print("Użytkownik został pomyślnie usunięty z obejrzanych filmów.")
                else:
                    print("Użytkownik nie obejrzał jeszcze tego filmu.")
            else:
                print("Nieprawidłowy numer użytkownika.")
        else:
            print("Brak użytkowników, którzy obejrzeli ten film.")
    else:
        print(f"Film o nazwie '{movie_name}' nie istnieje.")


def usun_uzytkownika_z_obejrzanych_filmow():
    movie_name = input("Podaj nazwę filmu, dla którego chcesz usunąć użytkownika z listy obejrzanych filmów: ")

    usun_uzytkownika_z_obejrzanych_filmow_baza_danych(session, movie_name)



def modyfikuj_uzytkownika_z_obejrzanych_filmow_baza_danych(session, movie_name, new_nick):

    movie = session.query(Movie).filter_by(movie_name=movie_name).first()

    if movie:

        users_watched_movie = session.query(User).join(Movies_watched).filter_by(movie=movie).all()

        if users_watched_movie:

            print("Lista użytkowników, którzy obejrzeli film:")
            for idx, user in enumerate(users_watched_movie, start=1):
                print(f"{idx}. {user.nick}")


            user_choice = int(input("Wybierz numer użytkownika do modyfikacji: "))
            selected_user = users_watched_movie[user_choice - 1]


            selected_user.nick = new_nick


            session.commit()
            print("Informacje o użytkowniku zostały pomyślnie zaktualizowane.")
        else:
            print("Brak użytkowników, którzy obejrzeli ten film.")
    else:
        print(f"Film o nazwie '{movie_name}' nie istnieje.")

def modyfikuj_uzytkownika_z_obejrzanych_filmow():
    movie_name = input("Podaj nazwę filmu, dla którego będziemy modyfikować użytkownika: ")
    new_nick = input("Podaj nowy nick użytkownika: ")

    modyfikuj_uzytkownika_z_obejrzanych_filmow_baza_danych(session, movie_name, new_nick)



# guisubkrypcje()


def gui_filmów_obejrzanych_przez_użytkownika(): # poprawic zmiane filmu (nie zmienia sie kategoria)
    while True:
        print( f'Menu: \n'
            f'0: Wyjdz \n'
            f'1: Wyświetl obejrzane filmy \n'
            f'2: Dodaj obejrzane filmy \n'
            f'3: Usuń obejrzany film \n'
            f'4: Modyfikuj obejrzany film \n'
           )
        menu_option = input("Podaj funkcje do wywołania - ")
        print(f'Wybrano funkcje {menu_option}')

        match menu_option:
            case "0":
                print("Kończę prace")
                break
            case "1":
                print("Wyswietlam użytkowników o danej subkrypcji: ")
                wyswietl_liste_filmow_obejrzanych_dla_uzytkownika()
            case "2":
                print("Dodaje użytkownika: ")
                dodaj_obejrzany_film()
            case "3":
                print("Usuwam użytkownika o danej subkrypcji")
                usun_film_obejrzany()
            case "4":
                print("Modyfikuje użytkownika o danej subkrypcji")
                modyfikuj_obejrzane_filmy()

def gui_klientow_ktorzy_obejrzali_dany_film():
    while True:
        print( f'Menu: \n'
            f'0: Wyjdz \n'
            f'1: Wyświetl użytkownika który obejrzał dany film \n'
            f'2: Dodaj użytkownika,który obejrzał dany film \n'
            f'3: Usuń użytkownika,który obejrzał dany film \n'
            f'4: Modyfikuj użytkownika,który obejrzał dany film \n'
           )
        menu_option = input("Podaj funkcje do wywołania - ")
        print(f'Wybrano funkcje {menu_option}')

        match menu_option:
            case "0":
                print("Kończę prace")
                break
            case "1":
                print("Wyswietlam użytkowników,którzy obejrzał dany film")
                wyswietl_uzytkownikow_ktorzy_obejrzeli_film()
            case "2":
                print("Dodaje użytkownika,który obejrzał dany film ")
                dodaj_uzytkownika_ktory_obejrzal_film()
            case "3":
                print("Usuwam użytkownika,który obejrzał dany film z tabeli obejrzanych filmów: ")
                usun_uzytkownika_z_obejrzanych_filmow()
            case "4":
                print("Modyfikuje użytkownika,który obejrzał dany film")
                modyfikuj_uzytkownika_z_obejrzanych_filmow()




# gui()

def get_map_for_movie_baza_danych(movie_name: str):
    user_alias = aliased(User)
    movie_alias = aliased(Movie)

    result = (
        session.query(user_alias)
        .distinct()
        .join(Movies_watched, user_alias.id == Movies_watched.user_id)
        .join(movie_alias, Movies_watched.movie_id == movie_alias.id)
        .filter(movie_alias.movie_name == movie_name)
        .all()
    )

    if result:
        map = folium.Map(
            location=[52.3, 21.0],
            tiles="OpenStreetmap",
            zoom_start=7,
        )

        for user in result:
            city_str = user.city
            city = get_coordinates_of_(city_str)

            folium.Marker(
                location=city,
                popup=f"Użytkownik: {user.nick}\n"
                      f"Miejscowość: {city_str}\n"
                      f"Rodzaj subskrypcji: {user.subscription}\n"
            ).add_to(map)

        map.save(f'mapka_{movie_name}.html')
        print(f"Mapa dla użytkowników, którzy obejrzeli film '{movie_name}' została wygenerowana.")
    else:
        print(f"Brak użytkowników, którzy obejrzeli film '{movie_name}'.")

def get_map_for_movie():
    film = input("Podaj film do generacji mapy użytkowników, którzy go widzieli: ")
    get_map_for_movie_baza_danych(film)


def get_map_for_category_baza_danych(category_name: str):
    user_alias = aliased(User)
    movie_alias = aliased(Movie)

    result = (
        session.query(user_alias)
        .distinct()
        .join(Movies_watched, user_alias.id == Movies_watched.user_id)
        .join(movie_alias, Movies_watched.movie_id == movie_alias.id)
        .filter(sqlalchemy.and_(movie_alias.category == category_name, Movies_watched.category == category_name))
        .all()
    )

    if result:
        map = folium.Map(
            location=[52.3, 21.0],
            tiles="OpenStreetmap",
            zoom_start=7,
        )

        for user in result:
            city_str = user.city
            city = get_coordinates_of_(city_str)

            folium.Marker(
                location=city,
                popup=f"Użytkownik: {user.nick}\n"
                      f"Miejscowość: {city_str}\n"
                      f"Rodzaj subskrypcji: {user.subscription}\n"
            ).add_to(map)

        map.save(f'mapka_{category_name}.html')
        print(f"Mapa dla użytkowników, którzy obejrzeli filmy z kategorii '{category_name}' została wygenerowana.")
    else:
        print(f"Brak użytkowników, którzy obejrzeli filmy z kategorii '{category_name}'.")

def get_map_for_category():
    category = input("Podaj kategorię filmu do generacji mapy użytkowników, którzy go widzieli: ")
    get_map_for_category_baza_danych(category)


def get_map_for_subscription_baza_danych(subscription_name: str):
    user_alias = aliased(User)
    movie_alias = aliased(Movie)

    result = (
        session.query(user_alias)
        .distinct()
        .join(Movies_watched, user_alias.id == Movies_watched.user_id)
        .join(movie_alias, Movies_watched.movie_id == movie_alias.id)
        .filter(sqlalchemy.and_(user_alias.subscription == subscription_name, Movies_watched.category == movie_alias.category))
        .all()
    )

    if result:
        map = folium.Map(
            location=[52.3, 21.0],
            tiles="OpenStreetmap",
            zoom_start=7,
        )

        for user in result:
            city_str = user.city
            city = get_coordinates_of_(city_str)

            folium.Marker(
                location=city,
                popup=f"Użytkownik: {user.nick}\n"
                      f"Miejscowość: {city_str}\n"
                      f"Rodzaj subskrypcji: {user.subscription}\n"
            ).add_to(map)

        map.save(f'mapka_{subscription_name}.html')
        print(f"Mapa dla użytkowników, którzy obejrzeli filmy z subskrypcji '{subscription_name}' została wygenerowana.")
    else:
        print(f"Brak użytkowników, którzy obejrzeli filmy z subskrypcji '{subscription_name}'.")

def get_map_for_subscription():
    subscription = input("Podaj subskrypcję użytkowników do generacji mapy: ")
    get_map_for_subscription_baza_danych(subscription)

# get_map_for_subscription()




def gui_maps():
    while True:
        print( f'Menu: \n'
            f'0: Wyjdź \n'
            f'1: Wyświetl mape wybranego użytkownka \n'
            f'2: Wyświetl mape wszystkich użytkowników \n'
            f'3: Wyświetl mape użytkowników, którzy widzieli dany film:  \n'
            f'4: Wyświetl mape użytkowników, którzy widzieli daną kategorie \n'
            f'5: Wyświetl mape użytkowników danej subkrypcji \n'
           )
        menu_option = input("Podaj funkcje do wywołania - ")
        print(f'Wybrano funkcje {menu_option}')

        match menu_option:
            case "0":
                print("Kończę prace")
                break
            case "1":
                print("Wyswietlam mape wybranego użytkownka:")
                get_map_one_user()
            case "2":
                print("mape wszystkich użytkowników:")
                get_map_of()
            case "3":
                print("mape użytkowników, którzy widzieli dany film:")
                get_map_for_movie()
            case "4":
                print("Wyświetl mape użytkowników, którzy widzieli daną kategorie: ")
                get_map_for_category()
            case "5":
                print("Wyświetl mape użytkowników danej subkrypcji: ")
                get_map_for_subscription()

#gui_maps()


def gui():
    while True:
        print( f'Menu: \n'
            f'0: Wyjdź \n'
            f'1: Wyświetl menu użytkownika \n'
            f'2: Wyświetl menu filmów \n'
            f'3: Wyświetl menu subkrypcji \n'
            f'4: Wyświetl menu klientów, ktorzy obejrzeli dany film \n'
            f'5: Wyświetl menu filmów, ktory obejrzał dany klient \n'
            f'6: Wyświetl menu generowania map \n'
           )
        menu_option = input("Podaj funkcje do wywołania - ")
        print(f'Wybrano funkcje {menu_option}')

        match menu_option:
            case "0":
                print("Kończę prace")
                break
            case "1":
                print("Wyswietlam menu użytkownika:")
                gui_users()
            case "2":
                print("Wyświetl menu filmów:")
                gui_movies()
            case "3":
                print("Wyświetl menu subkrypcji:")
                guisubkrypcje()
            case "4":
                print("Wyświetl menu klientów, ktorzy obejrzeli dany film")
                gui_klientow_ktorzy_obejrzali_dany_film()
            case "5":
                print("Wyświetl menu filmów, ktory obejrzał dany klient")
                gui_filmów_obejrzanych_przez_użytkownika()
            case "6":
                print("Wyświetl menu generowania map")
                gui_maps()

gui()