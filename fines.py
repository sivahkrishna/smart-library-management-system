
from database import execute_query, get_rows


def calculate_fines():
    print("\n--- OVERDUE FINE REPORT ---")

    sql = """
    SELECT
        bt.transaction_id,
        m.name,
        b.title,
        bt.due_date,
        DATEDIFF(CURDATE(), bt.due_date) AS overdue_days,
        DATEDIFF(CURDATE(), bt.due_date) * 5 AS fine_amount
    FROM borrow_transactions bt
    JOIN members m ON bt.member_id = m.member_id
    JOIN books b ON bt.book_id = b.book_id
    WHERE bt.status = 'ISSUED'
      AND bt.due_date < CURDATE();
    """

    rows = get_rows(sql)

    if not rows:
        print("No overdue books.")
        return

    for row in rows:
        print(" | ".join(row))


def record_fines():
    sql = """
    INSERT INTO fines
        (transaction_id, amount, paid_amount, payment_status)
    SELECT
        transaction_id,
        DATEDIFF(CURDATE(), due_date) * 5,
        0,
        'UNPAID'
    FROM borrow_transactions
    WHERE status = 'RETURNED'
      AND return_date > due_date
    ON DUPLICATE KEY UPDATE
        amount = GREATEST(
            amount,
            DATEDIFF(
                (SELECT return_date
                 FROM borrow_transactions
                 WHERE transaction_id = fines.transaction_id),
                (SELECT due_date
                 FROM borrow_transactions
                 WHERE transaction_id = fines.transaction_id)
            ) * 5
        );
    """

    if execute_query(sql) is not None:
        print("Fine records updated.")


def view_fines():
    sql = """
    SELECT
        f.fine_id,
        bt.transaction_id,
        m.name,
        f.amount,
        f.paid_amount,
        f.payment_status
    FROM fines f
    JOIN borrow_transactions bt
        ON f.transaction_id = bt.transaction_id
    JOIN members m
        ON bt.member_id = m.member_id
    ORDER BY f.fine_id;
    """

    rows = get_rows(sql)

    if not rows:
        print("No fine records found.")
        return

    for row in rows:
        print(" | ".join(row))


def pay_fine():
    fine_id = input("Enter fine ID: ").strip()

    if not fine_id.isdigit():
        print("Invalid fine ID.")
        return

    amount = input("Enter payment amount: ").strip()

    try:
        payment = float(amount)
        if payment <= 0:
            raise ValueError
    except ValueError:
        print("Enter a valid positive amount.")
        return

    sql = f"""
    UPDATE fines
    SET paid_amount = paid_amount + {payment:.2f},
        payment_status = CASE
            WHEN paid_amount + {payment:.2f} >= amount
                THEN 'PAID'
            ELSE 'PARTIAL'
        END
    WHERE fine_id = {int(fine_id)}
      AND paid_amount + {payment:.2f} <= amount;
    """

    if execute_query(sql) is not None:
        print("Payment command completed.")
        print("Check the fine list to confirm the updated balance.")
