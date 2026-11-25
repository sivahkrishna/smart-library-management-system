
import threading
import time
import subprocess

from database import get_rows


# Used to safely print messages from different threads
print_lock = threading.Lock()

# Used to stop the background monitoring thread
stop_event = threading.Event()


def safe_print(message):
    with print_lock:
        print(message)


# THREAD 1: Background overdue monitoring

def overdue_monitor():
    safe_print("[Overdue Thread] Started.")

    while not stop_event.is_set():

        sql = """
        SELECT COUNT(*)
        FROM borrow_transactions
        WHERE status = 'ISSUED'
          AND due_date < CURDATE();
        """

        rows = get_rows(sql)

        count = rows[0][0] if rows else "0"

        safe_print(
            f"[Overdue Thread] Current overdue books: {count}"
        )

        # Wait 60 seconds, but allow the thread to stop early
        stop_event.wait(60)

    safe_print("[Overdue Thread] Stopped.")


def start_overdue_monitor():
    thread = threading.Thread(
        target=overdue_monitor,
        name="OverdueMonitor",
        daemon=True
    )

    thread.start()

    return thread


# THREAD 2: Background report generation

def generate_report_task():
    safe_print("[Report Thread] Generating report...")

    sql = """
    SELECT title, COUNT(bt.transaction_id)
    FROM books b
    LEFT JOIN borrow_transactions bt
        ON b.book_id = bt.book_id
    GROUP BY b.book_id, b.title
    ORDER BY COUNT(bt.transaction_id) DESC;
    """

    rows = get_rows(sql)

    with print_lock:
        print("\n===== BACKGROUND REPORT =====")

        for row in rows:
            print(" | ".join(row))

        print("==============================\n")


def start_report_thread():
    thread = threading.Thread(
        target=generate_report_task,
        name="ReportGenerator"
    )

    thread.start()

    return thread


# THREAD 3: Database backup

def backup_database_task():
    safe_print("[Backup Thread] Starting database backup...")

    try:
        with open("smart_library_backup.sql", "w") as backup_file:

            result = subprocess.run(
                [
                    "mysqldump",
                    "--single-transaction",
                    "smart_library"
                ],
                stdout=backup_file,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )

        safe_print(
            "[Backup Thread] Backup created: smart_library_backup.sql"
        )

    except FileNotFoundError:
        safe_print(
            "[Backup Thread] mysqldump command was not found."
        )

    except subprocess.CalledProcessError as error:
        safe_print(
            "[Backup Thread] Backup failed: " + error.stderr
        )


def start_backup_thread():
    thread = threading.Thread(
        target=backup_database_task,
        name="DatabaseBackup"
    )

    thread.start()

    return thread


# THREAD 4: Concurrent book issue simulation

def concurrent_issue_worker(member_id, book_id, result_list, index):
    """
    Two threads try to issue the same book.
    MySQL row locking prevents both from taking the final copy.
    """

    sql = f"""
    START TRANSACTION;

    SELECT book_id
    FROM books
    WHERE book_id = {int(book_id)}
    FOR UPDATE;

    SET @book_found = ROW_COUNT();

    UPDATE books
    SET available_copies = available_copies - 1
    WHERE book_id = {int(book_id)}
      AND available_copies > 0
      AND @book_found = 1;

    SET @changed = ROW_COUNT();

    INSERT INTO borrow_transactions
    (book_id, member_id, issue_date, due_date, status)
    SELECT
        {int(book_id)},
        {int(member_id)},
        CURDATE(),
        DATE_ADD(CURDATE(), INTERVAL 14 DAY),
        'ISSUED'
    WHERE @changed = 1
      AND EXISTS (
          SELECT 1
          FROM members
          WHERE member_id = {int(member_id)}
            AND active = TRUE
      );

    SET @inserted = ROW_COUNT();

    -- If the member is invalid, restore the copy.
    UPDATE books
    SET available_copies = available_copies + 1
    WHERE book_id = {int(book_id)}
      AND @changed = 1
      AND @inserted = 0;

    SELECT CASE
        WHEN @book_found = 0 THEN 'BOOK NOT FOUND'
        WHEN @changed = 0 THEN 'NO COPY AVAILABLE'
        WHEN @inserted = 1 THEN 'ISSUE SUCCESSFUL'
        ELSE 'INVALID MEMBER'
    END;

    COMMIT;
    """

    from database import execute_query

    result = execute_query(sql)

    result_list[index] = result or "REQUEST FAILED"

    safe_print(
        f"[Thread {index + 1}] Member {member_id}: {result_list[index]}"
    )


def run_concurrency_test():
    print("\n--- CONCURRENT ISSUE TEST ---")

    book_id = input("Enter book ID to test: ").strip()
    member1 = input("Enter first member ID: ").strip()
    member2 = input("Enter second member ID: ").strip()

    if not all(value.isdigit() for value in [book_id, member1, member2]):
        print("All IDs must be numbers.")
        return

    book_id = int(book_id)
    member1 = int(member1)
    member2 = int(member2)

    rows = get_rows(
        f"SELECT available_copies FROM books WHERE book_id = {book_id};"
    )

    if not rows:
        print("Book not found.")
        return

    print("Available copies before test:", rows[0][0])

    results = [None, None]

    thread1 = threading.Thread(
        target=concurrent_issue_worker,
        args=(member1, book_id, results, 0)
    )

    thread2 = threading.Thread(
        target=concurrent_issue_worker,
        args=(member2, book_id, results, 1)
    )

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    print("\nConcurrent test completed.")
    print("Thread 1:", results[0])
    print("Thread 2:", results[1])


def stop_background_tasks():
    stop_event.set()
