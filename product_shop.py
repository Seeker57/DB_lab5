from mySQL_BD import MySQL_DB
from enum import Enum
from itertools import tee
from functools import partial
from tkinter import messagebox
import tkinter as tk


#Перечисление для хранения типа операции с таблицами БД
class Actions_With_Table(Enum):
    INSERT = 1
    UPDATE = 2
    DELETE = 3
    SELECT = 4
    NONE = 5


#Класс для взаимодействия с базой данных продуктовых магазинов
class Product_shop:

    def __init__(self, dateBase):
        self.__db = dateBase                                # объект для взаимодействия с БД
        self.__selectTable = ""                             # имя выбранной для работы таблицы
        self.__choiceAction = Actions_With_Table.NONE       # код операции для выбранной таблицы
        self.__window = None

    def runCommand(self, func):
        self.__window.destroy()
        func()

    # меню для выбора таблицы, с которой пользователь будет взаимодействовать
    def selectTableMenu(self):

        if (self.__window != None):
            self.__window.destroy()

        self.__window = tk.Tk()
        self.__window.title("Меню")
        self.__window.minsize(300, 300)
        self.__window.rowconfigure([0, 1, 2, 3, 4, 5], minsize=50, weight=1)
        self.__window.columnconfigure(0, minsize=50, weight=1)
        button1 = tk.Button(master=self.__window, text='Магазины', 
                command=partial(self.__selectActionMenu, 'shop'), width=30)
        button2 = tk.Button(master=self.__window, text='Сотрудники', 
                command=partial(self.runCommand, self.outputEmployee), width=30)
        button3 = tk.Button(master=self.__window, text='Товары', 
                command=partial(self.runCommand, self.topOfProduct), width=30)
        button4 = tk.Button(master=self.__window, text='Заказы', 
                command=partial(self.runCommand, self.getAverageCheckOnTime), width=30)
        button5 = tk.Button(master=self.__window, text='Поставки', 
                command=partial(self.runCommand, self.deliveryInformation), width=30)
        button6 = tk.Button(master=self.__window, text='Выход', command=exit, width=30)
        button1.grid(row=0, column=0)
        button2.grid(row=1, column=0)
        button3.grid(row=2, column=0)
        button4.grid(row=3, column=0)
        button5.grid(row=4, column=0)
        button6.grid(row=5, column=0)
        self.__window.mainloop()
        

    # меню, для выбора действия над выбранной таблицей
    def __selectActionMenu(self, table):

        self.__window.destroy()
        self.__selectTable = table
        self.__window = tk.Tk()
        self.__window.title("Выбор действия")
        self.__window.minsize(300, 200)
        self.__window.rowconfigure([0, 1, 2, 3], minsize=50, weight=1)
        self.__window.columnconfigure(0, minsize=50, weight=1)
        button1 = tk.Button(master=self.__window, text='Добавить строку', 
                command=partial(self.__execActionsWithTable, Actions_With_Table.INSERT), width=30)
        button2 = tk.Button(master=self.__window, text='Изменить строку', 
                command=partial(self.__execActionsWithTable, Actions_With_Table.UPDATE), width=30)
        button3 = tk.Button(master=self.__window, text='Удалить строку', 
                command=partial(self.__execActionsWithTable, Actions_With_Table.DELETE), width=30)
        button4 = tk.Button(master=self.__window, text='Получить все строки', 
                command=partial(self.__execActionsWithTable, Actions_With_Table.SELECT), width=30)

        button1.grid(row=0, column=0)
        button2.grid(row=1, column=0)
        button3.grid(row=2, column=0)
        button4.grid(row=3, column=0)
        self.__window.mainloop()
 
    # ф-ция для вызова соотв. метода в зависимости от выбранной таблицы
    def __execActionsWithTable(self, action):

        self.__window.destroy()
        self.__choiceAction = action
        if self.__selectTable == "shop":
            self.__shopTable()


    # ф-ция для генерирования запросов для таблицы Shop
    def __shopTable(self):
        if self.__choiceAction == Actions_With_Table.INSERT:

            self.__window = tk.Tk()
            self.__window.title("Добавление данных")
            self.__window.minsize(300, 200)
            self.__window.rowconfigure([0, 1, 2, 3], minsize=50, weight=1)
            self.__window.columnconfigure(0, minsize=50, weight=1)

            lblInfo = tk.Label(text='Введите данные нового магазина:')
            lblAddr = tk.Label(text='Адрес магазина: ')
            lblPhone = tk.Label(text='Телефон: ')
            entryAddr = tk.Entry(master=self.__window, width=30)
            entryPhone = tk.Entry(master=self.__window, width=30)

            def insertShop():
                addr = entryAddr.get()
                phone = entryPhone.get()
                db_query = "INSERT shop(phone_number, address) VALUE (\"" + phone + "\", \"" + addr + "\");"
                if self.__db.query_execute(db_query):
                    messagebox.showinfo("Инфо", "Запись успешно добавлена в БД")
                self.__window.destroy()
                self.__window = None
            button1 = tk.Button(master=self.__window, text='Добавить', width=30, command=insertShop)

            lblInfo.grid(row=0, column=0, sticky='ew')
            lblAddr.grid(row=1, column=0, sticky='w')
            lblPhone.grid(row=2, column=0, sticky='w')
            entryAddr.grid(row=1, column=1)
            entryPhone.grid(row=2, column=1)
            button1.grid(row=3, column=1)

            self.__window.mainloop()
            self.selectTableMenu()

        elif self.__choiceAction == Actions_With_Table.UPDATE:
            shops = self.__db.query_select("SELECT * FROM shop")
            res_query = ''
            for shop in shops:
                res_query += str(shop[0]) + ") " + str(shop[2]) + '\n'

            self.__window = tk.Tk()
            self.__window.title("Редактирование таблицы")
            self.__window.minsize(500, 200)
            self.__window.rowconfigure([0, 1, 2, 3], minsize=50, weight=1)
            self.__window.columnconfigure(0, minsize=50, weight=1)
            lblInfo = tk.Label(text='Выберете ID магазина, данные которого хотите изменить')
            lblRes = tk.Label(text=res_query, justify=tk.LEFT)
            entryShop = tk.Entry(master=self.__window, width=30)

            def changeShop():
                id_shop  = entryShop.get()
                self.__window.destroy()
                self.__window = None

                self.__window = tk.Tk()
                self.__window.title("Редактирование таблицы")
                self.__window.minsize(300, 250)
                self.__window.rowconfigure([0, 1, 2], minsize=50, weight=1)
                self.__window.columnconfigure(0, minsize=50, weight=1)
                lblInfo = tk.Label(text='Какие данные хотите изменить?')

                def queryChagne(col, id_shop):
                    self.__window.destroy()
                    self.__window = None
                    self.__window = tk.Tk()
                    self.__window.title("Редактирование таблицы")
                    self.__window.minsize(300, 200)
                    self.__window.rowconfigure([0, 1], minsize=50, weight=1)
                    self.__window.columnconfigure([0, 1], minsize=50, weight=1)
                    lblInput = None
                    if col == 'address':
                        lblInput = tk.Label(text='Введите новый адрес: ')
                        lblInput.grid(row=0, column=0)
                    elif col == 'phone':
                        lblInput = tk.Label(text='Введите новый телефон: ')
                        lblInput.grid(row=0, column=0)
                    entryInput = tk.Entry(master=self.__window, width=30)
                    entryInput.grid(row=0, column=1)

                    def change(col, id_shop):
                        db_query = ""
                        if col == 'address':
                            db_query = "UPDATE shop SET address = \"" +\
                                    entryInput.get() + "\" WHERE id = " + str(id_shop)
                        elif col == 'phone':
                            db_query = "UPDATE shop SET phone_number = \"" +\
                                    entryInput.get() + "\" WHERE id = " + str(id_shop)

                        if self.__db.query_execute(db_query):
                            messagebox.showinfo("Инфо", "Запись успешно обновлена")
                        self.selectTableMenu()

                    button1 = tk.Button(master=self.__window, text='Обновить', width=30, command=partial(change, col, id_shop))
                    button1.grid(row=1, column=1)
                    self.__window.mainloop()

                button1 = tk.Button(master=self.__window, text='Адрес', width=30, command=partial(queryChagne, 'address', id_shop))
                button2 = tk.Button(master=self.__window, text='Телефон', width=30, command=partial(queryChagne, 'phone', id_shop))
                lblInfo.grid(row=0, column=0)
                button1.grid(row=1, column=0)
                button2.grid(row=2, column=0)
                self.__window.mainloop()
                
            button1 = tk.Button(master=self.__window, text='Выбрать', width=30, command=changeShop)

            lblInfo.grid(row=0, column=0)
            lblRes.grid(row=1, column=0)
            entryShop.grid(row=2, column=0)
            button1.grid(row=3, column=0)
            self.__window.mainloop()
        
        elif self.__choiceAction == Actions_With_Table.DELETE:
            shops = self.__db.query_select("SELECT * FROM shop")
            res_query = ''
            for shop in shops:
                res_query += str(shop[0]) + ") " + str(shop[2]) + '\n'

            self.__window = tk.Tk()
            self.__window.title("Удаление записи")
            self.__window.minsize(500, 250)
            self.__window.rowconfigure([0, 1, 2, 3], minsize=50, weight=1)
            self.__window.columnconfigure(0, minsize=50, weight=1)
            lblInfo = tk.Label(text='Выберете ID магазина, который хотите удалить')
            lblRes = tk.Label(text=res_query, justify=tk.LEFT)
            entryShop = tk.Entry(master=self.__window, width=30)

            def deleteShop():
                id_shop  = entryShop.get()
                db_query = "DELETE FROM shop WHERE id = " + str(id_shop)
                if self.__db.query_execute(db_query):
                    messagebox.showinfo("Инфо", "Запись успешно удалена")
                self.selectTableMenu()
                self.__window.destroy()
                self.__window = None
                self.selectTableMenu()
            button1 = tk.Button(master=self.__window, text='Удалить', width=30, command=deleteShop)

            lblInfo.grid(row=0, column=0)
            lblRes.grid(row=1, column=0)
            entryShop.grid(row=2, column=0)
            button1.grid(row=3, column=0)
            self.__window.mainloop()

        elif self.__choiceAction == Actions_With_Table.SELECT:
            db_query = "SELECT * FROM shop"
            res_query = ''
            shops = self.__db.query_select(db_query)
            for shop in shops:
                res_query += str(shop) + '\n'

            self.__window = tk.Tk()
            self.__window.title("Содержимое таблицы")
            self.__window.minsize(500, 200)
            self.__window.rowconfigure([0, 1], minsize=50, weight=1)
            self.__window.columnconfigure(0, minsize=50, weight=1)
            lblRes = tk.Label(text=res_query, justify=tk.LEFT)
            button1 = tk.Button(master=self.__window, text='К главному меню', width=30, command=self.selectTableMenu)
            lblRes.grid(row=0, column=0)
            button1.grid(row=1, column=0)
            self.__window.mainloop()
    
    #функция для вывода сотрудников конкретного магазина
    def outputEmployee(self):

        shops = self.__db.query_select("SELECT * FROM shop")
        res_query = ''
        for shop in shops:
            res_query += str(shop[0]) + ") " + str(shop[2]) + '\n'

        self.__window = tk.Tk()
        self.__window.title("Сотрудники")
        self.__window.minsize(500, 400)
        self.__window.rowconfigure([0, 1, 2, 3, 4], minsize=50, weight=1)
        self.__window.columnconfigure(0, minsize=50, weight=1)
        lblInfo = tk.Label(text='Выберете ID магазина, сотрудников которого хотите посмотреть')
        lblRes = tk.Label(text=res_query, justify=tk.LEFT)
        entryShop = tk.Entry(master=self.__window, width=30)
        lblEmpl = tk.Label(text='')

        def getEmpl():
            id_shop  = entryShop.get()
            db_query = "SELECT E.full_name, E.phone, E.position, E.salary, S.address " +\
                    "FROM Employee AS E JOIN Shop AS S ON S.id = E.id_shop " +\
                    "WHERE S.id = " + str(id_shop)
            employees = self.__db.query_select(db_query)
            strEmployees = ''
            for employee in employees:
                strEmployees += str(employee) + '\n'
            lblEmpl['text'] = strEmployees
        button1 = tk.Button(master=self.__window, text='Выбрать', width=30, command=getEmpl)
        button2 = tk.Button(master=self.__window, text='В главное меню', width=30, command=self.__window.destroy)

        lblInfo.grid(row=0, column=0)
        lblRes.grid(row=1, column=0)
        entryShop.grid(row=2, column=0)
        lblEmpl.grid(row=3, column=0)
        button1.grid(row=4, column=0)
        button2.grid(row=5, column=0)
        self.__window.mainloop()
        self.__window = None
        self.selectTableMenu()

    #вывод информации о популярности товаров
    def topOfProduct(self):
        db_query = "SELECT P.name, SUM(Link.qty) AS qty " +\
                   "FROM Link_product_order AS Link " +\
                   "JOIN Orders AS O ON O.id = Link.id_order " +\
                   "JOIN Product AS P ON P.id = Link.id_product " +\
                   "GROUP BY P.name ORDER BY qty DESC"
        topProduct = self.__db.query_select(db_query)
        strProduct = ''
        for product in topProduct:
            strProduct += str(product[0]) + ' ' + str(product[1]) + '\n'

        self.__window = tk.Tk()
        self.__window.title("Рейтинг товаров")
        self.__window.minsize(300, 400)
        self.__window.rowconfigure([0, 1, 2], minsize=50, weight=1)
        self.__window.columnconfigure(0, minsize=50, weight=1)
        lblInfo = tk.Label(text='Рейтинг популярности товаров\nНаименование товара\\Кол-во проданных штук')
        lblRes = tk.Label(text=strProduct, justify=tk.LEFT)
        button1 = tk.Button(master=self.__window, text='В главное меню', width=30, command=self.__window.destroy)

        lblInfo.grid(row=0, column=0)
        lblRes.grid(row=1, column=0)
        button1.grid(row=2, column=0)
        self.__window.mainloop()
        self.__window = None
        self.selectTableMenu()

    #функция вывода информации по доставке в конкретный магазин
    def deliveryInformation(self):

        shops = self.__db.query_select("SELECT * FROM shop")
        res_query = ''
        for shop in shops:
            res_query += str(shop[0]) + ") " + str(shop[2]) + '\n'

        self.__window = tk.Tk()
        self.__window.title("Поставки")
        self.__window.minsize(500, 400)
        self.__window.rowconfigure([0, 1, 2, 3, 4], minsize=50, weight=1)
        self.__window.columnconfigure(0, minsize=50, weight=1)
        lblInfo = tk.Label(text='Выберете ID магазина, поставки в который хотите посмотреть')
        lblRes = tk.Label(text=res_query, justify=tk.LEFT)
        entryShop = tk.Entry(master=self.__window, width=30)
        lblDel = tk.Label(text='')

        def getDelivery():
            id_shop  = entryShop.get()
            db_query = "SELECT P.name, (SUM(DISTINCT Link_D.qty)) AS qty " +\
                    "FROM Link_product_delivery AS Link_D " +\
                    "JOIN Product AS P ON P.id = Link_D.id_product " +\
                    "JOIN Delivery AS D ON D.id = Link_D.id_delivery " +\
                    "WHERE D.id_shop = " + str(id_shop) + ' ' +\
                    "GROUP BY P.name ORDER BY qty"
            deliveries = self.__db.query_select(db_query)
            strDeliveries = ''
            for delivery in deliveries:
                strDeliveries += str(delivery[0]) + ' ' + str(int(delivery[1])) + '\n'
            lblDel['text'] = strDeliveries
        button1 = tk.Button(master=self.__window, text='Выбрать', width=30, command=getDelivery)
        button2 = tk.Button(master=self.__window, text='В главное меню', width=30, command=self.__window.destroy)

        lblInfo.grid(row=0, column=0)
        lblRes.grid(row=1, column=0)
        entryShop.grid(row=2, column=0)
        lblDel.grid(row=3, column=0)
        button1.grid(row=4, column=0)
        button2.grid(row=5, column=0)
        self.__window.mainloop()
        self.__window = None
        self.selectTableMenu()

    #функция нахождения среднего чека по магазина в опр. промежуток времени
    def getAverageCheckOnTime(self):

        self.__window = tk.Tk()
        self.__window.title("Заказы")
        self.__window.minsize(550, 200)
        self.__window.rowconfigure([0, 1, 2, 3], minsize=50, weight=1)
        self.__window.columnconfigure(0, minsize=50, weight=1)
        lblInfo = tk.Label(text="Нахождение стоимости среднего чека по магазинам в определенное время\n" + 
                "Введите диапазон времени в часах в виде 'нач.час - кон.час': ")
        entryTime = tk.Entry(master=self.__window, width=30)
        lblOrders = tk.Label(text='')

        def getOrders():
            timeRange  = entryTime.get()
            timeRange = timeRange.split('-')
            db_query = "SELECT S.id AS id_shop, S.address, SUM(Link.qty * P.price) / COUNT(*) AS AVG_SUM " +\
                    "FROM Link_product_order AS Link " +\
                    "JOIN Orders AS O ON O.id = Link.id_order " +\
                    "JOIN Product AS P ON P.id = Link.id_product " +\
                    "JOIN Shop AS S ON S.id = O.id_shop " +\
                    "WHERE EXTRACT(HOUR FROM O.date_and_time) BETWEEN " + timeRange[0] + " AND " + timeRange[1] + " " +\
                    "GROUP BY S.id ORDER BY AVG_SUM DESC"
            orders = self.__db.query_select(db_query)
            strOrders = ''
            for order in orders:
                strOrders += str(order[:2]) + ' ' + str(int(order[2])) + '\n'
            lblOrders['text'] = strOrders
        button1 = tk.Button(master=self.__window, text='Найти', width=30, command=getOrders)
        button2 = tk.Button(master=self.__window, text='В главное меню', width=30, command=self.__window.destroy)

        lblInfo.grid(row=0, column=0)
        entryTime.grid(row=1, column=0)
        lblOrders.grid(row=2, column=0)
        button1.grid(row=3, column=0)
        button2.grid(row=4, column=0)
        self.__window.mainloop()
        self.__window = None
        self.selectTableMenu()
