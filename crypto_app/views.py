from flask import jsonify
import requests
from . import app
from crypto_app.models import DBManager
from crypto_app.settings import APIKEY
#ENDPOINTS OBLIGATORIOS
@app.route("/api/v1/movimientos")
def movimientos():
    sql = "SELECT * from movimientos ORDER BY id, date, time, moneda_from, cantidad_from, moneda_to, cantidad_to"
    try:
        db = DBManager("db/movimientos.db")
        data = db.consultaSQL(sql)
        output = {
            "status":"success", 
            "datos":data
                }
        print(output)
        return output
    except Exception as error:
        output = {"status":"error", "error":error}
        print(error)
        return error

@app.route("/api/v1/tipo_cambio/<divisa_from>/<divisa_to>/<cantidad>")
def tipo_cambio():
    return "Valor unitario de la moneda destino en valor de origen"

@app.route("/api/v1/movimiento")
def alta_movimiento():
    return "Grabará un nuevo movimiento"

@app.route("/api/v1/staus")
def estado_inversion():
    return "Estado de la inversion"

#ENDPOINTS ADICIONALES

@app.route("/api/v1/monedas_disponibles")
def valor_monedas():
    headers = {'X-CoinAPI-Key' : APIKEY}
    url = "https://rest.coinapi.io/v1/assets"
    respuesta = requests.get(url, headers=headers)
    codigo = respuesta.status_code
    data = respuesta.json()
    index = 0
    assets = {}
    for elem in data:
        assets[index] = elem["asset_id"]
        index += 1
    output = {"status":"success", "data":assets}
    return output

@app.route("/api/v1/rate/<string:moneda_origen>/<string:moneda_destino>/<float:cantidad>")
def rate(moneda_origen: str, moneda_destino: str, cantidad: float):
    #TODO Comprobar si tenemos suficiente saldo para realizar la conversion
    headers = {'X-CoinAPI-Key' : APIKEY}
    url = f"https://rest.coinapi.io/v1/exchangerate/{moneda_origen}/{moneda_destino}"
    respuesta = requests.get(url, headers=headers)
    codigo = respuesta.status_code
    data = respuesta.json()
    price = {"tipo_cambio":data["rate"]*cantidad}
    output = {"status":"success", "data":price}
    return output

