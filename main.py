from mySQL_BD import MySQL_DB


host = input("Введите host: ")
username = input("Введите имя пользователя: ")
password = input("Введите пароль: ")
name_DB = input("Введите имя БД: ")

dateBase = MySQL_DB(host, username, password, name_DB)
counts = dateBase.query_select("SELECT * FROM shop")
for string in counts:
    print(string)