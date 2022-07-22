from flask import jsonify
from . import app
from crypto_app.models import DBManager

@app.route("/api/v1/movimientos")
def movimientos():
    #TODO: devolver json 
    sql = "SELECT * from movimientos ORDER BY id, date, time, moneda_from, cantidad_from, moneda_to, cantidad_to"
    try:
        db = DBManager("db/movimientos.db")
        data = db.consultaSQL(sql)
        output = {"status":"success", "data":data}
        return output
    except Exception as error:
        output = {"status":"error", "error":error}
        return output

@app.route("/api/v1/tipo_cambio/<divisa_from>/<divisa_to>/<cantidad>")
def tipo_cambio():
    return "Valor unitario de la moneda destino en valor de origen"

@app.route("/api/v1/movimiento")
def alta_movimiento():
    return "Grabará un nuevo movimiento"

@app.route("/api/v1/staus")
def estado_inversion():
    return "Estado de la inversion"



