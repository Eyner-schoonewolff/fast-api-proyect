#  Arquitectura 

Para el diseño de la arquitectura de carpetas utilice el patron DDD (Domain Driven Design) 
el cual lo elegi ya que es a la hora de modular el software es muy sencillo el relizarle optimizaciones o mantemintiento 
de pequeños modulos el cual lo hace muy robusto y a la vez escalable.

# Documentacion para configurar ambiente para la API Prueba Tecnica FastApi


requerimientos para funcionalidad de la API

tener instalado en tu maquina python3.11

en este caso yo use el python3.11.5

# instalar entorno virtual en python

python3 -m venv nombre_del_entorno

# acceder al entorno 

en Windows

 - nombre_del_entorno\Scripts\activate

 en MacOs o Linux

 - source nombre_del_entorno/bin/activate

# instalar todos los paquetes que estan en el archivo requirements.txt

- pip install -r requirements.txt

#  tener en cuenta que las tablas ya esten importadas en un adminitrador de base de datos (MariaDB)

- modificar el .env con las credenciales de tu base de datos

DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = ''
DB_PORT = '3300'
DB_NAME = 'proyectoFast'

- luego importar las tablas que estan en el archivo de tables-sql con sus relaciones 

# ejecuta el siguiente comando en tu terminal para iniciar el servidor API

uvicorn app.main:app --reload

# para probar las apis se encuentra la docuemntacion de las Apis en 
 -  127.0.0.1:8000/docs
