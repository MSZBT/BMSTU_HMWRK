from flask import Flask, render_template, jsonify, request
import sqlite3, jinja2

from datetime import datetime, timedelta
import calendar


def bigprint():
    connection = sqlite3.connect("./database.db")
    cursor = connection.cursor()
    cursor.execute('''SELECT * FROM Couples''')
    rows = cursor.fetchall()
    print(rows)
    connection.close()

def split_array(arr, chunk_size=6):
    return [arr[i:i + chunk_size] for i in range(0, len(arr), chunk_size)]

def initDb():
    connection = sqlite3.connect("./database.db")
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Couples (
        id TEXT,
        date INTEGER,
        pairindex INTEGER,
        pairname TEXT,
        homework TEXT UNIQE,
        cab TEXT,
        pairtype TEXT
    )''')
    #ID - комбинация из даты и пары 
    connection.commit()
    connection.close()

def addValues(i_d, date, index, pairname, homework, cab, typ):
    connection = sqlite3.connect("./database.db")
    cursor = connection.cursor()
    
    cursor.execute('''
        INSERT INTO Couples(id, date, pairindex, pairname, homework, cab, pairtype) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (i_d, date, index, pairname + str(date), homework, cab, typ))

    connection.commit()
    connection.close()

def dataUpdate(idPair, homework):
    connection = sqlite3.connect("./database.db")
    cursor = connection.cursor()

    cursor.execute('''
    UPDATE Couples
    SET
        homework = ?
    WHERE id = ?
    ''', (homework, idPair)) 

    connection.commit()
    connection.close()

def getListForRender(listTransmitDate):
    connection = sqlite3.connect("./database.db")
    cursor = connection.cursor()

    dates = [date for datelist in listTransmitDate for date in datelist]
    listForRender = []

    for day in dates:
        cursor.execute(f'''SELECT * FROM Couples WHERE date = {day}''')
        middleList = cursor.fetchall()
        if (middleList):
            listForRender.append(middleList)
    connection.commit()
    connection.close()

    return listForRender

def getlistTransmitData():
    year = datetime.now().year
    month = datetime.now().month

    #date = datetime.now().day
    date = 21
    dates = calendar.monthcalendar(year, month) + calendar.monthcalendar(year if month != 12 else year + 1, month + 1 if month != 12 else 1)
    
    for datelist in dates:
        if date in datelist:
            dates = dates[dates.index(datelist) : dates.index(datelist) + 4] 
            dates = [date for datelist in dates for date in datelist if date != 0]
            
            break
    dates.pop(20)
    dates.pop(13)
    dates.pop(6)
    dates = split_array(dates, 6)
    return dates, date

