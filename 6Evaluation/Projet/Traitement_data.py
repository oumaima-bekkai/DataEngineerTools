#------------------------------Importation des librairies nécessaires----------------------------------
import pandas as pd
import pymongo
import json


client = pymongo.MongoClient("mongo:27017")
database = client['TripAdvisor']
collection = database['TA_Restaurant']

# ------------------- Importation des jeux de données en dataframe et nettoyage ------------------------
df = pd.read_csv('TA_restaurants_curated.csv')
df = df.drop(['Unnamed: 0'], axis=1)
df = df.dropna()
df = df.drop_duplicates(subset='ID_TA', keep="first")

# -------------------------- Importation des jeux de données pour MongoDB ------------------------------

# Spécification de l'ID des documents
df= df.rename(columns={"ID_TA":"_id"})

payload = json.loads(df.to_json(orient='records'))
collection.delete_many({}) #pour nettoyer la collection
collection.insert_many(payload)

# nombre de villes différentes
print(len(collection.distinct('City')))
