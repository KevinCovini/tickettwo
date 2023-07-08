'''
ESPOSIZIONE FUNZIONALITA' PROGRAMMA (per video)
(Ci saranno dati già presenti sia di concerti che di ticket, grazie Max)
- Inserimento di un concerto
- Ricerca di un concerto: 
    per nome
    per artista partecipante
- Acquisto di un biglietto
- Rimborso di un biglietto:
    Rimborso valido
    Rimborso invalido

FUNZIONI DA FARE

-- getConcert() --

- PARTE OBBLIGATORIA:
    ricerca per:
      artista partecipante
      nome concerto
- PARTE FACOLTATIVA:
    ricertca per:
      intervallo di date
      per distanza
- COME FARE:
    fare la find sulla collection dei concerti e filtrare per quello che da in input l'utente
    visualizzare i seguenti dati: nome concerto, capienza attuale e i dati completi dei ticket

    
-- refundTicket() --

- COME FARE:
    - input anagrafica dell'utente (vedi "anagrafica" in ticket)
    - ricerca tutti i ticket registrati a quell'anagrafica
    - selezione ticket da rimborsare
    - verifica se il concerto c'è già stato o no
        se il concerto è da fare rimborso
        se il concerto è già fatto no rimborso
    - implementare pipeline per automatizzare l'increase della capacità del concerto se viene rimborsato un ticket

FUNZIONI DA MODIFICARE/MIGLIORARE

-- buyTicket() --

- Aggiungere possibilità di comprare più biglietti
- implementare pipeline per automatizzare il decrease della capacità del concerto se viene acquisato un ticket

    
'''


import pymongo as pm
from pymongo import MongoClient
import geojson
import geopy
from geopy.geocoders import Nominatim
from datetime import datetime

# Geocoder object
geolocator = Nominatim(user_agent="my_geocoder")

# Connessione al mongo cluster "KCluster"
uri = "mongodb+srv://kcovini:admin@kcluster.vg9adfo.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db_tickettwo = client["TicketTwo"]
collection_concerts = db_tickettwo["Concerts"]
collection_sales = db_tickettwo["Sales"]

# Controllo della connessione
try:
    client.admin.command('ping')
    print("Connection successful!")
except Exception as e:
    print(e)



def getLocFromAddress(locname = None, address = None, city = None):
    '''
     Ritorna le cordinate con GeoJSON
    '''
    fulladdress = f"{locname}, {city}"
    location = geolocator.geocode(fulladdress)
    # Ritorna None se non trova il posto e cerca l'indirizzo normale
    if location is None: 
        fulladdress = f"{address}, {city}"
        location = geolocator.geocode(fulladdress)
    # Crea un punto GeoJSON dalle cordinate
    try:
        point = geojson.Point((location.longitude, location.latitude))
        # Converte le cordinate GEOJSON in un dizionario
        point_dict = geojson.Feature(geometry=point, properties={}).__geo_interface__
    except:
        # Se non trova nessun indirizzo ritorna un dizionario vuoto
        return {}
    return point_dict

def insertConcert():
    '''
    Inserisci i dati di un corcerto nel database MongoDB e ritorno il suo _id 
    [Questa funzione serve per popolare il dizionario]
    '''
    # Creiamo l'istanza della lista 
    concert_dict = {
        "artists" : [],
    }
    concert_tickets = []
    concert_location = {
        "coords" : {}
    }

    # Prendiamo i dati di un concerto dall'utente

    concert_dict["name"], concert_dict["desc"]  = input("Name of the concert: "), input("Description of the concert: ")    
    '''
    Inserisci artisti fino a che non viene inserito il carratere di escape "e"
    '''
    while True:
        concert_artist = input("Artist partecipating? ['e' to exit]: ")
        if (concert_artist == 'e'):
            break
        concert_dict["artists"].append(concert_artist)
    # Inserisce la capacità nella capacità totale, corrente e in una variabile temporanea
    concert_dict["capacity"] = concert_dict["currentcapacity"] = capacity = int(input("How many seats?: "))

    # Qui inserisci i tipi di ticket che vanno a scalare sulla capacità totale fino a che non si raggiunge il massimo
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

    # Prendiamo i dati della location dall'utente

    concert_location["locname"] = input("Name of the building/ where the concert is held: ")
    print("Insert the following info of the location:")
    concert_location["address"] = input("Address [street, number]: ")
    concert_location["city"] = input("City: ")
    concert_location["district"] = input("District: ")
    concert_location["postalcode"] = input("Postal code: ")
    concert_location["country"] = input("Country: ")
    concert_location["point"] = getLocFromAddress(concert_location["locname"], concert_location["address"], concert_location["city"])

    # Insert della posizione del dizionario
    concert_dict["location"] = concert_location
    # Inserimento dei dati del concerto su mongoDB
    return collection_concerts.insert_one(concert_dict)

def getConcerts():
    return 0

def buyTicket():
    ticket_dict = {}

    # Insert dei dati del ticket
    concert = input("Concert Name: ")

    while True:
        if collection_concerts.find({"name":concert}).count() > 0:
            ticket_dict["concert"] = concert
            selected_concert = collection_concerts.find({"name":concert})
            break
        else:
            print("The inserted concert does not exist.")

    # Insert dei dati personali dell'utente
    ticket_dict["name"] = input("Name: ")
    ticket_dict["surname"] = input("Surname: ")
    ticket_dict["birth_date"] = input("Birth Date: ")
    
    type = input("Ticket Type (type ? for details): ")

    # Controllo del tipo di scelta
    result = None
    choices = [choice[:1][0] for choice in selected_concert[0]["tickets"]]
    while result == None:
        type.lower()
        if type not in choices:
            print("Error: you must choose a valid option.")
        elif type == "?":
            print(f"You can choose one of the following types: {choices}.")
        else:
            result = type
    
    ticket_dict["ticket_type"] = result

    # Decrementa la capacità attuale e della tipologia di ticket

    filter_query = {"name":concert}
    update_query = {"$inc": {"currentcapacity": -1}}
    update_query2 = {"$inc": {"tickets.0.2": -1}}

    collection_concerts.update_one(filter_query,update_query)
    collection_concerts.update_one(filter_query,update_query2)

    # Set della data di acquisto
    ticket_dict["purchase_date"] = datetime.now

    return collection_sales.insert_one(ticket_dict)
        
