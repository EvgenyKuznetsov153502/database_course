from main import connection, cursor
from fun_for_login import validate_input


def view_all_promotions():
    cursor.execute("SELECT * FROM Promotions")
    promotions = cursor.fetchall()

    for promotion in promotions:
        print(f"ID: {promotion[0]}, Описание: {promotion[1]}, Скидка: {promotion[2]}%")


def add_promotion():
    description = validate_input("Введите описание: ")
    while True:
        discount_percentage = validate_input("Введите размер скидки: ")
        try:
            if 0 <= int(discount_percentage) <= 100:
                break
            else:
                print("Скидка должна быть от 0 до 100")
        except:
            print("Ошибка ввода")
            return

    cursor.execute("INSERT INTO Promotions (description, discount_percentage) VALUES (%s, %s)",
                    (description, discount_percentage))
    connection.commit()
    print("Акция успешно добавлена.")


def edit_promotion():
    promotion_id = validate_input("Введите ID: ")
    new_description = validate_input("Введите новое описание: ")
    while True:
        new_discount_percentage = validate_input("Введите новый размер скидки: ")
        try:
            if 0 <= int(new_discount_percentage) <= 100:
                break
            else:
                print("Скидка должна быть от 0 до 100")
        except:
            print("Ошибка ввода")
            return

    # Проверка существования акции с указанным ID
    cursor.execute("SELECT * FROM Promotions WHERE id = %s", (promotion_id,))
    existing_promotion = cursor.fetchone()

    if existing_promotion:
        cursor.execute("UPDATE Promotions SET description = %s, discount_percentage = %s WHERE id = %s",
                       (new_description, new_discount_percentage, promotion_id))
        connection.commit()

        print("Акция успешно отредактирована.")
    else:
        print("Акция с указанным ID не существует.")


def delete_promotion():
    promotion_id = validate_input("Введите ID: ")

    # Проверка существования акции с указанным ID
    cursor.execute("SELECT * FROM Promotions WHERE id = %s", (promotion_id,))
    existing_promotion = cursor.fetchone()

    try:
        if existing_promotion:
            cursor.execute("DELETE FROM Promotions WHERE id = %s", (promotion_id,))
            connection.commit()
            print("Акция успешно удалена.")
        else:
            print("Акция с указанным ID не существует.")
    except:
        print("Ошибка удаления!")