def DBrenew():
    flag = 0 #отвечает за изменение числителся / знаменателя
    lastRunDay = 0
    while True:
        #date = datetime.now().day
        date = 21
        dates = getlistTransmitData()[0]
        print(dates)
        if lastRunDay != date and [data for subdates in dates for data in subdates].index(date) in [0, 6, 12]:
            executionList_flag0 = [
                (str(dates[2][0]) + "0", dates[2][0], 0, "Пар нет", "Отдыхай", "дом", "Солнышко"),

                (str(dates[2][1]) + "0", dates[2][1], 0, "Химия", "Нет | еще не занесено", "327.1", "Лекция"),
                (str(dates[2][1]) + "1", dates[2][1], 1, "Информатика", "Нет | еще не занесено", "601к", "Семинар"),
                (str(dates[2][1]) + "2", dates[2][1], 2, "ФЛИТА", "Нет | еще не занесено", "601к", "Семинар"),

                (str(dates[2][2]) + "0", dates[2][2], 0, "Информатика", "Нет | еще не занесено", "221х", "Лекция"),
                (str(dates[2][2]) + "1", dates[2][2], 1, "ИниДу", "Нет | еще не занесено", "221х", "Лекция"),
                (str(dates[2][2]) + "2", dates[2][2], 2, "ИниДу", "Нет | еще не занесено", "216х", "Семинар"),

                (str(dates[2][3]) + "0", dates[2][3], 0, "Физика", "Нет | еще не занесено", "ФН4", "Лабы"),
                (str(dates[2][3]) + "1", dates[2][3], 1, "Физика", "Нет | еще не занесено", "323", "Лекция"),
                (str(dates[2][3]) + "2", dates[2][3], 2, "Химия", "Нет | еще не занесено", "241", "Лабы"),
                (str(dates[2][3]) + "3", dates[2][3], 3, "Бассейн", "Нет | еще не занесено", "СК", "Семинар"),

                (str(dates[2][4]) + "0", dates[2][4], 0, "Бассейн", "Нет | еще не занесено", "СК", "Семинар"),
                (str(dates[2][4]) + "1", dates[2][4], 1, "История", "Нет | еще не занесено", "520к", "Семинар"),
                (str(dates[2][4]) + "2", dates[2][4], 2, "ИниДу", "Нет | еще не занесено", "520к", "Семинар"),

                (str(dates[2][5]) + "0", dates[2][5], 0, "Ин. язык", "Нет | еще не занесено", "523к/514к", "Семинар"),
                (str(dates[2][5]) + "1", dates[2][5], 1, "Линал", "Нет | еще не занесено", "527к", "Семинар"),
                (str(dates[2][5]) + "2", dates[2][5], 2, "Линал", "Нет | еще не занесено", "535к", "Лекция"),
            ]

            executionList_flag1 = [
                (str(dates[2][0]) + "0", dates[2][0], 0, "Пар нет", "Отдыхай", "дом", "Солнышко"),

                (str(dates[2][1]) + "0", dates[2][1], 0, "Химия", "Нет | еще не занесено", "327.1", "Лекция"),
                (str(dates[2][1]) + "1", dates[2][1], 1, "Информатика", "Нет | еще не занесено", "601к", "Семинар"),
                (str(dates[2][1]) + "2", dates[2][1], 2, "ФЛИТА", "Нет | еще не занесено", "601к", "Семинар"),

                (str(dates[2][2]) + "0", dates[2][2], 0, "Информатика", "Нет | еще не занесено", "221х", "Лекция"),
                (str(dates[2][2]) + "1", dates[2][2], 1, "ИниДу", "Нет | еще не занесено", "221х", "Лекция"),
                (str(dates[2][2]) + "2", dates[2][2], 2, "ФЛИТА", "Нет | еще не занесено", "221х", "Лекция"),
                (str(dates[2][2]) + "2", dates[2][2], 3, "История", "Нет | еще не занесено", "221х", "Лекция"),

                (str(dates[2][3]) + "0", dates[2][3], 0, "Физика", "Нет | еще не занесено", "304", "Семинар"),
                (str(dates[2][3]) + "1", dates[2][3], 1, "Физика", "Нет | еще не занесено", "323", "Лекция"),
                (str(dates[2][3]) + "2", dates[2][3], 2, "Химия", "Нет | еще не занесено", "241", "Лабы"),
                (str(dates[2][3]) + "3", dates[2][3], 3, "Бассейн", "Нет | еще не занесено", "СК", "Семинар"),

                (str(dates[2][4]) + "0", dates[2][4], 0, "Бассейн", "Нет | еще не занесено", "СК", "Семинар"),
                (str(dates[2][4]) + "1", dates[2][4], 1, "История", "Нет | еще не занесено", "520к", "Семинар"),
                (str(dates[2][4]) + "2", dates[2][4], 2, "ИниДу", "Нет | еще не занесено", "520к", "Семинар"),

                (str(dates[2][5]) + "0", dates[2][5], 0, "Ин. язык", "Нет | еще не занесено", "523к/514к", "Семинар"),
                (str(dates[2][5]) + "1", dates[2][5], 1, "Линал", "Нет | еще не занесено", "527к", "Семинар"),
                (str(dates[2][5]) + "2", dates[2][5], 2, "Линал", "Нет | еще не занесено", "535к", "Лекция"),
            ]

            connection = sqlite3.connect("./database.db")
            cursor = connection.cursor()

            #Удаление ненужных дней для отслеживания
            cursor.execute(f'''
            DELETE FROM Couples WHERE date < {date}
            ''')

            #Добавление новой недели
            cursor.executemany('INSERT INTO Couples(id, date, pairindex, pairname, homework, cab, pairtype) VALUES (?, ?, ?, ?, ?, ?, ?)', executionList_flag0 if flag == 0 else executionList_flag1)
            flag = not(flag)

            lastRunDay = date
            bigprint()
            

            connection.commit()
            connection.close()
            break


