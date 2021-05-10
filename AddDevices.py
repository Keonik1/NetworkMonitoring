
import os
import sys
import json
import constants
import datetime
import time

def checkFile(pathToFile):
    if os.path.exists(pathToFile) == True:
        with open(pathToFile, 'r', encoding=constants.Encoding) as File:
            try:
                getjson = json.loads(File.read())
                if len(getjson) == 0:
                    createJSON(pathToFile)
                    print("Данные записаны!")
            except Exception:
                createJSON(pathToFile)
                print("Данные записаны!")
    else:
        createJSON(pathToFile)
        print("Данные записаны!")
    

def createJSON(pathToFile):
    file = open(str(pathToFile), 'w')
    file.close()
    
    jsonFileDict = {"index": {"0":{"hostname": "", "IPadd": "", "Description": "", "past state": "Offline", "currently state": "Offline", "currently time": ""}}}
    with open(pathToFile, 'r+', encoding=constants.Encoding) as File:
        jsonFileDict["index"]["0"]["hostname"] = input('Введите имя устройства (hostname): ')
        jsonFileDict["index"]["0"]["IPadd"] = input('Введите IP-адрес устройства: ')
        jsonFileDict["index"]["0"]["Description"] = input('Введите описание устройства: ')
        nowTime = datetime.datetime.now()
        jsonFileDict["index"]["0"]["currently time"] = nowTime.strftime("%H:%M:%S  %d.%m.%Y")
        File.seek(0)                                                        #очистка файла json
        File.write(json.dumps(jsonFileDict, indent=constants.indent))        #запись файла json
        File.truncate()


#----------------------------MAIN-------------------------------
checkFile(constants.devicesJson)
while True:
    Answer = ""
    Answer = input("Добавить новое устройство? y/n \n")
    if Answer.lower() == ("y" or "yes"):
        with open(constants.devicesJson, 'r+', encoding=constants.Encoding) as File:
            DevicesData = json.loads(File.read())
            i = len(DevicesData["index"])
            insertDict = {"hostname": "", "IPadd": "", "Description": "", "past state": "Offline", "currently state": "Offline", "currently time": ""}
            insertDict["hostname"] = input('Введите имя устройства (hostname): ')
            insertDict["IPadd"] = input('Введите IP-адрес устройства: ')
            insertDict["Description"] = input('Введите описание устройства: ')
            nowTime = datetime.datetime.now()
            insertDict["currently time"] = nowTime.strftime("%H:%M:%S  %d.%m.%Y")
            DevicesData["index"][str(i)] = insertDict
            File.seek(0)                                                        #очистка файла json
            File.write(json.dumps(DevicesData, indent=constants.indent))        #запись файла json
            File.truncate()
    else:
        Exit = input('Вы действительно хотите завершить ввод новых устройств и выйти? \n Введите "no", если хотите продолжить ввод: ')
        if Exit.lower() != ('no' or '"no"'):
            print('Завершение работы программы!')
            time.sleep(1)
            sys.exit()
        else:
            continue