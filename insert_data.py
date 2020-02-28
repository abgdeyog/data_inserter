from pymongo import MongoClient
import json
import requests

try:
    conn = MongoClient()
    print("Connected successfully!!!")
except:
    print("Could not connect to MongoDB")
    conn = ""
    exit()


def insert_history(db):
    currencies_names = ["ada", "btc", "eth", "ltc", "xrp"]
    histories = [
        json.loads(
            requests.get("https://min-api.cryptocompare.com/data/v2/histoday?fsym="
                + currency_name + "&tsym=USD&limit=2000&" +
                "api_key=b4ed7a33d4bfd3bd4ec545c300cf13942a456c57bf0964105bdfe9323ba092ba").content)["Data"]["Data"]
        for currency_name in currencies_names]
    db.currency.create_index("timestamp")
    data_to_insert = [
        {"timestamp": histories[0][day]["time"],
         "data": [
             {currencies_names[i]: histories[i][day] for i in range(len(currencies_names))}
         ]
         } for day in range(len(histories[0]))
    ]
    print(len(data_to_insert))
    db.currency.insert_many(data_to_insert)


db = conn.history
insert_history(db)
# for index in db.currency.list_indexes():
#     print(index)
cursor = db.history.find()
for record in cursor:
    print(record)


