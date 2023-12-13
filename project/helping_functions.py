from print_info import *
from main import connection, cursor
from fun_for_login import register_user, authenticate_user, authenticate_admin
from admin_panel import admin_select
from fun_for_admin import view_all_books
from fun_for_client import search_books_by_genre, search_books_by_title, search_books_by_author,\
    make_order, track_order_status, leave_review, view_order_history

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
                print("Просмотр книг")
                view_all_books()
            case '2':
                print("Поиск книг")
                search_books()
            case '3':
                print("Оформление заказа")
                make_order(user_login)
            case '4':
                print("Отслеживание статуса")
                track_order_status(user_login)
            case '5':
                print("Оставление отзыва")
                leave_review(user_login)
            case '6':
                print("История покупок")
                view_order_history(user_login)
            case '7':
                print("Программа завершена")
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
                    admin_select()
                    return "end"
            case '4':
                print("Программа завершена")
                return "end"
            case _:
                print('Неверный ввод. Повторите попытку!')


def search_books():
    while True:
        print_search_menu()
        action = input("Выберите действие: ")
        match action:
            case '1':
                print("Поиск по названию: ")
                search_books_by_title()
            case '2':
                print("Поиск по автору: ")
                search_books_by_author()
            case '3':
                print("Поиск по жанру: ")
                search_books_by_genre()
            case '4':
                break
            case _:
                print('Неверный ввод. Повторите попытку!')

