import shutil
import os
class Generator(object):
    """docstring for Generator"""
    def __init__(self, path):
        super(Generator, self).__init__()
        self.testpath = path
        self.item_order = 1
        if path != '/':
            self.initenv()
    def initenv(self):
        shutil.rmtree(self.testpath)
        os.mkdir(self.testpath)
    def gengroup(self,group_name,group_order):
        self.filepath = os.path.join(self.testpath,'test_' + str(group_order)+'_'+group_name+'.py')
        with open(self.filepath,'a+',encoding = 'utf-8') as f:
            f.write("import unittest\n")
            f.write("from zeus import Zeus\n")
            f.write("class {group_name}(unittest.TestCase,Zeus):\n".format(group_name = group_name))
    def genitem(self,item_name):
        with open(self.filepath,'a+',encoding = 'utf-8') as f:
            f.write("  def test_{:0>2d}_{func}(self):\n".format(self.item_order,func = item_name))
            self.item_order += 1
    def genstep(self,step_method,step_value):
        with open(self.filepath,'a+',encoding = 'utf-8') as f:
            f.write("    self.{func}({params})\n".format(func = step_method,params = step_value))

if __name__ == '__main__':
    generator = Generator('/mnt/c/Users/00807/Desktop/resilio/toyou/code/核心测试用例/center_test/test')


# import unittest
# from zeus import Zeus
# class Env(unittest.TestCase,Zeus):
#     def test_env(self):
#         self.login()
#         self.set_free_disk()
#         self.set_ip(ctrl_idx=0,port=0,address='192.168.71.131')
#         self.set_ip(ctrl_idx=0,port=1,address='192.168.71.132')
#         self.set_ip(ctrl_idx=0,port=2,address='192.168.71.133')
#         self.set_ip(ctrl_idx=0,port=3,address='192.168.71.134')
#         self.set_ip(ctrl_idx=0,port=4,address='192.168.71.135')
#         self.set_ip(ctrl_idx=0,port=5,address='192.168.71.136')
#         self.set_ip(ctrl_idx=1,port=0,address='192.168.71.141')
#         self.set_ip(ctrl_idx=1,port=1,address='192.168.71.142')
#         self.set_ip(ctrl_idx=1,port=2,address='192.168.71.143')
#         self.set_ip(ctrl_idx=1,port=3,address='192.168.71.144')
#         self.set_ip(ctrl_idx=1,port=4,address='192.168.71.145')
#         self.set_ip(ctrl_idx=1,port=5,address='192.168.71.146')
#         self.clear_log()