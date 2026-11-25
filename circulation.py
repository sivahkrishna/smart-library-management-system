
from database import execute_query, sql_quote


def issue_book():
    print("\n--- ISSUE BOOK ---")

    member_id = input("Enter member ID: ").strip()
    book_id = input("Enter book ID: ").strip()

    if not member_id.isdigit() or not book_id.isdigit():
        print("Member ID and book ID must be numbers.")
        return

    member_id = int(member_id)
    book_id = int(book_id)

    # All these statements run in one MySQL session.
    # Row locks prevent two requests from taking the final copy.

    sql = f"""
    START TRANSACTION;

    SELECT member_id
    FROM members
    WHERE member_id = {member_id}
      AND active = TRUE
    FOR UPDATE;

    SET @member_ok = ROW_COUNT();

    SELECT book_id
    FROM books
    WHERE book_id = {book_id}
    FOR UPDATE;

    SET @book_ok = ROW_COUNT();

    SELECT COUNT(*)
    INTO @active_count
    FROM borrow_transactions
    WHERE member_id = {member_id}
      AND status = 'ISSUED';

    UPDATE books
    SET available_copies = available_copies - 1
    WHERE book_id = {book_id}
      AND available_copies > 0
      AND @member_ok = 1
      AND @book_ok = 1
      AND @active_count < 3;

    SET @updated = ROW_COUNT();

    INSERT INTO borrow_transactions
    (book_id, member_id, issue_date, due_date, status)
    SELECT
        {book_id},
        {member_id},
        CURDATE(),
        DATE_ADD(CURDATE(), INTERVAL 14 DAY),
        'ISSUED'
    WHERE @updated = 1;

    SELECT CASE
        WHEN @member_ok = 0 THEN 'INVALID OR INACTIVE MEMBER'
        WHEN @book_ok = 0 THEN 'BOOK NOT FOUND'
        WHEN @active_count >= 3 THEN 'MEMBER HAS REACHED THE BORROW LIMIT'
        WHEN @updated = 0 THEN 'NO COPIES AVAILABLE'
        ELSE 'BOOK ISSUED SUCCESSFULLY'
    END;

    COMMIT;
    """

    result = execute_query(sql)

    if result:
        print(result)
    else:
        print("Issue operation could not be completed.")


def return_book():
    print("\n--- RETURN BOOK ---")

    transaction_id = input("Enter transaction ID: ").strip()

    if not transaction_id.isdigit():
        print("Invalid transaction ID.")
        return

    transaction_id = int(transaction_id)

    sql = f"""
    START TRANSACTION;

    SELECT book_id
    INTO @book_id
    FROM borrow_transactions
    WHERE transaction_id = {transaction_id}
      AND status = 'ISSUED'
    FOR UPDATE;

    SET @found = ROW_COUNT();

    UPDATE borrow_transactions
    SET status = 'RETURNED',
        return_date = CURDATE()
    WHERE transaction_id = {transaction_id}
      AND status = 'ISSUED';

    SET @changed = ROW_COUNT();

    UPDATE books
    SET available_copies = available_copies + 1
    WHERE book_id = @book_id
      AND @changed = 1;

    SELECT CASE
        WHEN @changed = 1 THEN 'BOOK RETURNED SUCCESSFULLY'
        ELSE 'ACTIVE TRANSACTION NOT FOUND'
    END;

    COMMIT;
    """

    result = execute_query(sql)

    if result:
        print(result)
    else:
        print("Return operation failed.")


def renew_book():
    print("\n--- RENEW BOOK ---")

    transaction_id = input("Enter transaction ID: ").strip()

    if not transaction_id.isdigit():
        print("Invalid transaction ID.")
        return

    transaction_id = int(transaction_id)

    sql = f"""
    UPDATE borrow_transactions
    SET due_date = DATE_ADD(due_date, INTERVAL 7 DAY)
    WHERE transaction_id = {transaction_id}
      AND status = 'ISSUED'
      AND due_date >= CURDATE()
      AND (
          SELECT COUNT(*)
          FROM borrow_transactions AS other
          WHERE other.member_id = borrow_transactions.member_id
            AND other.status = 'ISSUED'
      ) <= 3;
    """

    if execute_query(sql) is not None:
        print("Renewal command completed.")
        print("Only active, not-yet-overdue transactions can be renewed.")
