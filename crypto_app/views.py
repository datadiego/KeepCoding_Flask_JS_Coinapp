from flask import render_template
import requests
from . import app
from crypto_app.models import DBManager
from crypto_app.settings import APIKEY, MONEDAS, RUTA_DB
import sqlite3
from datetime import datetime
#ENDPOINTS OBLIGATORIOS
@app.route("/api/v1/movimientos")
def movimientos():
    db = DBManager(RUTA_DB)
    output = db.devuelve_movimientos()
    return output

@app.route("/api/v1/rate/<string:moneda_origen>/<string:moneda_destino>/<float:cantidad>", methods=['GET'])
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
    #TODO: Crear la peticion sql en el modelo
    
    #Validar fecha
    date = "2022-12-10"
    time = "23:59"
    moneda_from = "XTZ"
    cantidad_from = 5.0
    moneda_to = "EUR"
    cantidad_to = 100.0
    precio_moneda_to = 50 #TODO Esta variable vendrá de el endpoint rate

    db = DBManager(RUTA_DB)
    valores_wallet = db.status_cuenta()

    try:
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        output = {"status":"failed", "error":"La fecha introducida no es valida"}
        return output

    #Validar tiempo
    
    try:
        datetime.strptime(time, '%H:%M')
    except ValueError:
        output = {"status":"failed", "error":"La hora introducida no es valida"}
        return output

    #Validar moneda origen
    
    if moneda_from not in MONEDAS:
        output = {"status":"failed", "error":f"La moneda de origen {moneda_from} no existe"}
        return output

    
    if moneda_to not in MONEDAS:
        output = {"status":"failed", "error":f"La moneda de destino {moneda_to} no existe"}
        return output
    
    if moneda_from != "EUR":
        if valores_wallet[moneda_from] < precio_moneda_to:
            output = {"status":"failed", "error":f"No dispones de suficientes {moneda_from}"}
            return output
    sql = f"""INSERT INTO movimientos (date, time, moneda_from, cantidad_from, moneda_to, cantidad_to) 
        VALUES ('{date}','{time}', '{moneda_from}', {cantidad_from}, '{moneda_to}', {cantidad_to})"""
    db = DBManager(RUTA_DB)
    estado = db.crear_movimiento(sql)
    output = {"status":"success","data":{"date":date, "time":time, "moneda_from":moneda_from, "cantidad_from":cantidad_from, "moneda_to":moneda_to, "cantidad_to":cantidad_to}}
    return output

@app.route("/api/v1/status")
def estado_inversion():
    db = DBManager(RUTA_DB)
    output = db.status_cuenta()
    return output


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

@app.route("/")
def main():
    return render_template("index.html")



