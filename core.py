import FDP as local
import bot as bot
import YaDisk as cloud
import os
import time
import threading
class LoadDatas:
    def __init__(self, filesFolder):
        self.mainFolder = filesFolder
        filesFolder = {
        "mainProgrammInfo": f"{self.mainFolder}/kap.json",
        "mainScriptBase": f"{self.mainFolder}/scriptBase.json"
        }
        if self.tryLoadMainFiles():
           return {
                "forBot": { "mainInfo": json.dumps(bot.mainBot.loadInfo(filesFolder['mainProgrammInfo'])),
                            "sripBase": json.dumps(bot.mainBot.loadScriptBase(filesFolder['mainScriptBase']))
                },
                "forLocal": {
                    "mainInfo": local.Files.loadInfo(filesFolder['mainProgrammInfo']),
                    "scriptBase": local.Files.loadInfo(filesFolder['mainScriptBase'])
                },
                "forCloud":{
                    "mainInfo": cloud.YaDisk.loadInfo(filesFolder['mainProgrammInfo'])
                }
            }
        def tryLoadMainFiles(self):
    
            a = []
            for i in os.listdir(self.mainFolder):
                try:
                    a[i]
                    a[i] = local.Files.loadInfo()
                    print(f"Файл: {i} успешно найден и загружен")
                    return True
                except FileNotFoundError:
                    print(f"Ошибка, файл не найден: {i}")
                    return False
                except AttributeError:
                    print(f"Невозможно прочитать файл: {i}")
                    return False
            del a
class fromFileWork:
    def __init__(self, infoCloud, infoLocal):
        self.disk = cloud.Yadisk.connect(infoCloud)
        self.info = {"cloud": infoCloud, "local": infoLocal}

    def update(self, type="script", nameFile=None):
        if type == "script":
            if cloud.Yadisk.checkVersion(f"/RI.Remote.Core/{nameFile}.py", self.disk) > local.Files.getVersion(f"/mainModule/{nameFile}.py"):
                os.remove(nameFile)
                cloud.Yadisk.download(self.disk, f"/RI.Remote.Scripts/{nameFile}.py", f"/scripts/{nameFile}.py")
                return True
            else:
                return "object no need to update"

        if type == "core":
            if cloud.Yadisk.checkVersion("/RI.Remote.Core/core.py", self.disk) > local.Files.getVersion("/mainModule/core.py"):
                os.remove("/mainModule/core")
                cloud.Yadisk.download(self.disk, "/RI.Remote.Core/core.py", "/mainModule/core.py")
                return True
            else:
                return "object no need to update"

        if type == "modules":
            modules = ['FDP.py', "core.py", "bot.py"]
            for i in modules:
                if cloud.Yadisk.checkVersion(f"/RI.Remote.Scripts/{i}", self.disk) > local.Files.getVersion(f"/mainModule/{i}.py"):
                    os.remove(i)
                    cloud.Yadisk.download(self.disk, f"/RI.Remote.Modules/{i}.py", f"/mainModule/{i}")
                    return True
            return "object no need to update"

    def getScripts(self):
        listLocalScripts = {} 
        listCloudScripts = {}

        for k, v in self.info['local']['scriptBase'].items():
            listLocalScripts[k] = v["version"]

        for k, v in cloud.getListFiles('/RI.Remote.Scripts', self.disk).items():
            listCloudScripts[k] = cloud.Yadisk.checkVersion(v["path"], self.disk)

        for k, v in listCloudScripts.items():
            if k not in listLocalScripts or listCloudScripts[k] > listLocalScripts[k]:
                cloud.Yadisk.downloadUpdate(self.disk, f'/RI.Remote.Scripts/{k}', f"scripts/{k}")
                local.Scripts(self.info['local']['scriptBase']).addScript("/info/kap.json", k, self.info['local']['scriptBase'])
            elif v > listLocalScripts[k]:
                Core.fromFileWork.downloadUpdate(k)
class Core:
    def __init__(self,filesFolder):
        self.info = LoadDatas(filesFolder)
        self.data = FileWork(self.info['forCloud'], self.info['forLocal'])
        self.allProcesses = local.Process(self.info['forLocal']['scriptBase'])
        self.allProcesses.startAllProcess()
        self.lock = threading.Lock()
        threads = [threading.Thread(target=i) for i in [self.threadBot, self.threadProcess, self.automative]]
    def threadProcess(self):
        with self.lock:
            while True:
                for k,v in self.allProcesses.items():
                    out = local.Process.checkProcess(v)

                    if out: 
                        if "__send:" in out: local.Process.sendRequestInProcess(self.bot, f"{k}: {out}")
    def threadBot(self): 
        with self.lock:    
            self.bot = local.Process.startProcess("bot.py")
            process.sendRequestInProcess(self.bot, [v for k,v in self.info['forLocal']])

            while True:
                out = local.process.sendRequestInProcess(bot)
                if out: 
                    for i in out:
                        if "__log" in out: pass
                        elif "_" in out and out.count("_") == 1:
                            _ = out.find("_")
                            process = out[0: _-1]
                            command = out[_+1: -1]
                            local.Process.sendRequestInProcess(self.allProcesses[process], command )

    def automative(self):
        with self.lock:
            infoForBot   = self.info['forBot']
            infoForLocal = self.info['forLocal']
            infoForCloud = self.info['forCloud']
            coreParr = infoForLocal["MainCore"]
            while True:
                if coreParr['update_Modules']:
                    fromFileWork.update(type='modules')
                if coreParr['update_core']:
                    fromFileWork.update(type='core')
                if coreParr['update_scripts']:
                    fromFileWork.getscripts()
                time.sleep(coreParr['check'])