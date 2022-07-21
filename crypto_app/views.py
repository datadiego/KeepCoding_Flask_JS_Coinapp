from . import app
from flask import render_template

@app.route("/api/v1/movimientos")
def movimientos():
    return "Hola flask"

@app.route("/api/v1/tipo_cambio/<divisa_from>/<divisa_to>/<cantidad>")
def tipo_cambio():
    return "Valor unitario de la moneda destino en valor de origen"

@app.route("/api/v1/movimiento")
def alta_movimiento():
    return "Grabará un nuevo movimiento"

@app.route("/api/v1/staus")
def estado_inversion():
    return "Estado de la inversion"



