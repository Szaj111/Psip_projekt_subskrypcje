
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

    if not film_category.strip():
        film_category = "Brak danych"

    if not movies_watched.strip():
        movies_watched = "Brak danych"

    sql_query = sqlalchemy.text("SELECT * FROM my_table WHERE nick=:nick")

    result = connection.execute(sql_query, {'nick': nick}).all()

    if not result:
        dodaj_uzytkownika_bazadanych(name, city, nick, subscription, film_category, movies_watched)
    else:
        print('Podany nick już istnieje')


#dodaj_użytkownika()

def pokaz_liste_uzytkownikow():
    sql_query_1 = sqlalchemy.text(f"SELECT * FROM my_table")
    result= connection.execute(sql_query_1).all()
    for user in result:
     #   print(user[0] + " nick " +user[3]+" jest z miasta "+ user[1] + " liczba jego postów - "+ str(user[2])   )
        print("Informacje na temat użytkownika: " +"Nick: " + user[0] + " Imię: " + user[1], "Rodzaj subskrypcji: "
              + user[3] + " Najczęściej oglądane kategorie: " + user[5] + " Obejrzane filmy: " + user[5])
#pokaz_liste_uzytkownikow()

def usun_uzytkownika_bazadanych(nick):
    query_text = "DELETE FROM public.my_table my_table WHERE  nick = :nick"
    sql_query_1 = sqlalchemy.text(query_text)
    connection.execute(sql_query_1, {'nick':nick})
    connection.commit()

def usun_uzytkownika():
    nick = input ("Podaj nick uzytkownika do usuniecia - ")
    usun_uzytkownika_bazadanych(nick)

#usun_uzytkownika()

def modyfikuj_uzytkownika_bazadanych(nick, new_name, new_city, subscription_type,new_movies_watched, new_film_category):
    query_text = "UPDATE public.my_table SET name = :new_name, city = :new_city, subscription = :subscription_type, movies_watched = :new_movies_watched, film_category = :new_film_category WHERE nick = :nick"
    sql_query_1 = sqlalchemy.text(query_text)
    connection.execute(sql_query_1, {'nick':nick, 'new_name':new_name, 'new_city': new_city, 'subscription_type':subscription_type, 'new_movies_watched': new_movies_watched, 'new_film_category':new_film_category})
    connection.commit()

def modyfikuj_uzytkownika():
    nick = input('Wprowadź nick użytkownika do modyfikacji: ')
    new_name= input("Wprowadz nowe imie: ")
    new_city = input('Wprowadz nowe miasto: ')
    subscription_type = input('Podaj aktualną liczbe postow: ')
    new_movies_watched = input('Podaj nazwe obejrzanego filmu: ')
    new_film_category = input('Podaj kategorie obejrzanych filmów: ')
    modyfikuj_uzytkownika_bazadanych(nick,new_name,new_city,subscription_type, new_movies_watched, new_film_category)
#modyfikuj_uzytkownika()

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
    sql_query_1 = sqlalchemy.text(f"SELECT * FROM my_table WHERE nick = '{nick}'")
    result = connection.execute(sql_query_1).first()
    city_str = result[2]

    city =get_coordinates_of_(city_str)
    map = folium.Map(
        location = city,
        tiles="OpenStreetMap",
        zoom_start=14
    )
    folium.Marker(
       location=city,
       popup=f"Tu rządzi_{result[0]}"
             f"Liczba postów{str(result[2])}"
    ).add_to(map)
    map.save(f"mapka_{result[0]}.html")

get_map_one_user()