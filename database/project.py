from .sql import Sqlite
from config import Config
class Project(Sqlite):
    """docstring for project"""
    def __init__(self):
        super().__init__(Config().databasepath)
    def create(self,name,info,user):
        # 创建一个项目，并返回刚刚创建的项目id
        return self.insert('project', NAME = name,INFO = info,USER = user,CREATE_DATE = self.get_date())

    def delete(self,project_id):
        return super().delete('project','where id = %s'%project_id)
    def get_project_list(self):
        # 返回项目列表
        return self.fetchall('project','ID','NAME','INFO','USER','CREATE_DATE')

    def create_item(self,project_id,name,info,user):
        return self.insert('item', PROJECT_ID = project_id,NAME = name,INFO = info,USER = user,CREATE_DATE = self.get_date())
project = Project()