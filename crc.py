import psycopg2
import serial
import time
import datetime

try:
    connection= psycopg2.connect(
        host='192.168.0.22',
        user='postgres',
        port='5050',
        password='Admin123',
        database='djangotest',
    )
    print("conexion exitosa")
    cursor=connection.cursor()
    cursor.execute("SELECT * FROM blog_temperature")
    rows=cursor.fetchall()

    arduino = serial.Serial('COM4', baudrate=9600, timeout=2.0) #conexion arduino
    arduino.setDTR(False)



    time.sleep(1)
    arduino.flushInput()
    arduino.setDTR(True)
    datos_db = []
    while True:
        datos = arduino.readline() # recibe los datos
        datos_split = datos.split()
        #print(datos_split)
        if len(datos_db)>=3:
                datos_db.clear()
                datos_db.clear()
        for i in range(len(datos_split)):
            byt2str = datos_split[i].decode("utf-8") #convierte byte a string
            dec = float(byt2str) # convierte en decimal
            if i == 0:
                datos_db.append(dec)
        
            if i == 1:
                datos_db.append(dec)

            if i == 2:
                datos_db.append(dec)
                if datos_db[1]>20.0:
                     tAlarm=False
                else:
                     tAlarm=True
                if datos_db[0]>70.0:
                     hAlarm=False
                else:
                     hAlarm=True
                if datos_db[1]>1000.0:
                     aqAlarm=False
                else:
                     aqAlarm=True

                   # Obtener la fecha y hora actual
                hora_actual = datetime.datetime.now()

                formato_deseado = hora_actual.strftime("%Y-%m-%d %H:%M:%S")
                hora="'"+str(formato_deseado)+"'"
                lugar="'"+"Valparaiso"+"'"
                descrip="'"+"Arduino con sensores ambientales"+"'"
                cursor.execute('INSERT INTO blog_nodes("sample_time", "location", "description") VALUES('+str(hora)+', '+str(lugar)+' , '+str(descrip)+');')
                connection.commit()

                cursor.execute('INSERT INTO blog_temperature("alarmTemp", "temp", nodes_id) VALUES('+str(tAlarm)+',' + str(datos_db[1]) + ',1);')
                connection.commit()

                cursor.execute('INSERT INTO blog_humidity("alarmHum", "humidity", nodes_id) VALUES('+str(hAlarm)+',' + str(datos_db[0]) + ',1);')
                connection.commit()

                cursor.execute('INSERT INTO blog_airquality("alarm_air_quality", "air_quality_ppm", nodes_id) VALUES('+str(aqAlarm)+',' + str(datos_db[2]) + ',1);')
                connection.commit()
                

except Exception as ex:
    print(ex)