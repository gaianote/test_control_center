import shutil
import os
class Generator(object):
    """docstring for Generator"""
    def __init__(self,test_dir_path,project_path):
        super(Generator, self).__init__()
        self.testpath = test_dir_path
        self.projectpath = project_path

        self.item_order = 1
        if self.projectpath not in ['/','']:
            self.initenv()
    def initenv(self):
        try:
            shutil.rmtree(self.testpath)
            os.mkdir(self.testpath)
        except Exception as e:
            print(e)

    def genentry(self,libpath,reportpath):
        file = """
import sys
import unittest
sys.path.append('{}')
from HTMLTestReportCN import run_suite
discover = unittest.defaultTestLoader.discover('test',pattern="test_*.py")
run_suite(discover,'{}')
""".format(libpath,reportpath)
        entrypaht = os.path.join(self.projectpath,'__test_center_entry__.py')
        with open(entrypaht,'w+',encoding='utf-8') as f:
            f.write(file)

    def gengroup(self,group_name,group_order):
        self.filepath = os.path.join(self.testpath,'test_' + str(group_order)+'_'+group_name+'.py')
        with open(self.filepath,'a+',encoding = 'utf-8') as f:
            f.write("import unittest\n")
            f.write("import sys\n")
            f.write("sys.path.append('{}')\n".format(self.projectpath))
            f.write("from zeus import Zeus\n")
            f.write("class {group_name}(unittest.TestCase,Zeus):\n".format(group_name = group_name))
    def genitem(self,item_name):
        with open(self.filepath,'a+',encoding = 'utf-8') as f:
            if item_name  in ['setUp','setUpClass','tearDown','tearDownClass']:
                f.write("  def {func}(self):\n".format(func = item_name))
            else:
                f.write("  def test_{:0>2d}_{func}(self):\n".format(self.item_order,func = item_name))
                self.item_order += 1
    def genstep(self,step_method,step_value):
        with open(self.filepath,'a+',encoding = 'utf-8') as f:
            f.write("    self.{func}({params})\n".format(func = step_method,params = step_value))


if __name__ == '__main__':
    generator = Generator('/mnt/c/Users/00807/Desktop/resilio/toyou/code/核心测试用例/center_test/test')

