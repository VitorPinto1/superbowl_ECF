import sys
import os
import json

# Agrega el directorio raíz del proyecto a sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from api.config import *
from api.app import mongo

# Charger les données depuis le fichier JSON
json_file_path = "records/Super_Bowl_Data_1967_2024.json"

# Assurez-vous que le fichier existe
if not os.path.exists(json_file_path):
    print(f"Erreur : Le fichier {json_file_path} n'existe pas.")
    sys.exit(1)

with open(json_file_path, "r", encoding="utf-8") as file:
    super_bowl_data = json.load(file)

collection = mongo.db['matchs_year']

for match in super_bowl_data:
    if not collection.find_one({"super_bowl": match["super_bowl"]}):
        collection.insert_one(match)
        print(f"Super Bowl {match['super_bowl']} Inséré correctement.")
    else:
        print(f"Super Bowl {match['super_bowl']} Déjà existant dans la base de données.")