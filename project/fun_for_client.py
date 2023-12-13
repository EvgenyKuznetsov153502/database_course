from main import connection, cursor
from fun_for_login import validate_input


def search_books_by_genre():
    genre_name = validate_input("Введите жанр: ")
    try:
        cursor.execute("""
            SELECT 
                B.id AS book_id,
                B.book_title,
                A.name AS author_name,
                P.name AS publisher_name,
                G.name AS genre_name,
                B.price,
                B.quantity,
                B.average_mark
            FROM 
                Books B
                LEFT JOIN Authors_and_Books AB ON B.id = AB.book_id
                LEFT JOIN Authors A ON AB.author_id = A.id
                LEFT JOIN Publishers P ON B.publisher_id = P.id
                LEFT JOIN Books_and_Genres BG ON B.id = BG.book_id
                LEFT JOIN Genres G ON BG.genre_id = G.id
            WHERE G.name = %s
        """, (genre_name,))
        books = cursor.fetchall()

        # Вывод результатов
        for book in books:
            print(
                f"ID: {book[0]}, Название: {book[1]}, Автор: {book[2]}, Издатель: {book[3]}, Жанр: {book[4]}, Цена: {book[5]}, Количество: {book[6]}, Средняя оценка: {book[7]}")
    except Exception as e:
        print(f"Ошибка при поиске книг по жанру: {e}")


def search_books_by_title():
    title = validate_input("Введите название: ")
    try:
        cursor.execute("""
            SELECT 
                B.id AS book_id,
                B.book_title,
                A.name AS author_name,
                P.name AS publisher_name,
                G.name AS genre_name,
                B.price,
                B.quantity,
                B.average_mark
            FROM 
                Books B
                LEFT JOIN Authors_and_Books AB ON B.id = AB.book_id
                LEFT JOIN Authors A ON AB.author_id = A.id
                LEFT JOIN Publishers P ON B.publisher_id = P.id
                LEFT JOIN Books_and_Genres BG ON B.id = BG.book_id
                LEFT JOIN Genres G ON BG.genre_id = G.id
            WHERE B.book_title LIKE %s
        """, (f"%{title}%",))
        books = cursor.fetchall()

        # Вывод результатов
        for book in books:
            print(
                f"ID: {book[0]}, Название: {book[1]}, Автор: {book[2]}, Издатель: {book[3]}, Жанр: {book[4]}, Цена: {book[5]}, Количество: {book[6]}, Средняя оценка: {book[7]}")
    except Exception as e:
        print(f"Ошибка при поиске книг по названию: {e}")


def search_books_by_author():
    author_name = validate_input("Введите имя автора: ")
    try:
        cursor.execute("""
            SELECT 
                B.id AS book_id,
                B.book_title,
                A.name AS author_name,
                P.name AS publisher_name,
                G.name AS genre_name,
                B.price,
                B.quantity,
                B.average_mark
            FROM 
                Books B
                LEFT JOIN Authors_and_Books AB ON B.id = AB.book_id
                LEFT JOIN Authors A ON AB.author_id = A.id
                LEFT JOIN Publishers P ON B.publisher_id = P.id
                LEFT JOIN Books_and_Genres BG ON B.id = BG.book_id
                LEFT JOIN Genres G ON BG.genre_id = G.id
            WHERE A.name LIKE %s
        """, (f"%{author_name}%",))
        books = cursor.fetchall()

        # Вывод результатов
        for book in books:
            print(
                f"ID: {book[0]}, Название: {book[1]}, Автор: {book[2]}, Издатель: {book[3]}, Жанр: {book[4]}, Цена: {book[5]}, Количество: {book[6]}, Средняя оценка: {book[7]}")
    except Exception as e:
        print(f"Ошибка при поиске книг по автору: {e}")


def add_order(customer_id, book_id, status_id):
    try:
        # Вызываем хранимую процедуру AddOrder
        cursor.callproc('AddOrder', (customer_id, book_id, status_id))

        # Коммитим изменения в базу данных
        connection.commit()

        print("Заказ успешно оформлен.")
    except Exception as e:
        print(f"Ошибка при оформлении заказа: {e}")


