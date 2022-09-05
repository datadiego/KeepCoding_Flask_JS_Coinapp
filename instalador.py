import requests

def peticion(text):
    resultado = ""
    while resultado == "":
        resultado = input(text)
    return resultado

def configuracion_APIKEY():
    print("Vamos a configurar tu APIKEY")
    APIKEY_AUX = peticion("Ingresa tu APIKEY: ")
    test_APIKEY = ""
    while test_APIKEY != "y" and test_APIKEY !="n":
        test_APIKEY = peticion("¿Quieres testear tu APIKEY? (y/n) ")
        test_APIKEY = test_APIKEY.lower()
        if test_APIKEY == "y":
            print("Llamando a coinapi.io... Esto puede tardar unos segundos.")
            headers = {'X-CoinAPI-Key' : APIKEY_AUX}
            url = "https://rest.coinapi.io/v1/assets"
            respuesta = requests.get(url, headers=headers)
            codigo = respuesta.status_code
            return codigo, APIKEY_AUX
        elif test_APIKEY == "n":
            return "NO_TEST", APIKEY_AUX
continuar = False
codigo = 0
APIKEY_AUX = ""
while continuar == False:
    codigo, APIKEY_AUX = configuracion_APIKEY()
    if codigo == 200:
        print("La APIKEY es valida")
        continuar = True
    elif codigo == "NO_TEST":
        print("La APIKEY no ha sido testada")
        continuar = True
    else:
        print("La APIKEY no es valida")
        respuesta_continuar = peticion("¿Continuar el proceso de instalación? (y/n) ")
        if respuesta_continuar == "n":
            continuar = False
        else:
            continuar = True
            
print("Creando archivo de configuración...")
file_name = "crypto_app/settings.py"
with open(file_name, "w") as file:
    file.write("APIKEY = " + '"'+APIKEY_AUX+'"\n')
    file.write("RUTA_DB = " + '"' + "db/movimientos.db"+'"\n')
    file.write("MONEDAS = " + "['EUR', 'USD', 'BTC', 'XTZ', 'DOGE', 'ETH']")
print("Archivo de configuración creado")
print("Creando base de datos...")
import sqlite3
conexion = sqlite3.connect("db/movimientos.db")
cursor = conexion.cursor()
try:
    cursor.execute('CREATE TABLE "movimientos" ("id" INTEGER NOT NULL UNIQUE, "date" TEXT NOT NULL, "time" TEXT NOT NULL, "moneda_from" TEXT NOT NULL, "cantidad_from" REAL NOT NULL, "moneda_to" NUMERIC NOT NULL, "cantidad_to" REAL NOT NULL, PRIMARY KEY("id" AUTOINCREMENT))')
except sqlite3.OperationalError:
    print("La base de datos ya existe, borrala para crearla de nuevo")
conexion.commit()
conexion.close()
print("Base de datos creada")

file_name = "./.env"
with open(file_name, "w") as file:
    file.write("FLASK_APP=app.py\n")
    file.write("FLASK_ENV=development\n")
print("Archivo .env creado")