import requests
import pymongo
import time

API_URL = 'https://api.coinmarketcap.com/v1/ticker/'
# API_URL = 'https://api.coinmarketcap.com/v2/ticker/'

def get_db_connection(uri):
  client = pymongo.MongoClient(uri)
  return client.cryptongo

def get_crypto_from_api():
  r = requests.get(API_URL)
  if r.status_code == 200:
    return r.json()

  raise Exception('API Error')

def check_if_exists(db_connection, ticker_data):
  ticker_hash = get_ticker_hash(ticker_data)
  if db_connection.tickers.find_one({'ticker_hash': ticker_hash}):
    return True

  return False

# Save ticket
def save_ticker(db_connection, ticker_data = None):
  if not ticker_data:
    return False

  if check_if_exists(db_connection, ticker_data):
    return False

  # Convert to integers
  ticker_hash = get_ticker_hash(ticker_data)
  ticker_data['ticker_hash'] = ticker_hash
  ticker_data['rank'] = int(ticker_data['rank'])
  ticker_data['last_updated'] = int(ticker_data['last_updated'])

  # Insert a document into the MongoDB collection
  db_connection.tickers.insert_one(ticker_data)
  return True

def get_hash(value):
  from hashlib import sha512 #Función para encriptar
  return sha512( #Encripto
    value.encode('utf-8') #El string codificado en utf-8, requisito de la librería hash
  ).hexdigest() #Convertir encriptado en un string para poder ser almacenado posteriormente en bd

def first_element(element):
  return element[0]

#Función para retornar un solo gran string con todos los datos de los items
def get_ticker_hash(ticker_data):
  from collections import OrderedDict #Permite ordenar una coleción bajo un criterio
  print (ticker_data)
  ticker_data = OrderedDict(
    sorted(
      ticker_data.items(), #Se le pasa la lista de items a ordenar
      key = first_element #Sorted manda a llamar a la función first_element, pasándole una tupla (key, value). 
                            #Y lo que retorne, será el valor usado para ordenar
    )
  )

  ticker_value = ''#Donde se guardará el hash final a retornar
  for _, value in ticker_data.items(): #Recorrer la lista de items
    ticker_value += str(value) #Concatenar el valor del item como string

  return get_hash(ticker_value) #Encripto string creado


if __name__ == '__main__':
  # connection = get_db_connection('mongodb://dbmongo:27017/') #Conectar a la bd de manera simple, sin usuario y contraseña
  # tickers = get_crypto_from_api() #Se solicita lista de tickers desde el api externo

  # for ticker in tickers: #Recorro lista de tickers recibidos
  #   save_ticker(connection, ticker) #Guardo cada ticker en bd, solo si no existe actualmente

  # print('Tickers almacenados')
  while True:
    print("Guardando información en Cryptongo")
    connection = get_db_connection('mongodb://dbmongo:27017/')
    tickers = get_crypto_from_api()

    for ticker in tickers:
        save_ticker(connection, ticker)
    time.sleep(240)