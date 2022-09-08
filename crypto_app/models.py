import sqlite3
from crypto_app.settings import MONEDAS
# from crypto_app.views import valor_monedas

class DBManager:
    def __init__(self, ruta):
        self.ruta = ruta
    
    def consultaSQL(self, consulta):
        """
        Método genérico de consulta a la base de datos

        Parámetros:
        consulta: string con la petición escrita en sqlite
        """
        conexion = sqlite3.connect(self.ruta)
        cursor = conexion.cursor()
        cursor.execute(consulta)

        self.movimientos = []
        nombres_columnas = []

        for desc_columna in cursor.description:
            nombres_columnas.append(desc_columna[0])
        datos = cursor.fetchall()

        for dato in datos:
            movimiento = {}
            indice = 0
            for nombre in nombres_columnas:
                movimiento[nombre] = dato[indice]
                indice += 1
            self.movimientos.append(movimiento)
        conexion.close()
        return self.movimientos

    def devuelve_movimientos(self):
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
        """
        Este metodo crea un movimiento nuevo en la DB

        Parámetros:
        consulta: string con la peticion escrita en sqlite
        """
        #TODO: Crear la peticion de sqlite aqui
        conexion = sqlite3.connect(self.ruta)
        cursor = conexion.cursor()
        cursor.execute(consulta)
        conexion.commit()
        resultado = cursor.description
        conexion.close()
        return cursor.lastrowid 

    def status_cuenta(self):
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

def valida_moneda(moneda):
    """
    Este método comprueba si la moneda introducida es válida

    Parámetros:
    moneda: string con la moneda a comprobar
    """
    if moneda in MONEDAS:
        return True
    else:
        return False