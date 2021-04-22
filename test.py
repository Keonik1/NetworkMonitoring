import modules.dominate
from modules.dominate.tags import *
import json
import constants

def CheckFile(filename):
    try:
        with open(str(filename), 'r', encoding='utf-8') as f:
            f.read()
    except Exception:
        File = open(str(filename), 'w', encoding='utf-8')

def WriteInHTML(text):
    with open('index.html', 'r+', encoding='utf-8') as File:
        File.write(str(text))


TextForHTML = None
PathDevicesData = constants.devicesJson
with open(PathDevicesData, 'r+', encoding=constants.Encoding) as File:
    DevicesData = json.loads(File.read()) 


CheckFile('index.html')
WriteInHTML(TextForHTML)



