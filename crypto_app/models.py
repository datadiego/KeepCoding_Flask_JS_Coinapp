import sqlite3
from crypto_app.settings import MONEDAS, RUTA_DB

class DBManager:
    def __init__(self, ruta):
        self.ruta = ruta

    def consultaConParametros(self, consulta, params): #SE SALVA
        conexion = sqlite3.connect(self.ruta)
        cursor = conexion.cursor()
        resultado = False
        try:
            cursor.execute(consulta, params)
            conexion.commit()
            resultado = True
        except Exception as error:
            print("ERROR DB:", error)
            conexion.rollback()
        conexion.close()
        return resultado

    def devuelve_movimientos(self): #SE SALVA
        """
        Este método devuelve un diccionario con todos los movimientos de la DB actuales
        """
        sql = "SELECT * from movimientos ORDER BY id, date, time, moneda_from, cantidad_from, moneda_to, cantidad_to"
        try:
            data = self.consultaSQL(sql)
        except sqlite3.OperationalError:
            output = {
                "status":"fail",
                "error":"Hay un problema con la base de datos"
            }
            return output
        output = {"status":"success", "data":data}
        return output

    def crear_movimiento(self, consulta):

        conexion = sqlite3.connect(self.ruta)
        cursor = conexion.cursor()
        cursor.execute(consulta)
        conexion.commit()
        resultado = cursor.description
        conexion.close()
        return cursor.lastrowid 

    def status_cuenta(self): #SE SALVA
        """
        Este método devuelve un diccionario con el número actual de monedas que tenemos en nuestra wallet
        """
        data = self.devuelve_movimientos()
        
        #Guardamos las monedas que se han usado en nuestros movimientos:
        lista_monedas = []
        for elem in data["data"]: 
            if elem["moneda_from"] not in lista_monedas:
                lista_monedas.append(elem["moneda_from"])
            if elem["moneda_to"] not in lista_monedas:
                lista_monedas.append(elem["moneda_to"])
        
        #Creamos un diccionario con las monedas que poseemos, iniciando a 0 su valor
        valores_monedas = {}
        for moneda in lista_monedas:
            valores_monedas[moneda] = 0
        
        #Sumamos y restamos segun el valor de moneda_from y moneda_to:
        for elem in data["data"]:
            valores_monedas[elem["moneda_from"]] -= elem["cantidad_from"]
            valores_monedas[elem["moneda_to"]] += elem["cantidad_to"]
        #TODO: si el valor de las monedas es cero, se quedan fuera del diccionario
            
        #if value is 0, delete key
        for key in list(valores_monedas):
            if valores_monedas[key] < 0.0:
                del valores_monedas[key]
        output = {"status":"success", "data":valores_monedas}
        return output
    def comprueba_db(self): #SE SALVA
        try:
            file = open(RUTA_DB)
            file.close()
        except FileNotFoundError:
            conexion = sqlite3.connect(RUTA_DB)
            cursor = conexion.cursor()
            cursor.execute('CREATE TABLE "movimientos" ("id" INTEGER NOT NULL UNIQUE, "date" TEXT NOT NULL, "time" TEXT NOT NULL, "moneda_from" TEXT NOT NULL, "cantidad_from" REAL NOT NULL, "moneda_to" NUMERIC NOT NULL, "cantidad_to" REAL NOT NULL, PRIMARY KEY("id" AUTOINCREMENT))')
            conexion.commit()
            conexion.close()
        


def valida_moneda(moneda):
    """
    Este método comprueba si la moneda introducida es válida

    Parámetros:
    moneda: string con la moneda a comprobar
    """
    if moneda not in MONEDAS:
        return False
    else:
        return True