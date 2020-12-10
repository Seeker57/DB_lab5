from mySQL_BD import MySQL_DB
from enum import Enum


#Перечисление для хранения типа операции с таблицами БД
class Actions_With_Table(Enum):
    INSERT = 1
    UPDATE = 2
    DELETE = 3
    NONE = 4


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
        self.__selectActionMenu()

    # меню, для выбора действия над выбранной таблицей
    def __selectActionMenu(self):
        print("\n1 - Добавить строку\n2 - Изменить строку\n3 - Удалить строку\n" +\
               "Введите цифру: ", end = '')

        choice = int(input())
        if choice == 1:
            self.__choiceAction = Actions_With_Table.INSERT
        elif choice == 2:
            self.__choiceAction = Actions_With_Table.UPDATE
        elif choice == 3:
            self.__choiceAction = Actions_With_Table.DELETE
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