import sqlite3




app = Flask(__name__)

initDb()



@app.route('/')
def renderMain():
    return render_template("mainPage.html")

@app.route('/studentPage.html')
def renderStudent():
    
    returnDateList = getlistTransmitData()

    listTransmitDate = returnDateList[0]

    #Указатели начала и канца отслеживаемых данных

    currentday = returnDateList[1]
    listTransmit = getListForRender(listTransmitDate)
    print("\n")
    print(listTransmit)
    print("\n")

    bigprint()
    return render_template("studentPage.html", listTransmit=listTransmit, listTransmitDate=listTransmitDate, dayNameList = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс'], currentday=currentday)

@app.route('/mainPage.html')
def renderMain_fromstudent():
    return render_template("mainPage.html")


@app.route('/api/endpoint', methods=['POST'])
def handle_post():
    transmitdata = request.get_json()

    date = transmitdata["date"]
    pairindex = transmitdata["pairindex"]
    homework = transmitdata["homework"]
    
    idPair = date + str(int(pairindex) - 1)
    dataUpdate(idPair, homework)    

"""
dates = [[21, 22, 23, 24, 25, 26], [28, 29, 30, 1, 2, 3], [5, 6, 7, 8, 9, 10]]
executionList_flag0 = [
    (str(dates[1][0]) + "0", dates[1][0], 0, "Пар нет", "Отдыхай", "дом", "Солнышко"),
    (str(dates[1][1]) + "0", dates[1][1], 0, "Химия", "Нет | еще не занесено", "327.1", "Лекция"),
    (str(dates[1][1]) + "1", dates[1][1], 1, "Информатика", "Нет | еще не занесено", "601к", "Семинар"),
    (str(dates[1][1]) + "2", dates[1][1], 2, "ФЛИТА", "Нет | еще не занесено", "601к", "Семинар"),
    (str(dates[1][2]) + "0", dates[1][2], 0, "Информатика", "Нет | еще не занесено", "221х", "Лекция"),
    (str(dates[1][2]) + "1", dates[1][2], 1, "ИниДу", "Нет | еще не занесено", "221х", "Лекция"),
    (str(dates[1][2]) + "2", dates[1][2], 2, "ИниДу", "Нет | еще не занесено", "216х", "Семинар"),
    (str(dates[1][3]) + "0", dates[1][3], 0, "Физика", "Нет | еще не занесено", "ФН4", "Лабы"),
    (str(dates[1][3]) + "1", dates[1][3], 1, "Физика", "Нет | еще не занесено", "323", "Лекция"),
    (str(dates[1][3]) + "2", dates[1][3], 2, "Химия", "Нет | еще не занесено", "241", "Лабы"),
    (str(dates[1][3]) + "3", dates[1][3], 3, "Бассейн", "Нет | еще не занесено", "СК", "Семинар"),
    (str(dates[1][4]) + "0", dates[1][4], 0, "Бассейн", "Нет | еще не занесено", "СК", "Семинар"),
    (str(dates[1][4]) + "1", dates[1][4], 1, "История", "Нет | еще не занесено", "520к", "Семинар"),
    (str(dates[1][4]) + "2", dates[1][4], 2, "ИниДу", "Нет | еще не занесено", "520к", "Семинар"),
    (str(dates[1][5]) + "0", dates[1][5], 0, "Ин. язык", "Нет | еще не занесено", "523к/514к", "Семинар"),
    (str(dates[1][5]) + "1", dates[1][5], 1, "Линал", "Нет | еще не занесено", "527к", "Семинар"),
    (str(dates[1][5]) + "2", dates[1][5], 2, "Линал", "Нет | еще не занесено", "535к", "Лекция"),
]

for ar in executionList_flag0:
#def addValues(i_d, date, index, pairname, homework, cab, typ):
    addValues(ar[0], ar[1], ar[2], ar[3], ar[4], ar[5], ar[6],)
"""

bigprint()

if __name__ == '__main__':
    app.run()