import pymysql


#Класс для взаимодействия с базой данных MySQL
class MySQL_DB:

    #инициализация/подключение
    def __init__(self, host, username, password, name_DB):
        try:
            self.__connection = pymysql.connect(host, username, password, name_DB)
            self.__cursor = self.__connection.cursor()
        except pymysql.OperationalError as opErr:
            print(opErr)
        except RuntimeError as rErr:
            print(rErr)

    def close(self):
        self.__connection.close()

    #запрос на изменение/добавление/удаление
    def query_execute(self, textQuery):
        try:
            self.__cursor.execute(textQuery)
            self.__connection.commit()
            return True
        except pymysql.ProgrammingError as progErr:     # ошибки в названии таблиц итд
            print(progErr)
            self.__connection.rollback()
            return False
        except pymysql.IntegrityError as intErr:        # нарушение целостности отношений
            print(intErr)
            self.__connection.rollback()
            return False
        except pymysql.DataError as dErr:               # ошибки в данных
            print(dErr)
            self.__connection.rollback()
            return False
        except pymysql.OperationalError as opErr:       # ошибка потеря соединения
            print(opErr)
            self.__connection.rollback()
            return False

    #запрос на выборку
    def query_select(self, textSelect):
        try:
            self.__cursor.execute(textSelect)
            resultSelect = self.__cursor.fetchall()
            return resultSelect
        except pymysql.ProgrammingError as progErr:
            print(progErr)
            return None
        except pymysql.IntegrityError as intErr:
            print(intErr)
            return None
        except pymysql.DataError as dErr:
            print(dErr)
            return None
        except pymysql.OperationalError as opErr:
            print(opErr)
            return None

    #функция-генератор для построчного чтения строк таблицы
    def query_select_countStr(self, textSelect, count):
        try:
            self.__cursor.execute(textSelect)
            for i in range(0, count):
                yield self.__cursor.fetchone()
        except pymysql.ProgrammingError as progErr:
            print(progErr)
            return None
        except pymysql.IntegrityError as intErr:
            print(intErr)
            return None
        except pymysql.DataError as dErr:
            print(dErr)
            return None
        except pymysql.OperationalError as opErr:
            print(opErr)
            return None

