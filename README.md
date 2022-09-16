# KeepCoding_Flask_JS_Coinapp
Proyecto realizado durante el fin de la edicion XI del bootcamp cero en keepcoding.io
Esta aplicacion web te permite consultar el precio de varias criptomonedas a coinapi.io y almacenar movimientos entre monedas para consultar inversiones.
[imagen]

## Características:
- Script para configurar la aplicación, ejecutalo y sigue sus instrucciones para lanzar tu aplicación de flask mas rápido
- Realiza consultas del valor de criptomonedas a través de la API de coinapi.io
- Realiza movimientos a una base de datos donde almacenar movimientos
- Muestra un listado de movimientos con sus datos en la parte principal
- Muestra la cantidad total de activos positivos en la cuenta en la parte inferior
- La aplicación crea automaticamente una base de datos nueva en caso de perder la original
- Muestra los errores posibles en pantalla
- Interfaz simple
- Tema claro/oscuro

# Instalación de la aplicacion

- Descarga el repositorio

```
git clone https://github.com/datadiego/KeepCoding_Flask_JS_Coinapp.git
```

- Crea un entorno virtual en la carpeta raiz del repositorio y actívalo.

En windows:
```
python -m venv env
.\env\Scripts\activate
```
En mac/linux:
```
python -m venv env
source ./bin/scripts/activate
```
- Instala las dependencias

Si solo vas a usar la aplicación:

```
pip install -r requirements.txt
```

Si quieres desarrollarla:

```
pip install -r requierements.dev.txt
```

# Configuración de aplicación
Antes de iniciar la aplicación, debemos configurarla:
- Si no tienes aun una *APIKEY* de [coinapi.io](http://coinapi.io), regístrate y copia tu *APIKEY*.

- Puedes configurar la aplicación ejecutando y siguiendo las instrucciones del instalador:
```
python instalador.py
```
- Sigue sus instrucciones y al finalizar, lanza la aplicación con:
```
flask run
```

Si prefieres realizar esta configuración de manera manual:

- Localiza el archivo `env_template`, edítalo para que quede así:

```
FLASK_APP=app.py
FLASK_ENV=development
```
- Renombra `env_template` a .`env`

- Localiza el archivo `settings.py`, pega tu *APIKEY* en la variable correspondiente:
```
APIKEY = "Añade aqui tu APIKEY de coinapi.io"
RUTA_DB = "db/movimientos.db"
MONEDAS = ['EUR', 'USD', 'BTC', 'XTZ', 'DOGE', 'ETH'] #Añade otras monedas aqui
```
- Lanza tu aplicacion:
```
flask run
```