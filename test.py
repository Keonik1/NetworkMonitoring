import os
import json
import sys

pathFFF = 'test.json'
if os.path.exists(pathFFF) == True:
    with open(pathFFF, 'r+', encoding="utf-8") as File:
        try:
            getjson = json.loads(File.read())
            if len(getjson) == 0:
                print('Нет данных в json')
                sys.exit()
        except Exception:
            print('Нет данных в json или не удалось считать эти данные')
            sys.exit()
else:
    print('Нет данных в json')
    sys.exit()

print('все ок')




"""
from modules.pythonping import ping
IPadd = "google.com"
hostname = 'test'
AnswerBool = None
PingDeviceBool = None
try:
    PingDevice = ping(IPadd, verbose=False, count=1, timeout=2)
except Exception:
    AnswerBool = False
if AnswerBool == None:
    PingDeviceBool = PingDevice.success() 
else:
    PingDeviceBool = False
if PingDeviceBool == True:
    answer = 'Устройство ' + hostname + ' по адресу ' + IPadd + ' Online'
    print(answer)
else:
    answer = 'Устройство ' + hostname + ' по адресу ' + IPadd + ' Offline'
    print(answer)
"""