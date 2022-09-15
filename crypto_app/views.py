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
    db.comprueba_db()
    output = db.status_cuenta()
    return output, status.HTTP_200_OK

@app.route("/api/v1/monedas_disponibles_usuario")
def monedas_disponibles_usuario():
    return json.dumps(MONEDAS), status.HTTP_200_OK

@app.route("/api/v1/movimientos")
def movimientos():
    db = DBManager(RUTA_DB)
    db.comprueba_db()
    output = db.devuelve_movimientos()
    return output, status.HTTP_200_OK

@app.route("/api/v1/rate/<string:moneda_origen>/<string:moneda_destino>/<float:cantidad>", methods=['GET'])
def rate(moneda_origen: str, moneda_destino: str, cantidad: float):
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
    db = DBManager(RUTA_DB)
    # fecha_aux = date.today()
    # fecha = ""
    # try:
    #     fecha = fecha_aux.strftime('%d-%m-%Y')

    # except ValueError:
    #     output = {"status":"failed", "error":"La fecha introducida no es valida"}
    #     return output, status.HTTP_400_BAD_REQUEST
    validacion_fecha = db.valida_fecha()
    fecha = ""
    if validacion_fecha["status"] == "failed":
        return validacion_fecha, status.HTTP_400_BAD_REQUEST
    else:
        fecha = validacion_fecha["fecha"]
        
    hora = time(datetime.now().hour, datetime.now().minute, datetime.now().second)
    hora = f"{hora.hour}:{hora.minute}:{hora.second}"
    try:
        datetime.strptime(hora, '%H:%M:%S')
    except ValueError:
        output = {"status":"failed", "error":"La hora introducida no es valida"}
        return output, status.HTTP_400_BAD_REQUEST
    except TypeError:
        output = {"status":"failed", "error":"La hora introducida no es valida"}
        return output, status.HTTP_400_BAD_REQUEST
        
    
    moneda_from = data["moneda_from"]
    if moneda_from not in MONEDAS:
        output = {"status":"failed", "error":f"La moneda de origen {moneda_from} no existe"}
        return output, status.HTTP_400_BAD_REQUEST
    
    moneda_to = data["moneda_to"]
    if moneda_to not in MONEDAS:
        output = {"status":"failed", "error":f"La moneda de destino {moneda_to} no existe"}
        return output, status.HTTP_400_BAD_REQUEST
    if moneda_from == moneda_to:
        output = {"status":"failed", "error":"Las monedas de origen y destino no pueden ser iguales"}
        return output, status.HTTP_400_BAD_REQUEST
    cantidad_to = data["cantidad_to"]
    cantidad_from = data["cantidad_from"]

    db = DBManager(RUTA_DB)
    db.comprueba_db()
    valores_wallet = db.status_cuenta()
    valores_wallet = valores_wallet["data"]

    if moneda_from != "EUR":
        try:
            if float(cantidad_from) > valores_wallet[moneda_from]:
                output = {"status":"failed", "error":f"No tienes suficiente saldo en {moneda_from}"}
                return output, status.HTTP_400_BAD_REQUEST
        except KeyError:
            output = {"status":"failed", "error":f"No tienes suficiente saldo en {moneda_from}"}
            return output, status.HTTP_400_BAD_REQUEST
    

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





