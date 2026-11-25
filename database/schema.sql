
CREATE DATABASE IF NOT EXISTS smart_library;

USE smart_library;

-- 1. Books table
CREATE TABLE IF NOT EXISTS books (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    author VARCHAR(100) NOT NULL,
    isbn VARCHAR(30) UNIQUE,
    category VARCHAR(80),
    total_copies INT NOT NULL DEFAULT 1,
    available_copies INT NOT NULL DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CHECK (total_copies >= 0),
    CHECK (available_copies >= 0),
    CHECK (available_copies <= total_copies)
);

-- 2. Members table
CREATE TABLE IF NOT EXISTS members (
    member_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE,
    phone VARCHAR(20),
    joined_date DATE NOT NULL,
    active BOOLEAN DEFAULT TRUE
);

-- 3. Borrow transactions table
CREATE TABLE IF NOT EXISTS borrow_transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT NOT NULL,
    member_id INT NOT NULL,
    issue_date DATE NOT NULL,
    due_date DATE NOT NULL,
    return_date DATE NULL,
    status ENUM('ISSUED', 'RETURNED') DEFAULT 'ISSUED',

    FOREIGN KEY (book_id)
        REFERENCES books(book_id),

    FOREIGN KEY (member_id)
        REFERENCES members(member_id)
);

-- 4. Fines table
CREATE TABLE IF NOT EXISTS fines (
    fine_id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_id INT NOT NULL UNIQUE,
    amount DECIMAL(10,2) NOT NULL DEFAULT 0,
    paid_amount DECIMAL(10,2) NOT NULL DEFAULT 0,
    payment_status ENUM('UNPAID', 'PARTIAL', 'PAID')
        DEFAULT 'UNPAID',

    FOREIGN KEY (transaction_id)
        REFERENCES borrow_transactions(transaction_id)
);

-- 5. Staff table
CREATE TABLE IF NOT EXISTS staff (
    staff_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    role VARCHAR(50) DEFAULT 'LIBRARIAN'
);

SHOW TABLES;
