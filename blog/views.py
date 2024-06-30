from django.shortcuts import render, redirect
import subprocess
import psutil
from django.http import HttpResponse, JsonResponse
from .models import nodes, temperature
from . import dbclass1 as dp


def index(request):
    title='index IOT'
    return render(request, 'index.html',{
        'title': title
    })

def hello(request, username):
    print(username)
    return HttpResponse("<h1>username: %s</h1>" % username)

def about(request):
    title='about IOT'
    return render(request, 'about.html', {
        'title': title
    })

def vistaDePrueba(request):
    return HttpResponse("<h3>texto de prueba</h3>")

def sensor(request):
    Nodes = list(nodes.objects.values())
    #print(Nodes)
    return render(request, 'nodes.html',{
        'nodes': Nodes
    })

def temp(request, id):
    #TEMP = temperature.objects.get(id=id)
    #TEMP = [TEMP.id, TEMP.temp]
    #return render(request, 'temperature.html',{
    #    'temp': TEMP
    #})
    raspidB = dp.dbConnection('192.168.0.22', '5050', 'djangotest', 'postgres', 'Admin123')
    raspidB.conn2dB()
    sqlQuery = 'select ns.id, ns.location, ns.sample_time, tempe.temp From blog_temperature tempe inner join blog_nodes ns on tempe.id = ns.id;'
    tempData= raspidB.query2dB(sqlQuery)
    print(tempData)
    return render(request, 'temperature.html',{
        'temp': tempData
    })


def hum(request, id):
    #TEMP = temperature.objects.get(id=id)
    #TEMP = [TEMP.id, TEMP.temp]
    #return render(request, 'temperature.html',{
    #    'temp': TEMP
    #})
    raspidB = dp.dbConnection('192.168.0.22', '5050', 'djangotest', 'postgres', 'Admin123')
    raspidB.conn2dB()
    sqlQuery = 'select ns.id, ns.location, ns.sample_time, hum.humidity From blog_humidity hum inner join blog_nodes ns on hum.id = ns.id;'
    humData= raspidB.query2dB(sqlQuery)
    return render(request, 'humidity.html',{
        'hum': humData
    })


def air(request, id):
    #TEMP = temperature.objects.get(id=id)
    #TEMP = [TEMP.id, TEMP.temp]
    #return render(request, 'temperature.html',{
    #    'temp': TEMP
    #})
    raspidB = dp.dbConnection('192.168.0.22', '5050', 'djangotest', 'postgres', 'Admin123')
    raspidB.conn2dB()
    sqlQuery = 'select ns.id, ns.location, ns.sample_time, air.air_quality_ppm From blog_airquality air inner join blog_nodes ns on air.id = ns.id;'
    airData= raspidB.query2dB(sqlQuery)
    return render(request, 'air.html',{
        'air': airData
    })



def test(request, id):
    raspi = dp.dbConnection('192.168.0.22', '5050', 'djangotest', 'postgres', 'Admin123')
    raspi.conn2dB()
    sqlQuery = 'select ns.id, ns.location, ns.sample_time, tempe.temp From blog_temperature tempe inner join blog_nodes ns on tempe.id = ns.id ORDER BY ns.id ASC;'
    tempData = raspi.query2dB(sqlQuery)
    sqlQuery = 'select ns.id, ns.location, ns.sample_time, hum.humidity From blog_humidity hum inner join blog_nodes ns on hum.id = ns.id ORDER BY ns.id ASC'
    humData= raspi.query2dB(sqlQuery)
    sqlQuery = 'select ns.id, ns.location, ns.sample_time, air.air_quality_ppm From blog_airquality air inner join blog_nodes ns on air.id = ns.id ORDER BY ns.id ASC'
    airData= raspi.query2dB(sqlQuery)

    times_1 = [record[2].strftime('%Y-%m-%d %H:%M:%S') for record in tempData]
    data_1 = [float(record[3]) for record in tempData]
    times_2 = times_1
    data_2 = [float(record[3]) for record in humData]
    times_3 = times_1
    data_3 = [float(record[3]) for record in airData]

    #print(data_4)
    return render(request, 'test.html',{
        'times_1': times_1,
        'data_1': data_1,
        'times_2': times_2,
        'data_2': data_2,
        'times_3': times_3,
        'data_3': data_3,

    })  


def rtplot(request):
    #lock_file_path = 'websocket_server.lock'
    #if not os.path.exists(lock_file_path):

    return render(request, 'rtplot.html',{
        'callWebsocket': True
    })
   