def get_customer_id_by_login(user_login):
    try:
        cursor.execute("SELECT id_customer FROM User WHERE login = %s", (user_login,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            print("Пользователь с таким логином не найден.")
            return None
    except Exception as e:
        print(f"Ошибка при получении id пользователя: {e}")
        return None


def check_book_id(book_id):
    try:
        cursor.execute("SELECT id FROM Books WHERE id = %s", (book_id,))
        result = cursor.fetchone()
        if result:
            return True
        else:
            print("Книга с таким ID не найдена.")
            return False
    except Exception as e:
        print(f"Ошибка при проверке ID книги: {e}")
        return False


def make_order(login):
    try:
        book_id = int(validate_input("Введит id: "))
    except:
        print("Ошибка удаления")
        return
    customer_id = get_customer_id_by_login(login)
    if customer_id is not None and check_book_id(book_id):
        add_order(customer_id, book_id, 1)


def track_order_status(user_login):
    try:
        # Получаем customer_id по логину
        cursor.execute("SELECT id_customer FROM User WHERE login = %s", (user_login,))
        result = cursor.fetchone()

        if result:
            customer_id = result[0]

            # Получаем статусы заказов для конкретного пользователя
            cursor.execute("""
                SELECT 
                    O.id AS order_id,
                    O.order_date,
                    S.status
                FROM 
                    Orders O
                    JOIN Delivery_status S ON O.status_id = S.id
                    JOIN Order_history H ON O.history_id = H.id
                WHERE H.customer_id = %s
            """, (customer_id,))

            order_statuses = cursor.fetchall()

            if order_statuses:
                print(f"Статусы заказов для пользователя {user_login}:")

                for order_status in order_statuses:
                    print(f"Заказ ID: {order_status[0]}, Дата: {order_status[1]}, Статус: {order_status[2]}")
            else:
                print(f"Для пользователя {user_login} нет оформленных заказов.")
        else:
            print("Пользователь с таким логином не найден.")
    except Exception as e:
        print(f"Ошибка при отслеживании статуса заказов: {e}")


def leave_review(user_login):
    try:
        book_id = int(validate_input("Введит id: "))
        mark = int(validate_input("Введит оценку: "))
        description = validate_input("Введите отзыв: ")
        if not (0 <= mark <= 10):
            print("Оценка от 0 до 10")
            return
    except:
        print("Ошибка добавления")
        return
    try:
        cursor.execute("SELECT id_customer FROM User WHERE login = %s", (user_login,))
        result = cursor.fetchone()

        if result:
            customer_id = result[0]

            cursor.execute("SELECT id FROM Books WHERE id = %s", (book_id,))
            book_exists = cursor.fetchone()

            if book_exists:
                # Добавляем отзыв
                cursor.execute("""
                    INSERT INTO Reviews (description, mark, book_id, customer_id) 
                    VALUES (%s, %s, %s, %s)
                """, (description, mark, book_id, customer_id))

                connection.commit()
                print("Отзыв успешно добавлен.")
            else:
                print("Книга с таким ID не найдена.")
        else:
            print("Пользователь с таким логином не найден.")
    except Exception as e:
        print(f"Ошибка при оставлении отзыва: {e}")


def view_order_history(user_login):
    try:
        cursor.execute("SELECT id_customer FROM User WHERE login = %s", (user_login,))
        result = cursor.fetchone()

        if result:
            customer_id = result[0]

            # Получаем историю заказов для конкретного пользователя
            cursor.execute("""
                SELECT 
                    O.id AS order_id,
                    O.order_date,
                    S.status,
                    B.book_title,
                    B.price
                FROM 
                    Orders O
                    JOIN Delivery_status S ON O.status_id = S.id
                    JOIN Order_history H ON O.history_id = H.id
                    JOIN Books B ON O.book_id = B.id
                WHERE H.customer_id = %s
            """, (customer_id,))

            order_history = cursor.fetchall()

            if order_history:
                print(f"История заказов для пользователя {user_login}:")

                for order in order_history:
                    print(f"Заказ ID: {order[0]}, Дата: {order[1]}, Статус: {order[2]}, Книга: {order[3]}, Цена: {order[4]}")
            else:
                print(f"Для пользователя {user_login} нет оформленных заказов.")
        else:
            print("Пользователь с таким логином не найден.")
    except Exception as e:
        print(f"Ошибка при просмотре истории заказов: {e}")





