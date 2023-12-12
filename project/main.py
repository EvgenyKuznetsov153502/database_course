from helping_functions import *
import mysql.connector

# Код подключения БД
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="240303240303",
    database="BookShop"
)
cursor = connection.cursor()

if __name__ == '__main__':
    program()





