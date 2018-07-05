import pymongo
from flask import Flask, jsonify, request

def get_db_connection(uri):
  client = pymongo.MongoClient(uri)
  return  client.cryptongo

app = Flask(__name__)
db_connection = get_db_connection('mongodb://dbmongo:27017/')

def get_documents():
  params ={}
  # name = int(request.args.get('name',''))
  name = request.args.get('name','')
  limit = int(request.args.get('limit', 0))
  if name:
    params.udpate({'name':name})
  cursor=db_connection.tickers.find(
    params,{'_id':0,'ticker_hash':0}).limit(limit)
  return list(cursor)

def get_top20():
  params = {}
  # name = int(request.args.get('name', ''))
  name = request.args.get('name','')
  limit = int(request.args.get('limit', 0))
  if name:
    params.udpate({'name':name})
    params.update({'rank': {'$lte': 20}})
  cursor = db_connection.tickers.find(
    params, {'_id': 0, 'ticker_hash': 0}).limit(limit)
  return list(cursor)

def remove_currency():
  params = {}
  name = request.args.get('name', '')
  if name:
    params.update({'name': name})
  else:
    returnFalse
  return db_connection.tickers.delete_many(params).deleted_count

@app.route('/') #Defino la ruta raíz para recibir peticiones
def index():#Cuando alguien pida esta ruta, se ejecutará esta función
  return jsonify( #Retornará una respuesta en formato json
    {
      'name': 'Cryptongo API'
    }
  )

@app.route("/tickers", methods=['GET', 'DELETE']) #Defino ruta para obtener o eliminar tickers, recibiendo petición por GET o DELETE
def tickers():#Con la ruta, se ejecuta esta función
  if request.method == "GET": #Si el método consultado por la ruta, es GET
    return jsonify(get_documents()) #Devuelve un json con el resultado de tickers, según parámetros por get (Puede ser sin parámetros)
  elif request.method == "DELETE": #En cambio, si el método consultado es por DELETE
    result = remove_currency() #Se borran los tickers que coincidan con los parámetros recibidos por get (Los parámetros son obligatorios)
    if result > 0:
      return jsonify({ #Retornar un json con la respuesta
        'text': 'Documentos eliminados'
      }), 204#Flask permite agregar otro parámetro al return, indicando el código de respuesta, en este caso, un "No hay contenido" (común en los borrados de datos)
    else:
      return jsonify({ #Retornar un json con la respuesta
        'error': 'No se encontraron documentos'
      }), 404#Flask permite agregar otro parámetro al return, indicando el código de respuesta, en este caso, un "No encontrado"

@app.route('/top20', methods=['GET']) #Defino ruta GET para top20
def top20():#Se ejecutará esta función cuando alguien entre a esa ruta
  return jsonify(get_top20()) #Devuelvo un json con la lista de top2