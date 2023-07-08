from datetime import datetime


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


TEMPLATE_CONCERTO2 = {
    "name": "Giocata Fredda",
    "desc": "Concerto della Giocata Fredda",
    "artists": [
        "Giocata Fredda",
        "Giocata molto Fredda",
        "Giocata Congelata",
        "Giocata Siderale",
        "Giocata quasi fredda"
    ],
    "dates": [
        datetime(2023, 11, 30, 10, 30, 00) # 11/07/2023 alle 10:30:00
    ],
    "capacity": 40000,
    "currentcapacity": 40000,
    "tickets": [
        ["standard", 30, 36000],
        ["premium", 100, 3900],
        ["backstage", 300, 100]
    ],
    "location": {
        "locname" : "Stadio Meazza",
        "address": "Piazzale Angelo Moratti",
        "city": "Milano",
        "district": "MI",
        "postalcode": 20151,
        "point": {
            "geometry": {
                "coordinates": [45.477987, 9.123846], 
                "type": "Point"
                }, 
            "properties": {}, 
            "type": "Feature"
        }
    }
}

TEMPLATE_CONCERTO3 = {
    "name": "DragonForce",
    "desc": "Incredibile ritorno del gruppo di Ostia",
    "artists": [
        "Marc Hudson – voce",
        "Herman Li – chitarra",
        "Sam Totman – chitarra",
        "Alicia Vigil – basso",
        "Gee Anzalone – batteria"
    ],
    "dates": [
        datetime(2022, 11, 14, 21, 00, 00) # 11/07/2023 alle 10:30:00
    ],
    "capacity": 38000,
    "currentcapacity": 0,
    "tickets": [
        ["standard", 30, 35000],
        ["premium", 100, 2900],
        ["backstage", 300, 100]
    ],
    "location": {
        "locname" : "Stadio Meazza",
        "address": "Piazzale Angelo Moratti",
        "city": "Milano",
        "district": "MI",
        "postalcode": 20151,
        "point": {
            "geometry": {
                "coordinates": [45.477987, 9.123846], 
                "type": "Point"
                }, 
            "properties": {}, 
            "type": "Feature"
        }
    }
}


TEMPLATE_CONCERTO4 = {
    "name": "Ligabue",
    "desc": "La festa rock",
    "artists": [
        "Ligabue"
    ],
    "dates": [
        datetime(2023, 8, 5, 20, 30, 00) # 11/07/2023 alle 10:30:00
    ],
    "capacity": 38000,
    "currentcapacity": 0,
    "tickets": [
        ["standard", 30, 35000],
        ["premium", 100, 2900],
        ["backstage", 300, 100]
    ],
    "location": {
        "locname" : "Stadio Meazza",
        "address": "Piazzale Angelo Moratti",
        "city": "Milano",
        "district": "MI",
        "postalcode": 20151,
        "point": {
            "geometry": {
                "coordinates": [45.477987, 9.123846], 
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
