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

TEMPLATE_JSON = {
    "name": "TZN 2023",
    "desc": "Concerto di Tiziano Ferro a Bologna allo Stadio dell'Ara",
    "artists": [
        "Tiziano Ferro",
        "Tiziano Acciaio",
        "Tiziano Titanio"
    ],
    "dates": [
        "2023-07-11T10:30:00Z"
    ],
    "capacity": 35000,
    "currentcapacity": 35000,
    "tickets": [
        ["standard", 30, 31900],
        ["premium", 100, 3000],
        ["standard", 30, 100]
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

def getLocFromAddress(locname = None, address = None, city = None):
    '''
    returns GeoJSON point coordinates of an address
    '''
    fulladdress = f"{locname}, {city}"
    location = geolocator.geocode(fulladdress)
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
    Inserts concert data in the connected MongoDB database.
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
    concert_dict["name"], concert_dict["desc"]  = input("Name of the concert: "), input("Description of the concert?: ")    
    while True:
        concert_artist = input("Artist partecipating? ['e' to exit]: ")
        if (concert_artist == 'e'):
            break
        concert_dict["artists"].append(concert_artist)
    concert_dict["capacity"] = concert_dict["currentcapacity"] = capacity = int(input("How many seats?: "))
    while True:
        print("Ticket creation, insert name, price and capacity [exit when max capacity is reached]:")
        ticket_name = input("Ticket name: ")
        ticket_price = input("Ticket price: ")
        ticket_capacity = int(input("Ticket capacity: "))
        if capacity >= 0:
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

    collection_concerts.insert_one(concert_dict)

def getConcerts():
    return 0

def orderTicket():
    return 0


if __name__ == "__main__":
    insertConcert()