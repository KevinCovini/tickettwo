import pymongo as pm
from pymongo import MongoClient
import geojson
import geopy
from geopy.geocoders import Nominatim
from datetime import datetime

# Geocoder object
geolocator = Nominatim(user_agent="my_geocoder")

# Connection to MongoDB cluster "KCluster"
uri = "mongodb+srv://kcovini:admin@kcluster.vg9adfo.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db_tickettwo = client["TicketTwo"]
collection_concerts = db_tickettwo["Concerts"]
collection_sales = db_tickettwo["Sales"]

# Connection check
try:
    client.admin.command('ping')
    print("Connection successful!")
except Exception as e:
    print(e)

TEMPLATE_CONCERTO = {
    "name": "TZN 2023",
    "desc": "Concerto di Tiziano Ferro a Bologna allo Stadio dell'Ara",
    "artists": [
        "Tiziano Ferro",
        "Tiziano Acciaio",
        "Tiziano Titanio",
        "Tiziano Tungsteno",
        "Tiziano Ferramenta",
        "Tiziano Piombo",
        "Tiziano Palladio",
        "Tiziano Platino",
        "Tiziano Tiziano"
    ],
    "dates": [
        datetime(2023, 7, 11, 10, 30, 00) # 11/07/2023 alle 10:30:00
    ],
    "capacity": 35000,
    "currentcapacity": 35000,
    "tickets": [
        ["standard", 30, 31900],
        ["premium", 100, 3000],
        ["backstage", 300, 100]
    ],
    "location": {
        "locname" : "Stadio Dall'Ara",
        "address": "Via Andrea Costa, 174",
        "city": "Bologna",
        "district": "BO",
        "postalcode": 40134,
        "point": {
            "geometry": {
                "coordinates": [11.309997, 44.492317], 
                "type": "Point"
                }, 
            "properties": {}, 
            "type": "Feature"
        }
    }
}

TEMPLATE_TICKET = {
    "concert" : "TZN 2023",
    "anagrafica" : {
        "name": "Giorgio Pow3r",
        "surname": "Calandrelli di Ostia",
        "birth_date" : datetime(1992, 11, 22)
    },
    "purchase_date": f"{datetime.now()}",
    "ticket_type": "backstage"
}


def getLocFromAddress(locname = None, address = None, city = None):
    '''
    returns GeoJSON point coordinates of an address
    '''
    fulladdress = f"{locname}, {city}"
    location = geolocator.geocode(fulladdress)
    #ritorna None se non trova il posto e cerca l'indirizzo normale
    if location is None: 
        fulladdress = f"{address}, {city}"
        location = geolocator.geocode(fulladdress)
    # Create a GeoJSON Point from coords
    try:
        point = geojson.Point((location.longitude, location.latitude))
        # Convert the GeoJSON object to a dictionary
        point_dict = geojson.Feature(geometry=point, properties={}).__geo_interface__
    except:
        # If no address is found we return an empty dictionary
        return {}
    return point_dict

def insertConcert():
    '''
    Inserts concert data in the connected MongoDB database and returns the _id of the inserted file.
    [this whole function is a dictionary population]
    '''
    # Allocating lists for .append()
    concert_dict = {
        "artists" : [],
    }
    concert_tickets = []
    concert_location = {
        "coords" : {}
    }

    # Getting concert data from user
    concert_dict["name"], concert_dict["desc"]  = input("Name of the concert: "), input("Description of the concert: ")    
    '''
    inserisci artisti fino a che non viene inserito il carratere di escape "e"
    '''
    while True:
        concert_artist = input("Artist partecipating? ['e' to exit]: ")
        if (concert_artist == 'e'):
            break
        concert_dict["artists"].append(concert_artist)
    #inserisce la capacità nella capacità totale, corrente e in una variabile temporanea
    concert_dict["capacity"] = concert_dict["currentcapacity"] = capacity = int(input("How many seats?: "))

    # qui inserisci i tipi di ticket che vanno a scalare sulla capacità totale fino a che non si raggiunge il massimo
    while True:
        print("Ticket creation, insert name, price and capacity [exit when max capacity is reached]:")
        ticket_name = input("Ticket name: ")
        ticket_price = input("Ticket price: ")
        ticket_capacity = int(input("Ticket capacity: "))
        if capacity <= 0:
            print("Maximum capacity reached! Proceeding with concert creation.")
            break
        else: 
            concert_tickets.append((ticket_name, ticket_price, ticket_capacity))
            capacity -= ticket_capacity

    # Getting location data from user
    concert_location["locname"] = input("Name of the building/ where the concert is held: ")
    print("Insert the following info of the location:")
    concert_location["address"] = input("Address [street, number]: ")
    concert_location["city"] = input("City: ")
    concert_location["district"] = input("District: ")
    concert_location["postalcode"] = input("Postal code: ")
    concert_location["country"] = input("Country: ")
    concert_location["point"] = getLocFromAddress(concert_location["locname"], concert_location["address"], concert_location["city"])

    # Insert location data in main dictionary
    concert_dict["location"] = concert_location
    #inserimento dei dati del concerto su mongoDB
    return collection_concerts.insert_one(concert_dict)

def getConcerts():
    return 0

def orderTicket():
    return 0


if __name__ == "__main__":
    insertConcert()