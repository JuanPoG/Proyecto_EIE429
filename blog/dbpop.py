import dbclass1 as dp
import datetime
raspidB = dp.dbConnection('192.168.0.22', '5050', 'djangotest', 'postgres', 'Admin123')
raspidB.conn2dB()

from random import random

delta=0
currenTime= datetime.datetime.now()

#sqlQuery = "INSERT INTO blog_red(userid, location) VALUES(1, 'valaparaiso');"
#raspidB.write2dB(sqlQuery)

#for i in range(1,5):
#    sqlQuery = "INSERT INTO blog_nodesregister(createdtime, nodenumber) VALUES(CURRENT_TIMESTAMP, 1);"
#    raspidB.write2dB(sqlQuery)
for node in range(1,5):
    for i in range(1,100):
        sqlQuery = "INSERT INTO blog_nodes(sampletime, nodenumber_id) VALUES("+"'"+currenTime.strftime('%Y-%m-%d %H:%M:%S')+"'"+", "+str(node)+");"
        raspidB.write2dB(sqlQuery)

        sqlQuery = 'INSERT INTO blog_temperature("alarmTemp", temp, node_id) VALUES(FALSE, '+str(round(random()*100,2))+','+str(node)+');'
        raspidB.write2dB(sqlQuery)
        delta=60
        currenTime=currenTime+datetime.timedelta(0,delta)