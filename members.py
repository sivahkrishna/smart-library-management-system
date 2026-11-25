
from database import execute_query, get_rows, sql_quote


def add_member():
    print("\n--- REGISTER MEMBER ---")

    name = input("Member name: ").strip()
    email = input("Email: ").strip()
    phone = input("Phone: ").strip()

    if not name:
        print("Name is required.")
        return

    email_sql = "NULL" if not email else sql_quote(email)
    phone_sql = "NULL" if not phone else sql_quote(phone)

    sql = f"""
    INSERT INTO members
    (name, email, phone, joined_date)
    VALUES (
        {sql_quote(name)},
        {email_sql},
        {phone_sql},
        CURDATE()
    );
    """

    if execute_query(sql) is not None:
        print("Member registered successfully.")


def view_members():
    sql = """
    SELECT member_id, name, email, phone, joined_date, active
    FROM members
    ORDER BY member_id;
    """

    rows = get_rows(sql)

    print("\n--- MEMBER LIST ---")

    if not rows:
        print("No members found.")
        return

    for row in rows:
        print(" | ".join(row))


def search_member():
    keyword = input("Enter member name: ").strip()

    if not keyword:
        print("Search text cannot be empty.")
        return

    sql = f"""
    SELECT member_id, name, email, phone, active
    FROM members
    WHERE name LIKE {sql_quote('%' + keyword + '%')};
    """

    rows = get_rows(sql)

    if not rows:
        print("No members found.")
        return

    for row in rows:
        print(" | ".join(row))


def deactivate_member():
    member_id = input("Enter member ID: ").strip()

    if not member_id.isdigit():
        print("Invalid member ID.")
        return

    sql = f"""
    UPDATE members
    SET active = FALSE
    WHERE member_id = {int(member_id)}
      AND NOT EXISTS (
          SELECT 1
          FROM borrow_transactions
          WHERE member_id = {int(member_id)}
            AND status = 'ISSUED'
      );
    """

    if execute_query(sql) is not None:
        print("Member deactivation command completed.")
        print("Members with active borrowed books cannot be deactivated.")
