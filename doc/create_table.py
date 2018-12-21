from sql import Sqlite
import datetime
def get_time():
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(time)
    return time
database = Sqlite('database')
# database.create_table('PROJECT',ID = 'INTEGER PRIMARY KEY AUTOINCREMENT', NAME = 'TEXT',INFO = 'TEXT',DATE = 'TEXT')
# database.create_table('ITEM',ID = 'INTEGER PRIMARY KEY AUTOINCREMENT', NAME = 'TEXT',INFO = 'TEXT',DATE = 'TEXT')

database.insert('ITEM', NAME = 'TEXT',INFO = 'TEXT',DATE = get_time())
id = database.fetchone('ITEM','DATE','NAME',where = 'where id = 9')
print(id)