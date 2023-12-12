from main import connection, cursor
import bcrypt


def register_user():
    while True:
        login = validate_input("Введите логин: ")
        cursor.execute("SELECT id FROM User WHERE login = %s", (login,))
        if cursor.fetchone():
            print("Логин уже занят. Выберите другой логин.")
        else:
            break

    while True:
        password = validate_input("Введите пароль: ", is_empty=True)
        confirm_password = validate_input("Повторите пароль: ", is_empty=True)
        if password != confirm_password:
            print("Пароли не совпадают. Попробуйте еще раз.")
        else:
            break

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    surname = validate_input("Введите фамилию: ")
    name = validate_input("Введите имя: ")
    patronymic = validate_input("Введите отчество: ")
    telephone = validate_input("Введите телефон: ")
    email = validate_input("Введите электронную почту: ")

    # Вставка данных в таблицу Customers
    cursor.execute(
        "INSERT INTO Customers (surname, name, patronymic, telephone, email) VALUES (%s, %s, %s, %s, %s)",
        (surname, name, patronymic, telephone, email)
    )
    customer_id = cursor.lastrowid

    # Вставка данных в таблицу User
    cursor.execute(
        "INSERT INTO User (login, password, id_customer) VALUES (%s, %s, %s)",
        (login, hashed_password, customer_id)
    )

    # Подтверждение изменений в базе данных
    connection.commit()

    print("Пользователь успешно зарегистрирован.")


def validate_input(prompt, is_empty=False):
    while True:
        user_input = input(prompt)
        if is_empty or user_input.strip():
            return user_input
        else:
            print("Введите непустую строку.")


def authenticate_user():

    login = validate_input("Введите логин: ")
    password = validate_input("Введите пароль: ", is_empty=True)

    # Получение хэшированного пароля из базы данных
    cursor.execute("SELECT password FROM User WHERE login = %s", (login,))
    hashed_password = cursor.fetchone()

    if hashed_password:
        # Проверка введенного пароля
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password[0].encode('utf-8')):
            print("Авторизация успешна.")
            return login
        else:
            print("Неверные учетные данные.")
    else:
        print("Пользователь с таким логином не найден.")


def authenticate_admin():
    admin_name = "Admin"
    admin_password = "qwerty"

    login = validate_input("Введите логин: ")
    password = validate_input("Введите пароль: ", is_empty=True)

    if admin_name == login:
        if password == admin_password:
            print("Авторизация успешна.")
            return True
        else:
            print("Неверный пароль.")
            return False
    else:
        print("Неверные учетные данные.")
        return False
