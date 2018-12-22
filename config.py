import os
class Config(object):
    """docstring for Config"""
    def __init__(self):
        self.basepath = os.path.abspath(os.path.dirname(__file__))
        self.reportpath = os.path.join(self.basepath,'templates','report')
        self.libpath = os.path.join(self.basepath,'lib')
        self.databasepath = os.path.join(self.basepath,'database','database.db')
        # self.database = Sqlite(self.databasepath)
config  = Config()
# database = config.database
