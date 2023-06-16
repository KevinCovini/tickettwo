import pymongo as pm
from pymongo import MongoClient
import geopy

# Creato il client per MongoDB
uri = "mongodb+srv://kcovini:admin@kcluster.vg9adfo.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)

try:
    client.admin.command('ping')
    print("Connection successful!")
except Exception as e:
    print(e)

TEMPLATE_JSON = {
    "_id": {
        "$oid": "648c226689c685be1dcb4f32"
    },
    "name": "TZN 2023",
    "desc": "Concerto di Tiziano Ferro a Bologna allo Stadio dell'Ara",
    "tickets": {
        "standard": [
            30,
            32000
        ],
        "premium": [
            100,
            2900
        ],
        "backstage": [
            250,
            100
        ]
    },
    "artists": [
        "Tiziano Ferro"
    ],
    "location": {
        "city": "Bologna",
        "district": "BO",
        "postalcode": 40134,
        "coords": [
            44.49220437265215,
            11.309950162342037
        ]
    },
    "dates": [
        "2023-07-11T10:30:00Z"
    ],
    "capacity": 35000,
    "currentcapacity": 35000
}

def getConcerts():
    return 0

def orderTicket():
    return 0


if __name__ == "__main__":
    getConcerts()
    orderTicket()