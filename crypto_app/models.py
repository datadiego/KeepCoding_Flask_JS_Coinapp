import sqlite3
from crypto_app.settings import MONEDAS, RUTA_DB
from datetime import datetime, date, time

class DBManager:
    def __init__(self, ruta):
        self.ruta = ruta

    def consultaConParametros(self, consulta, params): 
        conexion = sqlite3.connect(self.ruta)
        cursor = conexion.cursor()
        resultado = False
        try:
            cursor.execute(consulta, params)
            conexion.commit()
            resultado = True
        except Exception as error:
            conexion.rollback()
        conexion.close()
        return resultado

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
        
        for elem in data["data"]:
            valores_monedas[elem["moneda_from"]] -= elem["cantidad_from"]
            valores_monedas[elem["moneda_to"]] += elem["cantidad_to"]
            
        for key in list(valores_monedas):
            if valores_monedas[key] < 0.0:
                del valores_monedas[key]
        output = {"status":"success", "data":valores_monedas}
        return output
    def comprueba_db_creada(self): 
        try:
            file = open(RUTA_DB)
            file.close()
        except FileNotFoundError:
            conexion = sqlite3.connect(RUTA_DB)
            cursor = conexion.cursor()
            cursor.execute('CREATE TABLE "movimientos" ("id" INTEGER NOT NULL UNIQUE, "date" TEXT NOT NULL, "time" TEXT NOT NULL, "moneda_from" TEXT NOT NULL, "cantidad_from" REAL NOT NULL, "moneda_to" NUMERIC NOT NULL, "cantidad_to" REAL NOT NULL, PRIMARY KEY("id" AUTOINCREMENT))')
            conexion.commit()
            conexion.close()
    def crear_fecha(self):        
        fecha_aux = date.today()
        fecha = ""
        try:
            fecha = fecha_aux.strftime('%d-%m-%Y')
            output = {"status":"success", "data":fecha}
            return output

        except ValueError:
            output = {"status":"failed", "error":"La fecha no es valida"}
            return output
    def crear_hora(self):
        hora = time(datetime.now().hour, datetime.now().minute, datetime.now().second)
        hora = f"{hora.hour}:{hora.minute}:{hora.second}"
        try:
            datetime.strptime(hora, '%H:%M:%S')
            output = {"status":"success", "data":hora}
            return output
        except ValueError:
            output = {"status":"failed", "error":"La hora introducida no es valida"}
            return output
        except TypeError:
            output = {"status":"failed", "error":"La hora introducida no es valida"}
            return output    
    def valida_monedas(self, moneda_from, moneda_to):
        """
        Este método comprueba si las monedas introducidas son validas
        """
        if moneda_from == moneda_to:
            output = {"status":"failed", "error":f"Las monedas {moneda_to} introducidas son iguales"}
            return output
        if moneda_from not in MONEDAS:
            output = {"status":"failed", "error":f"La moneda de origen {moneda_from} no es valida"}
            return output
        if moneda_to not in MONEDAS:
            output = {"status":"failed", "error":f"La moneda de destino {moneda_to} no es valida"}
            return output
        output = {"status":"success"}
        return output
    def valida_cantidad(self, cantidad_from, cantidad_to):
        """
        Este método comprueba si la cantidad introducida es valida
        """
        try:
            cantidad_from = float(cantidad_from)
            cantidad_to = float(cantidad_to)
            output = {"status":"success"}
            return output
        except ValueError:
            output = {"status":"failed", "error":f"La cantidad introducida no es valida"}
            return output
    def saldo_suficiente(self, cantidad_from, moneda_from):
        """
        Este método comprueba si tenemos suficiente saldo para realizar la transacción
        """
        saldo_monedas = self.status_cuenta()
        print(saldo_monedas)
        saldo_monedas = saldo_monedas["data"]
        print(moneda_from)
        
        if moneda_from not in saldo_monedas:
            output = {"status":"failed", "error":f"No tienes suficientes {moneda_from}"}
            return output
        else:    
            if float(cantidad_from) > saldo_monedas[moneda_from]:
                output = {"status":"failed", "error":f"No tienes suficientes {moneda_from}b"}
                return output

            output = {"status":"success"}
            return output
        
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