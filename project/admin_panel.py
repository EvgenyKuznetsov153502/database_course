from main import connection, cursor


def login_fun():
    while True:

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
