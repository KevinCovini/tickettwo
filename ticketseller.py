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


def getLocFromAddress(locname=None, address=None, city=None):
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
        point_dict = geojson.Feature(
            geometry=point, properties={}).__geo_interface__
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
        "artists": [],
    }
    concert_tickets = []
    concert_location = {
        "coords": {}
    }

    # Prendiamo i dati di un concerto dall'utente

    concert_dict["name"], concert_dict["desc"] = input(
        "Name of the concert: "), input("Description of the concert: ")
    '''
    Inserisci artisti fino a che non viene inserito il carratere di escape "e"
    '''
    while True:
        concert_artist = input("Artist partecipating? ['e' to exit]: ")
        if (concert_artist == 'e'):
            break
        concert_dict["artists"].append(concert_artist)
    # Inserisce la capacità nella capacità totale, corrente e in una variabile temporanea
    capacity = int(input("How many seats?: "))
    concert_dict["capacity"] = int(capacity)
    concert_dict["currentcapacity"] = int(capacity)
    

    # Qui inserisci i tipi di ticket che vanno a scalare sulla capacità totale fino a che non si raggiunge il massimo
    while True:
        print("----------------------------------------------------------------")
        print(f"Current capacity: {capacity}")
        print("Ticket creation, insert name, price and capacity [exit when max capacity is reached]:")
        print("----------------------------------------------------------------")
        ticket_name = input("Ticket name: ")
        ticket_price = input("Ticket price: ")
        ticket_capacity = int(input("Ticket capacity: "))
        capacity -= ticket_capacity
        if capacity < 0:
            capacity += ticket_capacity
            print("--------------------------------------------------------")
            print(f"Quantità non valida | posti rimanenti {capacity}")
            print("--------------------------------------------------------")
            continue
        else:
            if capacity == 0:
                print("--------------------------------------------------------")
                print("Maximum capacity reached! Proceeding with concert creation.")
                print("--------------------------------------------------------")
                concert_tickets.append([ticket_name, ticket_price, ticket_capacity])
                break
            else:
                concert_tickets.append([ticket_name, ticket_price, ticket_capacity])

    # Inseriamo la data nel formato Datetime
    concert_date_str = input("Concert Date (YYYY-MM-DD): ")
    concert_date = datetime.strptime(concert_date_str, "%Y-%m-%d")
    concert_dict["dates"] = concert_date

    # Prendiamo i dati della location dall'utente
    concert_dict["tickets"] = concert_tickets
    concert_location["locname"] = input(
        "Name of the building/ where the concert is held: ")
    print("Insert the following info of the location:")
    concert_location["address"] = input("Address [street, number]: ")
    concert_location["city"] = input("City: ")
    concert_location["district"] = input("District: ")
    concert_location["postalcode"] = input("Postal code: ")
    concert_location["country"] = input("Country: ")
    concert_location["point"] = getLocFromAddress(
        concert_location["locname"], concert_location["address"], concert_location["city"])

    # Insert della posizione del dizionario
    concert_dict["location"] = concert_location
    # Inserimento dei dati del concerto su mongoDB
    return collection_concerts.insert_one(concert_dict)

def all_concerts():
    results = collection_concerts.find()
    results2 = collection_sales.find()
    
    if results.count() == 0:
        print("Non è presente nessun concerto")
    else:
        for doc in results:
            print(str(doc["name"]))
            print(str(doc["currentcapacity"]) + "/" + str(doc["capacity"]))
            tickets = doc.get("tickets")
            
            if tickets:
                for ticket in tickets:
                    print("Ticket:", ticket[0])
                    print("Prezzo:", ticket[1])
                    print("Ticket rimanenti:", ticket[2])
            else:
                print("Nessun dato sui biglietti disponibile per questo concerto.")
            print("--------------------------------------------------------------")
    
    if results2.count() == 0:
        print("Non è presente nessun ticket")
    else:
        for doc in results2:
            print(str(doc["concert"]))
            print(str(doc["name"]))
            print(str(doc["surname"]))
            print(str(doc["birth_date"]))
            print(str(doc["purchase_date"]))
            print(str(doc["ticket_type"]))
            print("--------------------------------------------------------------")


def searchConcert(concerto=None, artisti=None):
    if concerto is not None:
        results = collection_concerts.find({"name": concerto})

    elif artisti is not None:
        query = {"artists": {"$in": artisti}}
        results = collection_concerts.find(query)

    else:
        results = collection_concerts.find()

    for doc in results:
        print("----------------------------------------------------------------")
        print(str(doc["name"]))
        print(str(doc["currentcapacity"]) + "/" + str(doc["capacity"]))
        tickets = doc.get("tickets")
        
        if tickets:
            for ticket in tickets:
                print("Ticket:", ticket[0])
                print("Prezzo:", ticket[1])
                print("Ticket rimanenti:", ticket[2])
        else:
            print("Nessun dato sui biglietti disponibile per questo concerto.")
        print("----------------------------------------------------------------")
    return 0


