# 测试步骤
from .sql import Sqlite
from config import Config

class Step(Sqlite):
    """docstring for project"""
    def __init__(self):
        super().__init__(Config().databasepath)
    def create(self,item_id,description,method,value,user):
        # 创建一个步骤，并返回刚刚创建的项目id
        return self.insert('step', ITEM_ID = item_id,DESCRIPTION = description,METHOD = method,VALUE = value,USER = user,CREATE_DATE = self.get_date())
    def get_step_list(self,item_id):
        '''返回所有的对应project_id 的 item'''
        title = self.fetchone('item','NAME',where = 'where id = %s'%item_id)[0]
        items = self.fetchall('step','ID','DESCRIPTION','METHOD','VALUE','CREATE_DATE',where = 'where item_id = %s'%item_id)
        return title,items
    def delete(self,step_id):
        '''创建一个tem'''
        return super().delete('step', 'where id = %s'%step_id)
step = Step()