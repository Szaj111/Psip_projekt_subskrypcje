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
#Base.metadata.drop_all(bind=engine)
#Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

def dodaj_film_baza_danych(movie_name,category):
    movie = Movie(movie_name=movie_name,category=category)
    session.add(movie)
    session.commit()
def dodaj_film():
    movie_name = input("Nazwa filmu: ")
    category = input("Nazwa kategori:")
    dodaj_film_baza_danych(movie_name,category)
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

def wyświetl_wszystkie_filmy():
    movie_list = session.query(Movie).all()
    session.commit()
    for movie in movie_list:
        print(movie.movie_name +str(" -"), movie.category)

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
def usuń_film():
    wyświetl_wszystkie_filmy()
    movie_name_to_delete = input("Podaj film do usunięcia - ")
    usuń_film_baza_danych(movie_name_to_delete)
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
    wyświetl_użytkownika_baza_danych()
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


def gui(users_list:list)->None:
    while True:
        print( f'Menu: \n'
            f'0: Wyjdz \n'
            f'1: Wyświetl uztkowników \n'
            f'2: Dodaj użytkownika \n'
            f'3: Usuń uńytkownika \n'
            f'4: Modyfikuj użytkownika \n'
            f'5: Wygeneruj mape z użytkownikiem \n'
            f'6: Wygeneruj mape z użytkownikami \n'
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
                usuń_film()
            case "4":
                print("Modyfikuj użytkownika")
                modyfikuj_użytkownika()
            case '5':
                print('Rysuję mape z użytkownikiem')
                get_map_one_user()

            case '6':
                print("Rysuje mape z użytkownikami")
                get_map_of()