def view_all_books():
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
    """)
    books = cursor.fetchall()

    # Вывод результатов
    for book in books:
        print(
            f"ID: {book[0]}, Название: {book[1]}, Автор: {book[2]}, Издатель: {book[3]}, Жанр: {book[4]}, Цена: {book[5]}, Количество: {book[6]}, Средняя оценка: {book[7]}")


def add_book():
    book_title = validate_input("Введите название книги: ")
    try:
        quantity = int(validate_input("Введите кол-во книг: "))
        price = int(validate_input("Введите цену: "))
        publisher_id = int(validate_input("Введите id издательства: "))
        promotion_id = int(validate_input("Введите id акции: "))
        if (quantity < 1) or (price < 1) or (publisher_id < 1) or (promotion_id < 1 ):
            print("Ошибка ввода")
            return
    except:
        print("Ошибка ввода")
        return

    if not is_publisher_id_valid(publisher_id):
        print(f"Ошибка: Издательство с ID {publisher_id} не существует.")
        return

    if not is_promotion_id_valid(promotion_id):
        print(f"Ошибка: Акция с ID {promotion_id} не существует.")
        return

    try:
        cursor.callproc("AddBook", (book_title, price, quantity, publisher_id, promotion_id))
        connection.commit()
        print("Книга успешно добавлена.")
    except:
       print("Ошибка добавления")


def is_publisher_id_valid(publisher_id):
    try:
        cursor.execute("SELECT id FROM Publishers WHERE id = %s", (publisher_id,))
        result = cursor.fetchone()
        return result is not None
    except:
        print("тест!!!")
        return False


def is_promotion_id_valid(promotion_id):
    try:
        cursor.execute("SELECT id FROM Promotions WHERE id = %s", (promotion_id,))
        result = cursor.fetchone()
        return result is not None
    except:
        return False


def edit_book():
    new_title = validate_input("Введите название книги: ")
    try:
        book_id = int(validate_input("Введите id книги: "))
        new_quantity = int(validate_input("Введите кол-во книг: "))
        new_price = int(validate_input("Введите цену: "))
        new_publisher_id = int(validate_input("Введите id издательства: "))
        new_promotion_id = int(validate_input("Введите id акции: "))
        if (new_quantity < 1) or (new_price < 1) or (new_publisher_id < 1) or (new_promotion_id < 1) or (book_id < 1):
            print("Ошибка ввода")
            return
    except:
        print("Ошибка ввода")
        return

    if not is_publisher_id_valid(new_publisher_id):
        print(f"Ошибка: Издательство с ID {new_publisher_id} не существует.")
        return

    if not is_promotion_id_valid(new_promotion_id):
        print(f"Ошибка: Акция с ID {new_promotion_id} не существует.")
        return

    try:
        # Проверка существования книги с указанным ID
        cursor.execute("SELECT * FROM Books WHERE id = %s", (book_id,))
        existing_book = cursor.fetchone()

        if existing_book:
            sql_query = """
                    UPDATE Books
                    SET 
                        book_title = %s,
                        price = %s,
                        quantity = %s,
                        publisher_id = %s,
                        promotion_id = %s
                    WHERE id = %s
                    """
            cursor.execute(sql_query, (new_title, new_price, new_quantity, new_publisher_id, new_promotion_id, book_id))

            # Подтверждение изменений в базе данных
            connection.commit()

            print("Книга успешно отредактирована.")
        else:
            print("Книга с указанным ID не существует.")

    except:
        print("Ошибка обновления")


def delete_book():
    try:
        book_id = int(validate_input("Введите id книги"))
        if book_id < 1:
            print("Ошибка ввода")
            return
    except:
        print("Ошибка ввода")
        return

    try:
        cursor.execute("SELECT * FROM Books WHERE id = %s", (book_id,))
        existing_book = cursor.fetchone()
        if existing_book:
            cursor.execute("DELETE FROM Books WHERE id = %s", (book_id,))
            connection.commit()
            print("Книга успешно удалена.")
        else:
            print("Книга с указанным ID не существует.")

    except:
        print("Ошибка удаления")


def view_all_publishers():
    cursor.execute("""
        SELECT id, name, country
        FROM Publishers
    """)
    publishers = cursor.fetchall()

    # Вывод результатов
    for publisher in publishers:
        print(f"ID: {publisher[0]}, Название: {publisher[1]}, Страна: {publisher[2]}")


def add_publisher():
    name = validate_input("Введите название: ")
    country = validate_input("Введите страну: ")
    try:
        cursor.execute("""
            INSERT INTO Publishers (name, country) 
            VALUES (%s, %s)
        """, (name, country))
        connection.commit()
        print("Издательство успешно добавлено.")
    except Exception as e:
        print(f"Ошибка при добавлении издательства: {e}")


def edit_publisher():
    try:
        publisher_id = int(validate_input("Введит id: "))
        new_name = validate_input("Введите название: ")
        new_country = validate_input("Введите страну: ")
    except:
        print("Ошибка редкатирования")
        return

    try:
        cursor.execute("SELECT * FROM Publishers WHERE id = %s", (publisher_id,))
        existing_publisher = cursor.fetchone()

        if existing_publisher:
            cursor.execute("""
                UPDATE Publishers 
                SET name = %s, country = %s 
                WHERE id = %s
            """, (new_name, new_country, publisher_id))
            connection.commit()
            print("Издательство успешно отредактировано.")
        else:
            print("Издательство не найдено.")
    except Exception as e:
        print(f"Ошибка при редактировании издательства: {e}")


def delete_publisher():
    try:
        publisher_id = int(validate_input("Введит id: "))
    except:
        print("Ошибка удаления")
        return
    try:
        cursor.execute("SELECT * FROM Publishers WHERE id = %s", (publisher_id,))
        existing_publisher = cursor.fetchone()

        if existing_publisher:
            cursor.execute("""
                DELETE FROM Publishers 
                WHERE id = %s
            """, (publisher_id,))
            connection.commit()
            print("Издательство успешно удалено.")
        else:
            print("Издательство не найдено.")
    except Exception as e:
        print(f"Ошибка при удалении издательства: {e}")


def add_genre():
    name = validate_input("Введите название жанра: ")
    try:
        cursor.execute("""
            INSERT INTO Genres (name) 
            VALUES (%s)
        """, (name,))
        connection.commit()
        print("Жанр успешно добавлен.")
    except Exception as e:
        print(f"Ошибка при добавлении жанра: {e}")


def edit_genre():
    try:
        genre_id = int(validate_input("Введит id: "))
        new_name = validate_input("Введите новое название: ")
    except:
        print("Ошибка редактирования")
        return
    try:
        # Проверяем существование жанра
        cursor.execute("SELECT * FROM Genres WHERE id = %s", (genre_id,))
        existing_genre = cursor.fetchone()

        if existing_genre:
            cursor.execute("""
                UPDATE Genres 
                SET name = %s 
                WHERE id = %s
            """, (new_name, genre_id))
            connection.commit()
            print("Жанр успешно отредактирован.")
        else:
            print("Жанр не найден.")
    except Exception as e:
        print(f"Ошибка при редактировании жанра: {e}")


def delete_genre():
    try:
        genre_id = int(validate_input("Введит id: "))
    except:
        print("Ошибка удаления")
        return
    try:
        # Проверяем существование жанра
        cursor.execute("SELECT * FROM Genres WHERE id = %s", (genre_id,))
        existing_genre = cursor.fetchone()

        if existing_genre:
            cursor.execute("""
                DELETE FROM Genres 
                WHERE id = %s
            """, (genre_id,))
            connection.commit()
            print("Жанр успешно удален.")
        else:
            print("Жанр не найден.")
    except Exception as e:
        print(f"Ошибка при удалении жанра: {e}")


def view_all_genres():
    cursor.execute("""
        SELECT id, name
        FROM Genres
    """)
    genres = cursor.fetchall()

    # Вывод результатов
    for genre in genres:
        print(f"ID: {genre[0]}, Название: {genre[1]}")


def view_all_authors():
    cursor.execute("""
        SELECT id, name, country
        FROM Authors
    """)
    authors = cursor.fetchall()

    # Вывод результатов
    for author in authors:
        print(f"ID: {author[0]}, Имя: {author[1]}, Страна: {author[2]}")


def add_author():
    name = validate_input("Введите имя")
    country = validate_input("Введите страну")
    try:
        cursor.execute("""
            INSERT INTO Authors (name, country) 
            VALUES (%s, %s)
        """, (name, country))
        connection.commit()
        print("Автор успешно добавлен.")
    except Exception as e:
        print(f"Ошибка при добавлении автора: {e}")


def edit_author():
    try:
        author_id = int(validate_input("Введит id: "))
        new_name = validate_input("Введите имя: ")
        new_country = validate_input("Введите страну: ")
    except:
        print("Ошибка редактирования")
        return

    try:
        # Проверяем существование автора
        cursor.execute("SELECT * FROM Authors WHERE id = %s", (author_id,))
        existing_author = cursor.fetchone()

        if existing_author:
            cursor.execute("""
                UPDATE Authors 
                SET name = %s, country = %s 
                WHERE id = %s
            """, (new_name, new_country, author_id))
            connection.commit()
            print("Автор успешно отредактирован.")
        else:
            print("Автор не найден.")
    except Exception as e:
        print(f"Ошибка при редактировании автора: {e}")


def delete_author():
    try:
        author_id = int(validate_input("Введит id: "))
    except:
        print("Ошибка удаления")
        return
    try:
        # Проверяем существование автора
        cursor.execute("SELECT * FROM Authors WHERE id = %s", (author_id,))
        existing_author = cursor.fetchone()

        if existing_author:
            cursor.execute("""
                DELETE FROM Authors 
                WHERE id = %s
            """, (author_id,))
            connection.commit()
            print("Автор успешно удален.")
        else:
            print("Автор не найден.")
    except Exception as e:
        print(f"Ошибка при удалении автора: {e}")


def view_all_logs():
    try:
        cursor.execute("""
            SELECT id, message, id_customer
            FROM Log
        """)
        logs = cursor.fetchall()

        # Вывод результатов
        for log in logs:
            print(f"ID: {log[0]}, Сообщение: {log[1]}, ID Клиента: {log[2]}")
    except Exception as e:
        print(f"Ошибка при чтении логов: {e}")










