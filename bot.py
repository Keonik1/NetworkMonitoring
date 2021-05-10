from modules.pythonping import ping
import modules.discord
from modules.discord.ext import commands
import botinfo
import json
import time
import sys
import constants
import os
from modules.async_timeout import asyncio

#Определяет, с какой знака бот будет реагировать на команды
client = modules.discord.ext.commands.Bot(command_prefix = "!")

#Вывод сообщения о запуске бота
@client.event
async def on_ready():
    print('Бот залогинился под пользователем: {0.user}'.format(client))

#Создание фоновой задачи мониторинга
async def backgroundMonitoring():
    print('Фоновая задача включена')
    await client.wait_until_ready()         #дождаться включения бота
    channel = client.get_channel(botinfo.channelID)
    LastCheckChannel = client.get_channel(botinfo.LastCheckChannelID)
    await channel.send('Бот запущен, для вызова справки написать "!помощь"')
    #print('Фоновая задача 2 включена')                 #для дебага
    while not client.is_closed():
        PathToJson = constants.devicesJson
        AnswerState = ''
        CountAnswers = 0

        #print('Фоновая задача 3 включена')                 #для дебага
        with open(PathToJson, 'r', encoding=constants.Encoding) as FileJSON:
            JSONData = json.loads(FileJSON.read())

            #print('Фоновая задача 4 включена')                 #для дебага
            lastCheckTime = JSONData["index"][str(0)]["currently time"]
            for i in range(0, (len(JSONData["index"]))):
                if JSONData["index"][str(i)]["past state"] != JSONData["index"][str(i)]["currently state"]:
                    #print('Фоновая задача 5 включена')
                    AnswerState += f'''**Состояние устройства {i+1}:** 
IP-адрес: {JSONData["index"][str(i)]["IPadd"]}
Hostname: {JSONData["index"][str(i)]["hostname"]}
Прошлое состояние: __{JSONData["index"][str(i)]["past state"]}__
Текущее состояние: __{JSONData["index"][str(i)]["currently state"]}__
Время последнего опроса: {JSONData["index"][str(i)]["currently time"]}
             
             
'''
                #print('Фоновая задача 6 включена')                 #для дебага
                if len(AnswerState) > 1500:                         #у дискорда ограничение на 2000 символов в одном сообщении
                    #print('Фоновая задача 7 включена')                 #для дебага
                    await channel.send(AnswerState)
                    AnswerState = ''
                    CountAnswers += 1
        #print(len(AnswerState))                                    #для дебага
        if len(AnswerState) > 0:
            await channel.send(AnswerState)
        else:
            if (CountAnswers == 0 and botinfo.SendLastCheck.lower() == 'on'):
                await LastCheckChannel.send(f'Нет устройств изменивших состояние. Последнее время проверки: {lastCheckTime}')

        await asyncio.sleep(botinfo.timeToGetStatus)

#Справка по командам
@client.command()
async def помощь(ctx):
    answer = '''**Помощь по командам бота**
!status __тип__ __значение__ - Просмотр состояния заданного устройства, где:
                    - В поле __тип__ указывается тип запроса - "ip" или "host" по IP-адресу и имени хоста соответственно;
                    - В поле __значение__ указывается IP-адрес или имя хоста, в зависимости от выбранного типа запроса;
!all - Просмотр сведений обо всех устройствах;
!dif - Просмотр сведений только тех устройств, которые изменили свое состояние;
P.s.
Кавычки указывать не нужно.
Пример запроса: **__!status ip 127.0.0.1__** или **__!status host test.test.ru__**
    '''
    await ctx.send(answer)

#Отображение статуса отдельного устройства
@client.command()
async def status(ctx, responce, value):  #response - ip или hostname (host); value - уже значение (адрес или имя)
    answerStatus = getstatus(responce.lower(), value)
    try:
        await ctx.send(answerStatus)
    except Exception():
        await ctx.send('Что-то пошло не так 🤔. Возможно указаны некорректные данные или искомого устройства не существует.')

