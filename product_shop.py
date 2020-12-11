from mySQL_BD import MySQL_DB
from enum import Enum
from itertools import tee


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

    # меню для выбора таблицы, с которой пользователь будет взаимодействовать
    def selectTableMenu(self):
        print("\n1 - Магазины\n2 - Сотрудники\n3 - Товары\n4 - Заказы\n" +\
              "5 - Поставки\n6 - Выход\nВведите цирфу: ", end = '')

        choice = int(input())
        if choice == 1:
            self.__selectTable = "shop"
            self.__selectActionMenu()
        elif choice == 2:
            self.__selectTable = "employee"
            self.outputEmployee()
        elif choice == 3:
            self.__selectTable = "product"
            self.topOfProduct()
        elif choice == 4:
            self.__selectTable = "orders"
            self.getAverageCheckOnTime()
        elif choice == 5:
            self.__selectTable = "delivery"
            self.deliveryInformation()
        elif choice == 6:
            exit()
        else:
            print("Несуществующий номер!")
            self.__selectTable = ""

    # меню, для выбора действия над выбранной таблицей
    def __selectActionMenu(self):
        print("\n1 - Добавить строку\n2 - Изменить строку\n3 - Удалить строку\n" +\
              "4 - Получить все строки\nВведите цифру: ", end = '')

        choice = int(input())
        if choice == 1:
            self.__choiceAction = Actions_With_Table.INSERT
        elif choice == 2:
            self.__choiceAction = Actions_With_Table.UPDATE
        elif choice == 3:
            self.__choiceAction = Actions_With_Table.DELETE
        elif choice == 4:
            self.__choiceAction = Actions_With_Table.SELECT
        else:
            print("Несуществующий номер!")
            self.__choiceAction = Actions_With_Table.NONE
        self.__execActionsWithTable()

    # ф-ция для вызова соотв. метода в зависимости от выбранной таблицы
    def __execActionsWithTable(self):
        if self.__selectTable == "shop":
            self.__shopTable()

    # ф-ция для генерирования запросов для таблицы Shop
    def __shopTable(self):
        if self.__choiceAction == Actions_With_Table.INSERT:
            print("\nВведите данные нового магазина: ")
            address = input("Адрес магазина: ")
            phone_number = input("Телефон (в формате +7/8-(ХХХ)-ХХХ-ХХ-ХХ): ")
            db_query = "INSERT shop(phone_number, address) VALUE (\"" + phone_number + "\", \"" + address + "\");"
            if self.__db.query_execute(db_query):
                print("Магазин успешно добавлен!")
            self.selectTableMenu()

        elif self.__choiceAction == Actions_With_Table.UPDATE:
            print("\nВыберите ID магазина, данные которого хотите изменить")
            shops = self.__db.query_select("SELECT * FROM shop")
            print("ID) Адрес")
            for shop in shops:
                print( str(shop[0]) + ") " + str(shop[2]) )
            id_shop = int(input("Введите ID: "))
            print("\nКакие данные хотите изменить?\n1 - Адрес\n" +\
                  "2 - Номер телефона\nВведите цифру: ", end = '')
            choice = int(input())

            db_query = ""
            if choice == 1:
                print("Введите новый адрес: ", end='')
                address = input()
                db_query = "UPDATE shop SET address = \"" +\
                           address + "\" WHERE id = " + str(id_shop)
            elif choice == 2:
                print("Введите новый телефон в формате +7/8-(ХХХ)-ХХХ-ХХ-ХХ: ", end='')
                phone_number = input()
                db_query = "UPDATE shop SET phone_number = \"" +\
                           phone_number + "\" WHERE id = " + str(id_shop)

            if self.__db.query_execute(db_query):
                print("Данные о магазине успешно обновлены!")
            self.selectTableMenu()
        
        elif self.__choiceAction == Actions_With_Table.DELETE:
            print("\nВыберите ID магазина, который хотите удалить")
            shops = self.__db.query_select("SELECT * FROM shop")
            print("ID) Адрес")
            for shop in shops:
                print( str(shop[0]) + ") " + str(shop[2]) )
            id_shop = int(input("Введите ID: "))
            db_query = "DELETE FROM shop WHERE id = " + str(id_shop)
            if self.__db.query_execute(db_query):
                print("Магазин удален из базы данных!")
            self.selectTableMenu()

        elif self.__choiceAction == Actions_With_Table.SELECT:
            db_query = "SELECT * FROM shop"
            shops = self.__db.query_select(db_query)
            for shop in shops:
                print(shop)
            self.selectTableMenu()
    
    #функция для вывода сотрудников конкретного магазина
    def outputEmployee(self):
        print("\nВыберите ID магазина, сотрудников которого хотите посмотреть")
        shops = self.__db.query_select("SELECT * FROM shop")
        print("ID) Адрес")
        for shop in shops:
            print( str(shop[0]) + ") " + str(shop[2]) )
        id_shop = int(input("Введите ID: "))
        db_query = "SELECT E.full_name, E.phone, E.position, E.salary, S.address " +\
	               "FROM Employee AS E JOIN Shop AS S ON S.id = E.id_shop " +\
                   "WHERE S.id = " + str(id_shop)
        print("\nСотрудники магазина №" + str(id_shop) + ": ")
        employees = self.__db.query_select(db_query)
        for employee in employees:
            print(employee)
        self.selectTableMenu()

    #вывод информации о популярности товаров
    def topOfProduct(self):
        print("\nРейтинг популярности товаров, на основании сделанных заказов:")
        db_query = "SELECT P.name, SUM(Link.qty) AS qty " +\
                   "FROM Link_product_order AS Link " +\
                   "JOIN Orders AS O ON O.id = Link.id_order " +\
                   "JOIN Product AS P ON P.id = Link.id_product " +\
                   "GROUP BY P.name ORDER BY qty DESC"
        topProduct = self.__db.query_select(db_query)
        print("\nНаименование товара\\Кол-во проданных штук")
        for product in topProduct:
            print(str(product[0]) + ' ' + str(product[1]))
        self.selectTableMenu()

    #функция вывода информации по доставке в конкретный магазин
    def deliveryInformation(self):
        print("\nВыберите ID магазина, сотрудников которого хотите посмотреть")
        shops = self.__db.query_select("SELECT * FROM shop")
        print("ID) Адрес")
        for shop in shops:
            print( str(shop[0]) + ") " + str(shop[2]) )
        id_shop = int(input("Введите ID: "))
        db_query = "SELECT P.name, (SUM(DISTINCT Link_D.qty)) AS qty " +\
                   "FROM Link_product_delivery AS Link_D " +\
                   "JOIN Product AS P ON P.id = Link_D.id_product " +\
                   "JOIN Delivery AS D ON D.id = Link_D.id_delivery " +\
                   "WHERE D.id_shop = " + str(id_shop) + ' ' +\
                   "GROUP BY P.name ORDER BY qty"
        print("\nИнформация о кол-ве продуктов, доставленных в магазин №" + str(id_shop) + ": ")
        deliveries = self.__db.query_select(db_query)
        for delivery in deliveries:
            print(str(delivery[0]) + ' ' + str(int(delivery[1])))
        self.selectTableMenu()

    #функция нахождения среднего чека по магазина в опр. промежуток времени
    def getAverageCheckOnTime(self):
        print("\nНахождение стоимости среднего чека по магазинам в определенное время")
        timeRange = input("Введите диапазон времени в часах в виде 'нач.час - кон.час': ")
        timeRange = timeRange.split('-')
        db_query = "SELECT S.id AS id_shop, S.address, SUM(Link.qty * P.price) / COUNT(*) AS AVG_SUM " +\
                   "FROM Link_product_order AS Link " +\
                   "JOIN Orders AS O ON O.id = Link.id_order " +\
                   "JOIN Product AS P ON P.id = Link.id_product " +\
                   "JOIN Shop AS S ON S.id = O.id_shop " +\
                   "WHERE EXTRACT(HOUR FROM O.date_and_time) BETWEEN " + timeRange[0] + " AND " + timeRange[1] + " " +\
                   "GROUP BY S.id ORDER BY AVG_SUM DESC"
        results = self.__db.query_select(db_query)
        for result in results:
            print(str(result[:2]) + ' ' + str(int(result[2])))
        self.selectTableMenu()
    
    #функция для вывода n строк указанной таблицы
    def readNLines(self):
        print("\n1 - Магазины\n2 - Сотрудники\n3 - Товары\n4 - Заказы\n" +\
              "5 - Поставки\n6 - Выход\nВведите цирфу: ", end = '')

        choice = int(input())
        if choice == 1:
            self.__selectTable = "shop"
        elif choice == 2:
            self.__selectTable = "employee"
        elif choice == 3:
            self.__selectTable = "product"
        elif choice == 4:
            self.__selectTable = "orders"
        elif choice == 5:
            self.__selectTable = "delivery"
        elif choice == 6:
            exit()
        else:
            print("Несуществующий номер!")
            self.__selectTable = ""

        db_query = "SELECT * FROM " + self.__selectTable
        howStrAlreadyReads = 0
        results = self.__db.query_select_countStr(db_query)
        newResults = tee(results)
        lenResults = len(list(newResults))
        while howStrAlreadyReads <= lenResults:
            count = int(input("Сколько строк ещё хотите вывести: "))
            for i in range(0, count):
                print(next(results))
            howStrAlreadyReads += count

