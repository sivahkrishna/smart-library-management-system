
from database import execute_query, get_rows, sql_quote


def add_book():
    print("\n--- ADD NEW BOOK ---")

    title = input("Book title: ").strip()
    author = input("Author: ").strip()
    isbn = input("ISBN: ").strip()
    category = input("Category: ").strip()
    quantity = input("Number of copies: ").strip()

    if not title or not author:
        print("Title and author are required.")
        return

    if not quantity.isdigit() or int(quantity) < 1:
        print("Enter a valid positive quantity.")
        return

    isbn_sql = "NULL" if not isbn else sql_quote(isbn)
    category_sql = "NULL" if not category else sql_quote(category)

    sql = f"""
    INSERT INTO books
    (title, author, isbn, category, total_copies, available_copies)
    VALUES (
        {sql_quote(title)},
        {sql_quote(author)},
        {isbn_sql},
        {category_sql},
        {int(quantity)},
        {int(quantity)}
    );
    """

    if execute_query(sql) is not None:
        print("Book added successfully.")


def view_books():
    sql = """
    SELECT book_id, title, author, category,
           total_copies, available_copies
    FROM books
    ORDER BY book_id;
    """

    rows = get_rows(sql)

    print("\n--- ALL BOOKS ---")

    if not rows:
        print("No books found.")
        return

    print("ID | TITLE | AUTHOR | CATEGORY | TOTAL | AVAILABLE")

    for row in rows:
        print(" | ".join(row))


def search_book():
    keyword = input("Enter book title or author: ").strip()

    if not keyword:
        print("Search text cannot be empty.")
        return

    sql = f"""
    SELECT book_id, title, author, available_copies
    FROM books
    WHERE title LIKE {sql_quote('%' + keyword + '%')}
       OR author LIKE {sql_quote('%' + keyword + '%')};
    """

    rows = get_rows(sql)

    if not rows:
        print("No matching books found.")
        return

    for row in rows:
        print(" | ".join(row))


def update_book():
    book_id = input("Enter book ID: ").strip()

    if not book_id.isdigit():
        print("Invalid book ID.")
        return

    title = input("New title: ").strip()
    author = input("New author: ").strip()
    category = input("New category: ").strip()

    if not title or not author:
        print("Title and author cannot be empty.")
        return

    sql = f"""
    UPDATE books
    SET title = {sql_quote(title)},
        author = {sql_quote(author)},
        category = {sql_quote(category)}
    WHERE book_id = {int(book_id)};
    """

    if execute_query(sql) is not None:
        print("Book update command completed.")


def delete_book():
    book_id = input("Enter book ID to delete: ").strip()

    if not book_id.isdigit():
        print("Invalid book ID.")
        return

    sql = f"""
    DELETE FROM books
    WHERE book_id = {int(book_id)}
      AND NOT EXISTS (
          SELECT 1
          FROM borrow_transactions
          WHERE borrow_transactions.book_id = books.book_id
      );
    """

    if execute_query(sql) is not None:
        print("Delete command completed.")
        print("A book with borrowing history cannot be deleted.")
