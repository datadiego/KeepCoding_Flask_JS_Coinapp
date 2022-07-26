from flask import jsonify
import requests
from . import app
from crypto_app.models import DBManager
from crypto_app.settings import APIKEY, MONEDAS, RUTA_DB
import sqlite3
from datetime import datetime
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
    
    except sqlite3.OperationalError:
        output = {"status":"fail", "error":"Hay un problema con la base de datos"}
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

@app.route("/api/v1/movimiento")
def alta_movimiento():
    #TODO Estoy hardcodeando los datos ¿Como introducimos los datos aqui?
    #TODO Validar cantidades para que no nos la cuelen
    
    #Validar fecha
    date = "2022-12-10"
    try:
        
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        output = {"status":"failed", "error":"La fecha introducida no es valida"}
        return output

    #Validar tiempo
    time = "23:59"
    try:
        datetime.strptime(time, '%H:%M')
    except ValueError:
        output = {"status":"failed", "error":"La hora introducida no es valida"}
        return output

    #Validar moneda origen
    moneda_from = "BTC"
    if moneda_from not in MONEDAS:
        output = {"status":"failed", "error":f"La moneda de origen {moneda_from} no existe"}
        return output

    cantidad_from = 5.0
    moneda_to = "EUR"
    if moneda_to not in MONEDAS:
        output = {"status":"failed", "error":f"La moneda de destino {moneda_to} no existe"}
        return output
    cantidad_to = 1000.0
    sql = f"""INSERT INTO movimientos (date, time, moneda_from, cantidad_from, moneda_to, cantidad_to) 
        VALUES ('{date}','{time}', '{moneda_from}', {cantidad_from}, '{moneda_to}', {cantidad_to})"""
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



