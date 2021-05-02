# NetworkMonitoring
monitor devices using python and check their status on the site and via the discord bot

eng:
Program for monitoring network devices listed in the JSON file
StartMonitoring - Bash script for running programs.Make it executable and run.
Application.py - Monitoring Program
bot.py - Bot which will be notified to the specified digital channel
constants.py and botinfo.py (botinfo.copy) - Data Files
devices.json - file with devices. Description can be written in human, and not through Unicode
AddDevices.py - Data Entering the JSON file. ! So far not working.!
index.html + styles / styles.css - display information in the browser (you need a web server)
Directory "modules" - for installed modules.
Python 3.9.3 - may work on earlier
If you do not work try the following:
    - Install the necessary modules:
            pip Install pythonping          Currently Version = 1.0.16
            pip Install discord.py          Currently Version = 1.7.1
    - Check the completed data.
    - Check directory. Everything must be in the same directory.

ru:
Программа для мониторинга сетевых устройств ЗАНЕСЕННЫХ в json файл
startMonitoring - bash скрипт для запуска программ. Сделать его исполняемым и запустить.
Application.py - программа мониторинга
bot.py         - бот который будет слать уведомления в указанный дискорд канал
constants.py и botinfo.py (botinfo.copy) - файлы с данными
devices.json   - файл с устройствами. Description можно писать по человечески, а не через unicode
AddDevices.py  - занесение данных в json файл. !Пока что не работает.!
index.html + styles/styles.css - отображение информации в браузере (нужен веб сервер)
директория modules - для установленных модулей.
Python 3.9.3 - может будет работать на более ранних
Если не будет работать попробовать следующее:
    -   установить необходимые модули:
            pip install pythonping      currently version = 1.0.16
            pip install discord.py      currently version = 1.7.1
    -   проверить заполненные данные.
    -   проверить директории. Все должно быть в одной директории.
