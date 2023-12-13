from print_info import print_main_menu_admin, print_actions, print_actions_rew
from fun_for_admin import view_all_promotions, add_promotion, edit_promotion, delete_promotion,\
    view_all_books, edit_book, add_book, delete_book, view_all_publishers, delete_publisher,\
    edit_publisher, add_publisher, view_all_genres, delete_genre, edit_genre, add_genre,\
    delete_author, edit_author, add_author, view_all_authors, view_all_logs, view_all_reviews, delete_review


def admin_select():
    while True:
        print_main_menu_admin()
        answer = input("Введите цифру из меню: ")
        match answer:
            case '1':
                print("Акции:")
                admin_promotions()

            case '2':
                print("Книги:")
                admin_books()
            case '3':
                print("Издательства:")
                admin_publishers()

            case '4':
                print("Жанры:")
                admin_genres()

            case '5':
                print("Авторы:")
                admin_authors()
            case '6':
                print("Логгирование:")
                view_all_logs()
            case '7':
                print("Отзывы:")
                admin_rew()
            case '8':
                print("Программа завершена")
                break
            case _:
                print('Неверный ввод. Повторите попытку!')


def admin_promotions():
    while True:
        print_actions()
        action = input("Выберите действие: ")
        match action:
            case '1':
                print("Просмотр акций:")
                view_all_promotions()
            case '2':
                print("Создание акций:")
                add_promotion()
            case '3':
                print("Редактирование акций:")
                edit_promotion()
            case '4':
                print("Удаление акции:")
                delete_promotion()
            case '5':
                break
            case _:
                print('Неверный ввод. Повторите попытку!')


def admin_books():
    while True:
        print_actions()
        action = input("Выберите действие: ")
        match action:
            case '1':
                print("Просмотр книг:")
                view_all_books()
            case '2':
                print("Создание книги:")
                add_book()
            case '3':
                print("Редактирование книги:")
                edit_book()
            case '4':
                print("Удаление книги:")
                delete_book()
            case '5':
                break
            case _:
                print('Неверный ввод. Повторите попытку!')


def admin_publishers():
    while True:
        print_actions()
        action = input("Выберите действие: ")
        match action:
            case '1':
                print("Просмотр издательств:")
                view_all_publishers()
            case '2':
                print("Создание издательства:")
                add_publisher()
            case '3':
                print("Редактирование издательства:")
                edit_publisher()
            case '4':
                print("Удаление издательства:")
                delete_publisher()
            case '5':
                break
            case _:
                print('Неверный ввод. Повторите попытку!')


def admin_genres():
    while True:
        print_actions()
        action = input("Выберите действие: ")
        match action:
            case '1':
                print("Просмотр жанров:")
                view_all_genres()
            case '2':
                print("Создание жанра:")
                add_genre()
            case '3':
                print("Редактирование жанра:")
                edit_genre()
            case '4':
                print("Удаление жанра:")
                delete_genre()
            case '5':
                break
            case _:
                print('Неверный ввод. Повторите попытку!')


def admin_authors():
    while True:
        print_actions()
        action = input("Выберите действие: ")
        match action:
            case '1':
                print("Просмотр авторов:")
                view_all_authors()
            case '2':
                print("Создание автора:")
                add_author()
            case '3':
                print("Редактирование автора:")
                edit_author()
            case '4':
                print("Удаление автора:")
                delete_author()
            case '5':
                break
            case _:
                print('Неверный ввод. Повторите попытку!')


def admin_rew():
    while True:
        print_actions_rew()
        action = input("Выберите действие: ")
        match action:
            case '1':
                print("Просмотр отзывов:")
                view_all_reviews()
            case '2':
                print("Удаление отзыва:")
                delete_review()
            case '3':
                break
            case _:
                print('Неверный ввод. Повторите попытку!')



