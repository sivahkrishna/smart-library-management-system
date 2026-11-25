
from database import get_rows


def library_statistics():
    print("\n--- LIBRARY STATISTICS ---")

    queries = {
        "Total books": "SELECT COUNT(*) FROM books;",
        "Total members": "SELECT COUNT(*) FROM members;",
        "Active members": "SELECT COUNT(*) FROM members WHERE active = TRUE;",
        "Available copies": "SELECT COALESCE(SUM(available_copies), 0) FROM books;",
        "Currently issued": "SELECT COUNT(*) FROM borrow_transactions WHERE status = 'ISSUED';",
        "Returned transactions": "SELECT COUNT(*) FROM borrow_transactions WHERE status = 'RETURNED';",
        "Overdue transactions": """
            SELECT COUNT(*)
            FROM borrow_transactions
            WHERE status = 'ISSUED'
              AND due_date < CURDATE();
        """
    }

    for label, query in queries.items():
        rows = get_rows(query)

        value = rows[0][0] if rows else "0"

        print(f"{label}: {value}")


def most_borrowed_books():
    print("\n--- MOST BORROWED BOOKS ---")

    sql = """
    SELECT
        b.title,
        COUNT(bt.transaction_id) AS borrow_count
    FROM books b
    LEFT JOIN borrow_transactions bt
        ON b.book_id = bt.book_id
    GROUP BY b.book_id, b.title
    ORDER BY borrow_count DESC
    LIMIT 10;
    """

    rows = get_rows(sql)

    if not rows:
        print("No report data.")
        return

    for row in rows:
        print(" | ".join(row))


def member_borrowing_report():
    print("\n--- MEMBER BORROWING REPORT ---")

    sql = """
    SELECT
        m.member_id,
        m.name,
        COUNT(bt.transaction_id) AS total_borrowed
    FROM members m
    LEFT JOIN borrow_transactions bt
        ON m.member_id = bt.member_id
    GROUP BY m.member_id, m.name
    ORDER BY total_borrowed DESC;
    """

    rows = get_rows(sql)

    for row in rows:
        print(" | ".join(row))
