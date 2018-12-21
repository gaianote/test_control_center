import os
import re

def get_file_list(dirpath,filetype):
    file_list = []
    list_dirs = os.walk(dirpath)
    for root, dirs, files in list_dirs:
        if root.find('.git') != -1 or root.find('__pycache__') != -1:
            continue
        for f in files:
            filepath = os.path.join(root,f)
            if f.endswith(filetype):
                file_list.append(filepath)
    return file_list

file_list = get_file_list('C:\\Users\\00807\\Desktop\\resilio\\toyou\\code\\核心测试用例\\center_test\\zeus','.py')

def get_funcname(file_list):
    func_list = []
    func_dict = {}
    for file in file_list:
        with open(file,'r',encoding = 'utf-8') as f:
            line = f.readline()
            while line:
                if line.strip().startswith('def ') and not line.strip().startswith('def _'):
                    result = re.compile(r'def\s*?(\S*?)\((.*?)\)').search(line)
                    name = result.group(1)
                    param = result.group(2).replace(' ','').replace('self,','').replace('self','').replace(',*args','').replace(',**kwargs','')
                    func_list.append(name)
                    func_dict[name] = param

                line = f.readline()

    return func_list,func_dict

if __name__ == '__main__':
    print(get_funcname(file_list))