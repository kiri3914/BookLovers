from apps.books.models import Author, Genre, Book

books = [
    {
        "author": "Франсуа Рабле",
        "book_name": "Гаргантюа и Пантагрюэль",
        "genre": "Сатира",
        "description": "Феерия душевного здоровья, грубых и добрых шуток, пародия пародий, каталог всего. Сколько столетий прошло, а ничего не изменилось."
    }
]

# Проходимся по списку книг и добавляем их в базу данных
for book_data in books:
    author_name = book_data["author"]
    book_name = book_data["book_name"]
    genres = [genre.strip() for genre in book_data["genre"].split(',')]  # Разделение жанров по запятой
    description = book_data["description"]
    # Поиск или создание автора
    author, created = Author.objects.get_or_create(
        first_name=author_name.split()[0],
        last_name=author_name.split()[-1],
        defaults={"birth_date": None, "bio": ""}
    )
    # Создание книги и связывание с автором
    book = Book.objects.create(
        title=book_name,
        description=description
    )
    book.author.add(author)
    # Добавление жанров к книге
    for genre_name in genres:
        genre, created = Genre.objects.get_or_create(
            name=genre_name.strip(),
            defaults={"description": ""}
        )
        book.genre.add(genre)
