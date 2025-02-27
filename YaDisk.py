version = 0.1
import yadisk
from io import BytesIO, BufferedReader
import json
import json5
import importlib
import os

class YaDisk:

    def loadInfo(filename):
        absPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', filename)
        with open(absPath, 'r', encoding='utf-8') as file:
            info = json5.load(file)['YaDisk']  
            return {
                "key": info["key"],
                "dirScripts": info["dirSRC"],
                "dirModules": info["dirML"],
                "dirCore": info["dirC"],
            }
            file.close()

    def connect(infoDisk):
        try:
            disk = yadisk.Client(infoDisk['key'])
            return disk
        except Exception:
            return False

    def checkVersion(name, disk, buffer=BytesIO()):
        disk.download(name, buffer)
        buffer.seek(0)

        result = importlib.import_module(BufferedReader(buffer)).version
        buffer.truncate(0)
        buffer.seek(0)
        return result

    def checkVersionFull(disk, diskInfo, buffer=BytesIO()):
        mainDisk = disk
        result = {'dirScripts': {}, 'dirModules': {}, 'dirCore': {}}

        for k, v in result.items():
            for i in disk.listdir(diskInfo[k]):
                mainDisk.download(f"{diskInfo[k]}/{i}", buffer)
                buffer.seek(0)
                result[k][i] = importlib.import_module(BufferedReader(buffer)).version
                buffer.truncate(0)
                buffer.seek(0)
        return result

    def getListFiles(disk, folder):
        return disk.listdir(f'{folder}')

    def downloadUpdate(disk, folder, pathDownload):
        try:
            disk.download(folder, pathDownload)
            return True
        except Exception:
            return False

if __name__ == '__main__':
    pass