#Отобразить информацию устройств, у которых различаются прошлое и текущее состояния
@client.command()
async def dif(ctx):
    PathToJson = constants.devicesJson
    answerStatus = ''
    with open(PathToJson, 'r', encoding=constants.Encoding) as FileJSON:
        JSONData = json.loads(FileJSON.read())
        lastCheckTime = JSONData["index"][str(0)]["currently time"]
        for i in range(0, (len(JSONData["index"]))):
            if JSONData["index"][str(i)]["past state"] != JSONData["index"][str(i)]["currently state"]:
                answerStatus += f'''**Состояние устройства {i+1}:** 
IP-адрес: {JSONData["index"][str(i)]["IPadd"]}
Hostname: {JSONData["index"][str(i)]["hostname"]}
Прошлое состояние: __{JSONData["index"][str(i)]["past state"]}__
Текущее состояние: __{JSONData["index"][str(i)]["currently state"]}__
Время последнего опроса: {JSONData["index"][str(i)]["currently time"]}
             
             
'''
            if len(answerStatus) > 1500:                #у дискорда ограничение на 2000 символов в одном сообщении
                #print(len(answerStatus))
                await ctx.send(answerStatus)
                answerStatus = ''
    #print(len(answerStatus))
    if len(answerStatus) > 0:
        await ctx.send(answerStatus)
    else:
        await ctx.send(f'Нет устройств изменивших состояние. Последнее время проверки: {lastCheckTime}')

#Отобразить информацию обо всех устройствах
@client.command()
async def all(ctx):
    PathToJson = constants.devicesJson
    answerStatus = ''
    with open(PathToJson, 'r', encoding=constants.Encoding) as FileJSON:
        JSONData = json.loads(FileJSON.read())
        for i in range(0, (len(JSONData["index"]))):
            answerStatus += f'''**Состояние устройства {i+1}:** 
{JSONData["index"][str(i)]["IPadd"]}
{JSONData["index"][str(i)]["hostname"]}
Прошлое состояние: __{JSONData["index"][str(i)]["past state"]}__
Текущее состояние: __{JSONData["index"][str(i)]["currently state"]}__
Время последнего опроса: {JSONData["index"][str(i)]["currently time"]}
             
             
'''
            if len(answerStatus) > 1500:
                #print(len(answerStatus))
                await ctx.send(answerStatus)
                answerStatus = ''
            
    #print(len(answerStatus))
    if len(answerStatus) > 0:
        await ctx.send(answerStatus)

#функция запроса статуса. Используется в команде !status
def getstatus(TypeOfResponse, value):
    answer = None
    PathToJson = constants.devicesJson

    if TypeOfResponse == 'ip':
        with open(PathToJson, 'r', encoding=constants.Encoding) as FileJSON:
            JSONData = json.loads(FileJSON.read())
            indexDev = None
            for i in range(0, (len(JSONData["index"]))):
                if JSONData["index"][str(i)]["IPadd"] == str(value):
                    indexDev = i
                    break
            
            if indexDev == None:
                answer = 'Устройство не найдено или введены некорректные значения!'
            else:
            # ** - Жирный текст в дискорде
            # __ - подчеркнутый текст в дискорде 
                answer = f'''**Запрошенное устройство имеет следующее состояние:** 
{JSONData["index"][str(indexDev)]["IPadd"]}
{JSONData["index"][str(indexDev)]["hostname"]}
Прошлое состояние: __{JSONData["index"][str(indexDev)]["past state"]}__
Текущее состояние: __{JSONData["index"][str(indexDev)]["currently state"]}__
Время последнего опроса: {JSONData["index"][str(indexDev)]["currently time"]}
'''

    elif TypeOfResponse == 'host':
        with open(PathToJson, 'r', encoding=constants.Encoding) as FileJSON:
            JSONData = json.loads(FileJSON.read())
            indexDev = None
            for i in range(0, (len(JSONData["index"]))):
                if JSONData["index"][str(i)]["hostname"] == str(value):
                    indexDev = i
                    break

            if indexDev == None:
                answer = 'Устройство не найдено или введены некорректные значения!'
            else: 
            # ** - Жирный текст в дискорде
            # __ - подчеркнутый текст в дискорде
                answer = f'''**Запрошенное устройство имеет следующее состояние:** 
{JSONData["index"][str(indexDev)]["IPadd"]}
{JSONData["index"][str(indexDev)]["hostname"]}
Прошлое состояние: __{JSONData["index"][str(indexDev)]["past state"]}__
Текущее состояние: __{JSONData["index"][str(indexDev)]["currently state"]}__
Время последнего опроса: {JSONData["index"][str(indexDev)]["currently time"]}
'''

    else:
        answer = 'Устройство не найдено или введены некорректные значения!'
    return answer

#-------------------------------------------MAIN-----------------------------------------------
PathToJson = constants.devicesJson
#проверка на существование json'а
if os.path.exists(PathToJson) == True:
    with open(PathToJson, 'r', encoding=constants.Encoding) as File:
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
client.loop.create_task(backgroundMonitoring())     #запуск фоновой задачи
client.run(botinfo.BotToken)                        #запуск бота