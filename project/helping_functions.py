import bcrypt
from print_info import *
from main import connection, cursor
from fun_for_login import register_user, authenticate_user, authenticate_admin

user_login = None


def program():

    if login_fun() == 'end':
        cursor.close()
        connection.close()
        return

    while True:
        print_menu()
        answer = input("Введите цифру из меню: ")
        match answer:
            case '1':
                print("Программа завершена")
                print(user_login)
                cursor.close()
                connection.close()
                break
            case _:
                print('Неверный ввод. Повторите попытку!')


def login_fun():
    while True:
        global user_login
        print_login()
        answer = input("Введите цифру из меню: ")
        match answer:
            case '1':
                print("Авторизация:")
                user_login = authenticate_user()
                if user_login:
                    break
            case '2':
                print("Регистрация:")
                register_user()
                break
            case '3':
                print("Вход в админку:")
                if authenticate_admin():

                    break
            case '4':
                print("Программа завершена")
                return "end"
            case _:
                print('Неверный ввод. Повторите попытку!')


