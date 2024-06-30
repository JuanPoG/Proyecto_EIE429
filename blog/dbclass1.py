import psycopg2 as pg
import pandas as pd

class dbConnection(object):

    def __init__(self, host, port, dbName, user, password):
        self.host = host
        self.port = port
        self.dbName = dbName
        self.user = user
        self.password = password

    def conn2dB(self):
        self.connection = pg.connect(host=self.host, port=self.port, dbname=self.dbName, user=self.user, password=self.password)
        return "connection succesfull"

    def query2dB(self, incQuery):
        conn = self.connection
        cur = conn.cursor()
        cur.execute(incQuery)
        return cur.fetchall()


    def write2dB(self, incQuery):
        conn = self.connection
        try:
            cur = conn.cursor()
            cur.execute(incQuery)
            conn.commit()
            return "write successful"
        except:
            return "error in process of writing to the dB"

    def dfQuery(self, sqlQuery):
        return pd.read_sql_query(sqlQuery, self.connection)
