import os
from tool.some_tool import SomeTool

class PanTool:
    @staticmethod
    def folder(path):
        # 获取文件夹下的所有文件以及文件夹，以及此目录和上一级目录
        abspath = os.getcwd() + '\\'
        current = 'static' + str(abspath + path).split('static')[1]
        folders, files = [], []
        for f in os.listdir(abspath + path):
            if os.path.isfile(current + '\\' + f):
                files.append(str(current + '\\' + f).replace('\\', '/'))
            else :
                folders.append(str(current + '\\' + f).replace('\\', '/'))
        if current.replace('\\', '/').split('/').pop(-2) == 'pan':
            last = current
        else:
            last = current.split('/')
            last.pop(-1)
            last = '/'.join(last)
        return {'last': last.replace('\\', '/'), 'current': current.replace('\\', '/'),
                'folders': folders, 'files': files}

    @staticmethod
    def add_folder(folder, current):
        # 添加文件夹
        abspath = os.getcwd() + '\\' + current + '\\' + folder
        if os.path.exists(abspath) != True:
            os.mkdir(abspath)

    @staticmethod
    def add_file(file, filename, current):
        # 上传文件
        abspath = os.getcwd() + '\\' + current + '\\' + str(filename).split('\\')[-1]
        with open(abspath, 'wb', ) as f:
            f.write(file)