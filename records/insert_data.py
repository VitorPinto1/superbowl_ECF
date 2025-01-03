import sys
import os

# Agrega el directorio raíz del proyecto a sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from api.config import *
from api.app import mongo

collection = mongo.db['matchs_year']

super_bowl_data = [
    {
        "year": 1967,
        "super_bowl": 1,
        "winner": "Green Bay Packers",
        "loser": "Kansas City Chiefs",
        "result": "35-10",
        "location": {
            "stadium": "Los Angeles Memorial Coliseum",
            "city": "Los Angeles",
            "state": "California"
        },
        "météo": "Ensoleillé, 20°C",
        "mvp": "Bart Starr (Quarterback)",
        "attendance": 61946
    }
]

for match in super_bowl_data:
    if not collection.find_one({"super_bowl": match["super_bowl"]}):
        collection.insert_one(match)
        print(f"Super Bowl {match['super_bowl']} Inséré correctement.")
    else:
        print(f"Super Bowl {match['super_bowl']} Déjà existant dans la base de données.")