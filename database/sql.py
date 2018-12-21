import sqlite3
from functools import wraps
import datetime
import time
import os

def cursor(func):
    @wraps(func)
    def wrapper(self,*args, **kwargs):
        self.conn = sqlite3.connect(self.tablebase)
        self.cursor = self.conn.cursor()
        result = func(self,*args, **kwargs)
        self.cursor.close()
        self.conn.commit()
        self.conn.close()
        return result
    return wrapper

class Sqlite():
    def __init__(self,tablebase):
        self.tablebase = tablebase

    def get_date(self):
        '''
        返回当前的日期，格式为'2018-10-1 12:2:30'的字符串
        '''
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return date
    def get_timeStamp(self):
        return int(round(time.time() * 1000))
    @cursor
    def execute(self,sql,*args):
        self.cursor.execute(sql,*args)
        if sql.startswith('INSERT'):

            return int(self.cursor.lastrowid)

    @cursor
    def create_table(self,tablename,**kw):
      header = ','.join(['{0} {1}'.format(key,kw[key]) for key in kw.keys()])
      sql = 'CREATE TABLE {tablename}({header})'.format(tablename = tablename,header = header)
      print(sql)
      self.cursor.execute(sql)

    @cursor
    def insert(self,tablename,**kw):
        header = ','.join(kw.keys())
        value = ','.join(["'{0}'".format(key) if isinstance(key,str) else str(key) for key in kw.values()])
        sql = "INSERT INTO {tablename} ({header}) VALUES ({value})".format(tablename = tablename,header = header,value = value)
        self.cursor.execute(sql)
        return int(self.cursor.lastrowid)

    def _select(self,tablename,*keys,where = ''):
        headers = ','.join(keys)
        sql = "SELECT {0} from {1} {2}".format(headers,tablename,where)
        result = self.cursor.execute(sql)
        return result
    @cursor
    def update(self,tablename,key,value,where):
        self.cursor.execute("UPDATE {0} set {1} = {2} {3}".format(tablename,key,value,where))
    @cursor
    def delete(self,tablename,where):
        self.cursor.execute("DELETE from {} {}".format(tablename,where))
    # @cursor
    # def fetchall(self,tablename,*keys,where = ''):
    #     result = self._select(tablename,*keys,where = where)
    #     return result.fetchall()
    # @cursor
    # def fetchone(self,tablename,*keys,where = ''):
    #     result = self._select(tablename,*keys,where = where)
    #     return result.fetchone()
    @cursor
    def fetchall(self,sql,*args):

        return self.cursor.execute(sql,*args).fetchall()
    @cursor
    def fetchone(self,sql,*args):

        return self.cursor.execute(sql,*args).fetchone()


basepath = os.path.abspath(os.path.dirname(__file__))
databasepath = os.path.join(basepath,'database.db')
sqlite = Sqlite(databasepath)