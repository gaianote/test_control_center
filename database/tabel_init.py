from sql import Sqlite
import datetime
def get_time():
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(time)
    return time
# IS_DELETED 删除状态 1 非删除状态 0
# IS_EXECUTE 执行状态 checked 执行状态 ''
database = Sqlite('database.db')
# 名称，信息，创建日期，修改日期，创建人
# STATE:free busy complete
database.create_table('PROJECT',ID = 'INTEGER PRIMARY KEY AUTOINCREMENT', NAME = 'TEXT',INFO = 'TEXT',CREATE_DATE = 'TEXT',UPDATE_DATE = 'TEXT',USER = 'TEXT',SORTORDER = 'INTEGER',IS_DELETED = 'INTEGER',STATE = 'TEXT',LOOP = 'INTEGER',PROJECTPATH = 'TEXT',ENTRYORDER = 'TEXT',TEXTPATH = 'TEXT')
database.create_table('[GROUP]',ID = 'INTEGER PRIMARY KEY AUTOINCREMENT', PROJECT_ID = 'INTEGER',NAME = 'TEXT',INFO = 'TEXT',CREATE_DATE = 'TEXT',UPDATE_DATE = 'TEXT',USER = 'TEXT',SORTORDER = 'INTEGER',IS_DELETED = 'INTEGER',IS_EXECUTE = 'TEXT',LOOP = 'INTEGER')
database.create_table('ITEM',ID = 'INTEGER PRIMARY KEY AUTOINCREMENT', GROUP_ID = 'INTEGER',NAME = 'TEXT',INFO = 'TEXT',CREATE_DATE = 'TEXT',UPDATE_DATE = 'TEXT',USER = 'TEXT',SORTORDER = 'INTEGER',IS_DELETED = 'INTEGER',IS_EXECUTE = 'TEXT',LOOP = 'INTEGER',TYPE = 'TEXT')
database.create_table('STEP',ID = 'INTEGER PRIMARY KEY AUTOINCREMENT', ITEM_ID = 'INTEGER',DESCRIPTION = 'TEXT',METHOD = 'TEXT',VALUE = 'TEXT',CREATE_DATE = 'TEXT',UPDATE_DATE = 'TEXT',USER = 'TEXT',SORTORDER = 'INTEGER',IS_DELETED = 'INTEGER',IS_EXECUTE = 'TEXT',LOOP = 'INTEGER',ASSERT = 'TEXT')
database.create_table('REPORT',ID = 'INTEGER PRIMARY KEY AUTOINCREMENT', PROJECT_ID = 'INTEGER',DESCRIPTION = 'TEXT',CREATE_DATE = 'TEXT',END_DATE = 'TEXT',STATE = 'TEXT')

database.execute("""
CREATE TRIGGER log_time_project AFTER INSERT ON PROJECT
BEGIN
   UPDATE PROJECT SET SORTORDER = new.ID, CREATE_DATE = datetime('now'),IS_DELETED = 0,LOOP = 1,STATE = 'FREE' WHERE ID = new.ID;
END;
""")
database.execute("""
CREATE TRIGGER log_time_group AFTER INSERT ON [GROUP]
BEGIN
   UPDATE [GROUP] SET SORTORDER = new.ID, CREATE_DATE = datetime('now'),IS_DELETED = 0,LOOP = 1 ,IS_EXECUTE = "checked" WHERE ID = new.ID;
END;
""")
database.execute("""
CREATE TRIGGER log_time_item AFTER INSERT ON ITEM
BEGIN
   UPDATE ITEM SET SORTORDER = new.ID, CREATE_DATE = datetime('now'),IS_DELETED = 0,LOOP = 1 ,IS_EXECUTE = "checked" WHERE ID = new.ID;
END;
""")
database.execute("""
CREATE TRIGGER log_time_step AFTER INSERT ON STEP
BEGIN
   UPDATE STEP SET SORTORDER = new.ID, CREATE_DATE = datetime('now'),IS_DELETED = 0,LOOP = 1 ,IS_EXECUTE = "checked" WHERE ID = new.ID;
END;
""")
#  成功/失败/初始化失败/
database.execute("""
CREATE TRIGGER log_time_report AFTER INSERT ON REPORT
BEGIN
   UPDATE REPORT SET CREATE_DATE = datetime('now') WHERE ID = new.ID;
END;
""")