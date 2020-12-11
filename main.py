from mySQL_BD import MySQL_DB
from product_shop import Product_shop


if __name__ == "__main__":
    host = input("Введите host: ")
    username = input("Введите имя пользователя: ")
    password = input("Введите пароль: ")
    name_DB = input("Введите имя БД: ")

    dateBase = MySQL_DB(host, username, password, name_DB)
    myProductShop = Product_shop(dateBase)
    #myProductShop.selectTableMenu()
    myProductShop.readNLines()
    dateBase.close()