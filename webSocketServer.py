import asyncio
import websockets
import json
import os 
import psycopg2 as pg
from datetime import datetime
from decimal import Decimal

lock_file_path = 'websocket_server.lock'

# Estructura para almacenar los datos recibidos
class Payload:
    def __init__(self):
        self.raw = [0, 0, 0, 0, 0, 0]

# Lista de clientes conectados
clientes = set()

def create_lock_file():
    with open(lock_file_path, 'w') as f:
        f.write('running')

def delete_lock_file():
    os.remove(lock_file_path)

def default_serializer(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')

async def enviar_datos_a_clientes(datos):
    if clientes:
        # Convertir los datos a formato JSON
        datos_json = json.dumps(datos, default=default_serializer)

        # Enviar datos a todos los clientes
        await asyncio.gather(*(cliente.send(datos_json) for cliente in clientes))

async def recibir_datos(websocket):
    global clientes
    clientes.add(websocket)

    try:
        # Conectar a la base de datos
        conn = pg.connect(
            host='192.168.0.22',
            user='postgres',
            port='5050',
            password='Admin123',
            database='djangotest',
        )
        cursor = conn.cursor()

        dataX = []
        dataY = []
        dt = []

        while True:
            # Consulta para obtener los últimos datos de la tabla
            cursor.execute("SELECT air_quality_ppm FROM blog_airquality ORDER BY id DESC LIMIT 1")
            row = cursor.fetchone()
            if row:
                CH1 = float(row[0])
                CH2 = float(row[0])  # Extraer el valor de la tupla
                
                tiempo_transcurrido = datetime.now().isoformat()

                dataX.append(CH1)
                dataY.append(CH2)
                dt.append(tiempo_transcurrido)

                if len(dataX) >= 10:
                    print('sending data')
                    datos = {"CH1": dataX, "CH2": dataY, "Tiempo": dt}
                    # Enviar los datos a todos los clientes conectados
                    await enviar_datos_a_clientes(datos)
                    dataX = []
                    dataY = []
                    dt = []

                # Simulate a delay matching the expected rate of data arrival
                await asyncio.sleep(0.001)  # Ajusta el delay según sea necesario

    except websockets.exceptions.ConnectionClosedError:
        pass
    finally:
        # Eliminar el cliente al desconectarse
        clientes.remove(websocket)
        # Cerrar la conexión con la base de datos
        conn.close()

start_server = websockets.serve(recibir_datos, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
