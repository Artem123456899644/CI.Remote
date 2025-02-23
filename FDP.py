import os
import subprocess
import json5
import time
import importlib
import inspect

class Files:
    @staticmethod
    def loadInfo(filename):
        absPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', filename)
        with open(absPath, 'r', encoding='utf-8') as file:
            return json5.load(file)

    @staticmethod
    def writeInfo(filepath, info):
        with open(filepath, 'w', encoding='utf-8') as file:
            json5.dump(info, file, ensure_ascii=False, indent=4)

    @staticmethod
    def getVersion(filename):
        absPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', filename) 
        fv = importlib.import_module(absPath)
        return fv.version

    @staticmethod
    def checkModules(listModules):
        needToInstall = []
        for i in listModules:
            try:
                importlib.import_module(i)
            except ModuleNotFoundError:
                needToInstall.append(i)
        return needToInstall

    @staticmethod
    def delFile(filepath):
        os.remove(filepath)


class Scripts:
    def __init__(self, baseScripts):
        self.baseScripts = baseScripts

    class addScript:
        def __init__(self, config, filename, baseScripts):
            self.script = filename
            self.pathToScriptBase = config['mainCore']['script_Base']
            self.baseScripts = baseScripts
            self.appendInBase(self.loadInfoINScript())

        def loadInfoINScript(self):
            isModule = importlib.import_module(self.script)
            return {
                "Libs": [name for name, obj in inspect.getmembers(isModule) if inspect.ismodule(obj)],
                "name": isModule.name,
                "commands": isModule.commandsList
            }

        def appendInBase(self, infScript):
            maxAuxilinary = max((int(k) for k in self.baseScripts.items()), default=0)

            self.baseScripts[str(maxAuxilinary + 1)] = {
                "name": infScript['name'],
                "commands": infScript['commands']
            }
            Files.writeInfo(filepath=self.pathToScriptBase, info=self.baseScripts)

    class removeScript:
        def __init__(self, config, scriptName):
            self.config = config
            self.scriptName = scriptName
            self.loadData()
            self.deleteFromBS()

        def loadData(self):
            self.scriptBase = Files.loadInfo(self.config['mainCore']['script_Base'])

        def deleteFromBS(self):
            for k, v in list(self.scriptBase.items()):
                if v['name'] == self.scriptName: 
                    self.scriptBase.pop(k, None)
                    break
            Files.writeInfo(self.config['mainCore']['script_Base'], self.scriptBase)


# class Logs:
#     def __init__(self, filepath):
#         self.filepath = filepath
#         self.logs = Files.loadInfo(filepath)

#     def append(self, event):
#         self.logs.append({f'{time.strftime("%Y-%m-%d %H:%M:%S:", time.localtime())}': f" {event}"})

#     def clear(self):
#         self.logs = []
#         Files.writeInfo(self.filepath, [])

#     def write(self):
#         self.clear()
#         self.writeInfo(self.filepath, self.logs)


class Process:
    def __init__(self, fileList):
        self.listProcees = {k: False for k,v in self.convertForProcessList(fileList)}

    def convertForProcessList(self, filename):
        info = Files.loadInfo(filename)
        return list(info.keys())

    def startProcess(self, processName):
        process = subprocess.Popen(
            ["python3", processName],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return process

    def startAllProcess(self):
        for k, v in self.listProcees.items():
            if not v:
                self.listProcees[k] = subprocess.Popen(
                    ["python3", k],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )

    def closeProcess(self, process):
        process.terminate()
        process.wait()

    def closeAllProcess(self):
        for k, v in self.listProcees.items():
            if v:
                v.terminate()
                v.wait()

    def listenInProcess(self):
        import sys
        if sys.stdin:
            for mess in sys.stdin:
                return mess.strip()

    def sendRequestInProcess(self, process, request):
        process.stdin.write(request)
        process.stdin.flush()
    def listenProcess(self, process):
    
        output = process.stdout.readline()
        return output
    def checkProcess(self, process):
	    if process.poll() is not None: 
	        return None

	    ready, _, _ = select.select([process.stdout], [], [], 0)
	    if ready:
	        return process.stdout.readline().strip()
if __name__ == "__main__":
    pass
