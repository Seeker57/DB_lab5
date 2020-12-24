from mySQL_BD import MySQL_DB
from product_shop import Product_shop
import tkinter as tk
from functools import partial


def connectWithDB(host, username, password, name_DB):
    host = entryHost.get()
    username = entryUsername.get()
    password = entryPass.get()
    name_DB = entryNameDB.get()
    windowAuth.destroy()

    dateBase = MySQL_DB('localhost', 'root', 'fsn703zu', 'product_shop')
    myProductShop = Product_shop(dateBase)
    myProductShop.selectTableMenu()
    dateBase.close()


if __name__ == "__main__":

    host = ''
    username = ''
    password = ''
    name_DB = ''

    windowAuth  = tk.Tk()
    windowAuth.title("Подключение к БД")
    windowAuth.minsize(400, 300)
    windowAuth.rowconfigure([0, 1, 2, 3, 4], minsize=50, weight=1)
    windowAuth.columnconfigure(0, weight=1)
    entryHost = tk.Entry(master=windowAuth, width=30)
    entryUsername = tk.Entry(master=windowAuth, width=30)
    entryPass = tk.Entry(master=windowAuth, width=30, show="*")
    entryNameDB = tk.Entry(master=windowAuth, width=30)
    lblHost = tk.Label(text='Host: ')
    lblUsername = tk.Label(text='Имя пользователя: ')
    lblPass = tk.Label(text='Пароль: ')
    lblNameDB = tk.Label(text='Имя БД: ')
    button1 = tk.Button(master=windowAuth, text='Подключиться', 
                        command=partial(connectWithDB, host, username, password, name_DB), 
                        width=30)

    lblHost.grid(row=0, column=0, sticky='w')
    entryHost.grid(row=0, column=1)
    lblUsername.grid(row=1, column=0, sticky='w')
    entryUsername.grid(row=1, column=1)
    lblPass.grid(row=2, column=0, sticky='w')
    entryPass.grid(row=2, column=1)
    lblNameDB.grid(row=3, column=0, sticky='w')
    entryNameDB.grid(row=3, column=1)
    button1.grid(row=4, column=1)

    windowAuth.mainloop()
