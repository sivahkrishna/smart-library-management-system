
from books import (
    add_book,
    view_books,
    search_book,
    update_book,
    delete_book
)

from members import (
    add_member,
    view_members,
    search_member,
    deactivate_member
)

from circulation import (
    issue_book,
    return_book,
    renew_book
)

from fines import (
    calculate_fines,
    record_fines,
    view_fines,
    pay_fine
)

from reports import (
    library_statistics,
    most_borrowed_books,
    member_borrowing_report
)

from threading_tasks import (
    start_overdue_monitor,
    start_report_thread,
    start_backup_thread,
    run_concurrency_test,
    stop_background_tasks
)


def book_menu():

    while True:
        print("\n===== BOOK MANAGEMENT =====")
        print("1. Add Book")
        print("2. View All Books")
        print("3. Search Book")
        print("4. Update Book")
        print("5. Delete Book")
        print("0. Back")

        choice = input("Enter choice: ")

        if choice == "1":
            add_book()

        elif choice == "2":
            view_books()

        elif choice == "3":
            search_book()

        elif choice == "4":
            update_book()

        elif choice == "5":
            delete_book()

        elif choice == "0":
            break

        else:
            print("Invalid choice.")


def member_menu():

    while True:
        print("\n===== MEMBER MANAGEMENT =====")
        print("1. Register Member")
        print("2. View Members")
        print("3. Search Member")
        print("4. Deactivate Member")
        print("0. Back")

        choice = input("Enter choice: ")

        if choice == "1":
            add_member()

        elif choice == "2":
            view_members()

        elif choice == "3":
            search_member()

        elif choice == "4":
            deactivate_member()

        elif choice == "0":
            break

        else:
            print("Invalid choice.")


def circulation_menu():

    while True:
        print("\n===== BOOK CIRCULATION =====")
        print("1. Issue Book")
        print("2. Return Book")
        print("3. Renew Book")
        print("0. Back")

        choice = input("Enter choice: ")

        if choice == "1":
            issue_book()

        elif choice == "2":
            return_book()

        elif choice == "3":
            renew_book()

        elif choice == "0":
            break

        else:
            print("Invalid choice.")


def fine_menu():

    while True:
        print("\n===== FINE MANAGEMENT =====")
        print("1. Calculate Overdue Fines")
        print("2. Record Returned Book Fines")
        print("3. View Fine Records")
        print("4. Pay Fine")
        print("0. Back")

        choice = input("Enter choice: ")

        if choice == "1":
            calculate_fines()

        elif choice == "2":
            record_fines()

        elif choice == "3":
            view_fines()

        elif choice == "4":
            pay_fine()

        elif choice == "0":
            break

        else:
            print("Invalid choice.")


def report_menu():

    while True:
        print("\n===== LIBRARY REPORTS =====")
        print("1. Library Statistics")
        print("2. Most Borrowed Books")
        print("3. Member Borrowing Report")
        print("4. Generate Report in Background")
        print("0. Back")

        choice = input("Enter choice: ")

        if choice == "1":
            library_statistics()

        elif choice == "2":
            most_borrowed_books()

        elif choice == "3":
            member_borrowing_report()

        elif choice == "4":
            start_report_thread()

        elif choice == "0":
            break

        else:
            print("Invalid choice.")


def threading_menu():

    while True:
        print("\n===== THREADING OPERATIONS =====")
        print("1. Start Overdue Background Monitor")
        print("2. Generate Background Report")
        print("3. Database Backup")
        print("4. Concurrent Book Issue Test")
        print("0. Back")

        choice = input("Enter choice: ")

        if choice == "1":
            start_overdue_monitor()

        elif choice == "2":
            start_report_thread()

        elif choice == "3":
            start_backup_thread()

        elif choice == "4":
            run_concurrency_test()

        elif choice == "0":
            break

        else:
            print("Invalid choice.")


def main():

    print("\n====================================")
    print("   SMART LIBRARY MANAGEMENT SYSTEM")
    print("====================================")

    # Start background overdue monitoring
    start_overdue_monitor()

    try:
        while True:

            print("\n========== MAIN MENU ==========")
            print("1. Book Management")
            print("2. Member Management")
            print("3. Book Circulation")
            print("4. Fine Management")
            print("5. Library Reports")
            print("6. Threading Operations")
            print("0. Exit")

            choice = input("\nEnter your choice: ").strip()

            if choice == "1":
                book_menu()

            elif choice == "2":
                member_menu()

            elif choice == "3":
                circulation_menu()

            elif choice == "4":
                fine_menu()

            elif choice == "5":
                report_menu()

            elif choice == "6":
                threading_menu()

            elif choice == "0":
                print("Closing Library Management System...")
                break

            else:
                print("Invalid choice. Try again.")

    except KeyboardInterrupt:
        print("\nApplication interrupted.")

    finally:
        stop_background_tasks()
        print("Thank you for using Smart Library Management System.")


if __name__ == "__main__":
    main()
