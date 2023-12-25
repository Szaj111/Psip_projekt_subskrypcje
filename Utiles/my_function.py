
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
#dodawanie uzytkownika
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
        dodaj_użytkownika()
#WYSWIETLANIE LISTY UZYTKOWNIKOW
def pokaz_liste_uzytkownikow():
    sql_query_1 = sqlalchemy.text(f"SELECT * FROM my_table")
    result= connection.execute(sql_query_1).all()
    for user in result:
     #   print(user[0] + " nick " +user[3]+" jest z miasta "+ user[1] + " liczba jego postów - "+ str(user[2])   )
        print("Informacje na temat użytkownika: " +"Nick: " + user[0] + " Imię: " + user[1], "Rodzaj subskrypcji: " +"Miejscowość: " +user[2]
              + user[3] + " Najczęściej oglądane kategorie: " + user[5] + " Obejrzane filmy: " + user[5])


#usuwanie
def usun_uzytkownika_bazadanych(nick):
    query_text = "DELETE FROM public.my_table my_table WHERE  nick = :nick"
    sql_query_1 = sqlalchemy.text(query_text)
    connection.execute(sql_query_1, {'nick':nick})
    connection.commit()

def usun_uzytkownika():
    nick = input ("Podaj nick uzytkownika do usuniecia - ")
    usun_uzytkownika_bazadanych(nick)

# Modyfikacja uzytkownika
def modyfikuj_uzytkownika_bazadanych(nick, new_name, new_city, subscription_type,new_movies_watched, new_film_category):
    query_text = "UPDATE public.my_table SET name = :new_name, city = :new_city, subscription = :subscription_type, movies_watched = :new_movies_watched, film_category = :new_film_category WHERE nick = :nick"
    sql_query_1 = sqlalchemy.text(query_text)
    connection.execute(sql_query_1, {'nick':nick, 'new_name':new_name, 'new_city': new_city, 'subscription_type':subscription_type, 'new_movies_watched': new_movies_watched, 'new_film_category':new_film_category})
    connection.commit()

def modyfikuj_uzytkownika():
    nick = input('Wprowadź nick użytkownika do modyfikacji: ')
    new_name= input("Wprowadz nowe imie: ")
    new_city = input('Wprowadz nowe miasto: ')
    subscription_type = input('Podaj typ subskrypcji: ')
    new_movies_watched = input('Podaj nazwe obejrzanego filmu: ')
    new_film_category = input('Podaj kategorie obejrzanych filmów: ')
    modyfikuj_uzytkownika_bazadanych(nick,new_name,new_city,subscription_type, new_movies_watched, new_film_category)
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
        popup=f"Użytkownik - {result[0]}\n"
              f"Miejscowość - {str(result[2])}\n"
              f"Rodzaj subskrypcji - {result[3]}\n"
    ).add_to(map)
    map.save(f"mapka_{result[0]}.html")

def get_map_of():
    sql_query_1 = sqlalchemy.text("SELECT * FROM my_table")
    result = connection.execute(sql_query_1).all()

    map = folium.Map(
        location=[52.3, 21.0],
        tiles="OpenStreetmap",
        zoom_start=7,
    )

    for user in result:
        city_str = user[2]
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
                pokaz_liste_uzytkownikow()
            case "2":
                print("Dodaje użytkownika")
                dodaj_użytkownika()
            case "3":
                print("Usuwam użytkownika")
                usun_uzytkownika()
            case "4":
                print("Modyfikuj użytkownika")
                modyfikuj_uzytkownika()
            case '5':
                print('Rysuję mape z użytkownikiem')
                get_map_one_user()

            case '6':
                print("Rysuje mape z użytkownikami")
                get_map_of()