def buyTicket():
    ticket_dict = {}
    
    # Insert dei dati del ticket

    while True:
        concert = input("Concert Name: ")
        if collection_concerts.find({"name": concert}).count() > 0:
            ticket_dict["concert"] = concert
            selected_concert = list(collection_concerts.find({"name": concert}))
            #selected_concert = collection_concerts.find({"name": concert})
            break
        else:
            print("The inserted concert does not exist.")

    # Insert dei dati personali dell'utente
    ticket_dict["name"] = input("Name: ")
    ticket_dict["surname"] = input("Surname: ")

    birth_date_str = input("Birth Date (YYYY-MM-DD): ")
    birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d")
    ticket_dict["birth_date"] = birth_date

    # Controllo del tipo di scelta
    result = None
    choices = [choice[:1][0] for choice in selected_concert[0]["tickets"]]
    
    ticket_type = ""
    while result == None:
        ticket_type = input("Ticket Type (type ? for details): ")
        if ticket_type == "?":
            print(f"You can choose one of the following types: {choices}.")
        elif ticket_type not in choices:
            print("Error: you must choose a valid option.")
        else:
            result = ticket_type

    ticket_dict["ticket_type"] = result

    # Decremento della capacità
    filter_query = {"name": concert}
    update_query = {"$inc": {"currentcapacity": -1}}
    update_query2 = {"$inc": {f"tickets.{choices.index(result)}.2": -1}}

    collection_concerts.update_one(filter_query, update_query)
    collection_concerts.update_one(filter_query, update_query2)

    #test print capacity
    risultatodellaquery = collection_concerts.find(filter_query)
    print(risultatodellaquery[0]["currentcapacity"])
    print(risultatodellaquery[0]["tickets"][0][2])

    # Set della data di acquisto
    current_date = datetime.now()
    ticket_dict["purchase_date"] = current_date
    collection_sales.insert_one(ticket_dict)
    


def refundTicket():
    ticket_dict = {}
    # Richiedo i dati dell'utente
    print("Per eseguire un refund inserisci i tuoi dati")
    name= input("Name: ")

    result = collection_sales.find({"name": name})
    tickets_found = []

    if result:
        i = 0
        for ticket in result:
            print(str(ticket["concert"]) + " - Premi [" + str(i) + "] per fare il refund di questo ticket")
            i += 1
            tickets_found.append(ticket)

        while True: #scelta del ticket sul quale effettuare il refound
            try:
                print("----------------------------------------------------------------")
                print("Premi q per uscire.")
                print("----------------------------------------------------------------")
                choice = input("Scelta: \n")
                if choice == "q":
                    break
                elif int(choice) >= len(tickets_found):
                    raise ValueError
                else:
                    # Eliminiamo il ticket corrispondente alla scelta dell'utente
                    selected_ticket_index = int(choice)
                    selected_ticket = tickets_found[selected_ticket_index]
                    selected_concert = selected_ticket["concert"]
                    selected_type = selected_ticket["ticket_type"]
                    concert_search = collection_concerts.find_one({"name": selected_concert})
                    choices = [choice[:1][0] for choice in concert_search["tickets"]] #aggiunto in modo da avere una lista con solo i tipi
                    concert_date = concert_search["dates"]
                    current_date = datetime.now()
                    if concert_search is not None:
                        if current_date >= concert_date: # Controllo se il concerto si è già svolto
                            print("----------------------------------------------------------------")
                            print("Il rimborso non può essere effuttuato perchè ormai il concerto si è già svolto")
                            print("----------------------------------------------------------------")
                        else:
                            collection_sales.delete_one(selected_ticket)
                            print("----------------------------------------------------------------")
                            print("Ticket eliminato con successo.")
                            print("----------------------------------------------------------------")
                            #andiamo a incrementare il numero di ticket
                            filter_query = {"name": selected_concert}
                            update_query = {"$inc": {"currentcapacity": 1}}
                            update_query2 = {"$inc": {f"tickets.{choices.index(selected_type)}.2": 1}}

                            collection_concerts.update_one(filter_query, update_query)
                            collection_concerts.update_one(filter_query, update_query2)
                            break
            except ValueError:
                print("----------------------------------------------------------------")
                print("Valore inserito non valido")
                print("----------------------------------------------------------------")
    else:
        print("----------------------------------------------------------------")
        print("Nessun risultato trovato.")
        print("----------------------------------------------------------------")

    return 0

def del_sales(): # Cancella tutti i ticket
    collection_sales.delete_many({})
    print("Ticket eliminati con successo")
    print("----------------------------------------------------------------")

def del_concerts(): # Cancella tutti i concerti
    collection_concerts.delete_many({})
    print("Concerti eliminati con successo")
    print("----------------------------------------------------------------")

BENVENUTO = '''Benvenuto su TicketTwo!
0. Esci dal menù
1. Annuncia un concerto
2. Visualizza tutti i concerti
3. Cerca un concerto per nome
4. Cerca un concerto per artista
5. Compra un biglietto
6. Rimborsa un biglietto
7. Cancella tutti i concerti
8. Cancella tutti i ticket
'''
while True:
    print(BENVENUTO)
    selezione = int(input("Seleziona un'opzione: "))
    if selezione == 1:
        insertConcert()
    elif selezione == 2:
        all_concerts()
    elif selezione == 3:
        concerto = input("Inserisci il nome del concerto [Enter per andare avanti]: ")
        searchConcert(concerto=concerto)

    elif selezione == 4:
        lista_artisti = []
        while True:
            artista = input("Artisti partecipanti [inserire 'e' per andare avanti]: ")
            if artista == 'e':
                break
            lista_artisti.append(artista)
        searchConcert(artisti=lista_artisti)

    elif selezione == 5:
        buyTicket()

    elif selezione == 6:
        refundTicket()

    elif selezione == 7:
        del_concerts()

    elif selezione == 8:
        del_sales()

    elif selezione == 0:
        break