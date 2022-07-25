from flask import jsonify
import requests
from . import app
from crypto_app.models import DBManager
from crypto_app.settings import APIKEY, RUTA_DB
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

@app.route("/api/v1/movimiento")
def alta_movimiento():
    date = "2022-01-01"
    time = "22:12"
    moneda_from = "BTC"
    cantidad_from = 5.0
    moneda_to = "XTZ"
    cantidad_to = 1000.0
    sql = "INSERT INTO movimientos (date, time, moneda_from, cantidad_from, moneda_to, cantidad_to) VALUES ('2022-07-02','21:06', 'XTZ', 0.25, 'LTC', 5)"
    db = DBManager(RUTA_DB)
    estado = db.crear_movimiento(sql)
    output = {"data":estado}
    return output

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



