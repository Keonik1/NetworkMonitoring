from modules.pythonping import ping
import constants
import os
import time
#import AddDevices
import datetime
import json
import sys


def Pinging(IPaddF="127.0.0.1"):              #функция пинга
    IPadd = IPaddF
    AnswerBool = None
    PingDeviceBool = None
    
    #ping
    try:
        PingDevice = ping(IPadd, verbose=False, count=1, timeout=2) #пинг ip; не выводить на экран; количество пингов; сколько ждать ответа.
    except Exception:
        AnswerBool = False
    #проверка, что пинг удался или выдал ошибку
    if AnswerBool == None:
        PingDeviceBool = PingDevice.success()                       #пингануло? true - онлайн, false - не пингануло
    else:
        PingDeviceBool = False
    
    #возвращение ответа
    if PingDeviceBool == True:
        answer = 'Online'
    else:
        answer = 'Offline'
    return answer

#todo: сделать проверку наличия json, если его нет запросить данные на ввод
#todo: ✓сделать try except✓, ДОДЕЛАТЬ!!!! чтобы можно даже было пинговать через hostname или избавиться от багов
#todo: сделать в json еще 1 параметр, чтобы можно было проверять и по hostname и ip и оба (ip - 0, hostname - 1, оба - 2)
#todo: добавить время пинга, и менять прошлое время, если изменилось состояние. Добавить в json 2 пункта, текущее и прошлое время


while True:
    PathDevicesData = constants.devicesJson
    #проверка наличия данных в json или существование json
    if os.path.exists(PathDevicesData) == True:
        with open(PathDevicesData, 'r+', encoding=constants.Encoding) as File:
            try:
                getjson = json.loads(File.read())
                if len(getjson) == 0:
                    print('Нет данных в json, заполните их через AddDevices.py или вручную в файле ' + PathDevicesData)
                    sys.exit()
            except Exception:
                print('Нет данных в json или не удалось считать эти данные, заполните их через AddDevices.py или вручную в файле ' + PathDevicesData)
                sys.exit()
    else:
        print('Нет данных в json, заполните их через AddDevices.py или вручную в файле ' + PathDevicesData)
        sys.exit()

    with open(PathDevicesData, 'r+', encoding=constants.Encoding) as File:      #открытие файла json с кодировкой utf
        DevicesData = json.loads(File.read())                                   #перенос данных из json в словарь; len(DevicesData["index"]) - определение количества данных (устройств)
        for i in (range(0, (len(DevicesData["index"])))):
            hostname = DevicesData["index"][str(i)]["hostname"]
            IPadd = DevicesData["index"][str(i)]["IPadd"]

            answerPing = Pinging(IPadd)

            pastState = DevicesData["index"][str(i)]["currently state"]     #запись состояния, что сейчас для переноса его в прошлое
            DevicesData["index"][str(i)]["currently state"] = answerPing    #изменение текущего состояния
            DevicesData["index"][str(i)]["past state"] = pastState          #изменение прошлого состояния
            nowTime = datetime.datetime.now()
            DevicesData["index"][str(i)]["currently time"] = nowTime.strftime("%H:%M:%S  %d.%m.%Y")

            checkStateCur = DevicesData["index"][str(i)]["currently state"]
            checkStatePast = DevicesData["index"][str(i)]["past state"]

            if constants.displayView == 'on':                               #отображения пинга на консоли
                print('Устройство ' + hostname + ' по адресу ' + IPadd + ' было ' + checkStatePast + ', а сейчас - ' + checkStateCur)
                
                if checkStateCur !=checkStatePast:
                    print(hostname + ' по адресу ' + IPadd + ' изменило свое состояние на ' + checkStateCur)
        
        File.seek(0)                                                        #очистка файла json
        File.write(json.dumps(DevicesData, indent=constants.indent))        #запись файла json
        File.truncate()

    time.sleep(constants.timeToPing)                                        #Подождать время и повторить проверку по новой