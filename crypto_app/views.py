from flask import render_template, request, json
from flask_api import status
import requests
from . import app
from crypto_app.models import DBManager, valida_moneda
from crypto_app.settings import APIKEY, RUTA_DB, MONEDAS
import sqlite3
from datetime import datetime, date, time

@app.route("/", methods=["GET","POST"])
def main():
    return render_template("index.html")

@app.route("/api/v1/status")
def estado_inversion():
    db = DBManager(RUTA_DB)
    db.comprueba_db_creada()
    output = db.status_cuenta()
    return output, status.HTTP_200_OK

@app.route("/api/v1/monedas_disponibles_usuario")
def monedas_disponibles_usuario():
    return json.dumps(MONEDAS), status.HTTP_200_OK

@app.route("/api/v1/movimientos")
def movimientos():
    db = DBManager(RUTA_DB)
    db.comprueba_db_creada()
    output = db.devuelve_movimientos()
    return output, status.HTTP_200_OK

@app.route("/api/v1/rate/<string:moneda_origen>/<string:moneda_destino>/<float:cantidad>", methods=['GET'])
def rate(moneda_origen: str, moneda_destino: str, cantidad: float):
    #TODO: Cambiar esto por el metodo de DBManager
    if valida_moneda(moneda_origen) == False:
        output = {
            "status":"fail",
            "error":"Las monedas seleccionadas no son válidas"
        }
        return output, status.HTTP_400_BAD_REQUEST
    if valida_moneda(moneda_destino) == False:
        output = {
            "status":"fail",
            "error":"Las monedas seleccionadas no son válidas"
        }
        return output, status.HTTP_400_BAD_REQUEST
    
    headers = {'X-CoinAPI-Key' : APIKEY}
    url = f"https://rest.coinapi.io/v1/exchangerate/{moneda_origen}/{moneda_destino}"
    respuesta = requests.get(url, headers=headers)
    codigo = respuesta.status_code
    data = respuesta.json()
    try:
        price = {"tipo_cambio":data["rate"]*cantidad}
        output = {"status":"success", "data":price}
    except KeyError:
        output = {"status":"fail", "error":"ERROR: No se ha podido realizar la conversión, comprueba tu APIKEY y vuelve a intentarlo, si acabas de crear tu APIKEY puede dar algunos errores, intenta de nuevo en unos minutos"}
        return output, status.HTTP_400_BAD_REQUEST
    return output, status.HTTP_200_OK

@app.route("/api/v1/movimiento", methods=['POST'])
def alta_movimiento():
    data = ""
    if request.method == 'POST':
        data = request.get_json()
        request.close()
    fecha = ""
    hora = ""
    moneda_from = data["moneda_from"]
    moneda_to = data["moneda_to"]
    cantidad_to = data["cantidad_to"]
    cantidad_from = data["cantidad_from"]
    
    db = DBManager(RUTA_DB)
    validacion_fecha = db.crear_fecha()
    if validacion_fecha["status"] == "failed":
        return validacion_fecha, status.HTTP_400_BAD_REQUEST
    else:
        fecha = validacion_fecha["data"]

    validacion_hora = db.crear_hora()
    if validacion_hora["status"] == "failed":
        return validacion_hora, status.HTTP_400_BAD_REQUEST
    else:
        hora = validacion_hora["data"]
  
    validacion_monedas = db.valida_monedas(moneda_from, moneda_to)
    if validacion_monedas["status"] == "failed":
        return validacion_monedas, status.HTTP_400_BAD_REQUEST

    validacion_cantidades = db.valida_cantidad(cantidad_from, cantidad_to)
    if validacion_cantidades["status"] == "failed":
        return validacion_cantidades, status.HTTP_400_BAD_REQUEST
    
    if moneda_from != "EUR":
        validacion_saldo_suficiente = db.saldo_suficiente(cantidad_from, moneda_from)
        if validacion_saldo_suficiente["status"] == "failed":
            return validacion_saldo_suficiente, status.HTTP_400_BAD_REQUEST
    
    db.comprueba_db_creada()

    sql = "INSERT INTO movimientos (date, time, moneda_from, cantidad_from, moneda_to, cantidad_to) VALUES (?,?,?,?,?,?)" 
    params = (
        fecha,
        hora,
        moneda_from,
        cantidad_from,
        moneda_to,
        cantidad_to
    )
    db = DBManager(RUTA_DB)
    estado = db.consultaConParametros(sql, params)
    output = {"status":"success","data":{"date":fecha, "time":hora, "moneda_from":moneda_from, "cantidad_from":cantidad_from, "moneda_to":moneda_to, "cantidad_to":cantidad_to}}
    return output, status.HTTP_200_OK

@app.route("/api/v1/monedas_disponibles")
def valor_monedas():
    headers = {'X-CoinAPI-Key' : APIKEY}
    url = "https://rest.coinapi.io/v1/assets"
    respuesta = requests.get(url, headers=headers)
    codigo = respuesta.status_code
    data = respuesta.json()
    index = 0
    assets = {}
    try:
        for elem in data:
            assets[index] = elem["asset_id"]
            index += 1
        output = {"status":"success", "data":assets}
    except KeyError:
        output = {"status":"fail", "error":"ERROR: No se ha podido realizar la consulta, comprueba tu APIKEY y vuelve a intentarlo, si acabas de crear tu APIKEY puede dar algunos errores, intenta de nuevo en unos minutos"}
        return output, status.HTTP_400_BAD_REQUEST
    except TypeError:
        output = {"status":"fail", "error":"ERROR: No se ha podido realizar la consulta, comprueba tu APIKEY y vuelve a intentarlo, si acabas de crear tu APIKEY puede dar algunos errores, intenta de nuevo en unos minutos"}
        return output, status.HTTP_400_BAD_REQUEST
    return output, status.HTTP_200_OK





