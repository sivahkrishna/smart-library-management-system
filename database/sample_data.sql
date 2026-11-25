
USE smart_library;

INSERT INTO books
(title, author, isbn, category, total_copies, available_copies)
VALUES
('Python Programming', 'John Zelle', '9781590282755', 'Programming', 5, 5),
('Clean Code', 'Robert C. Martin', '9780132350884', 'Programming', 3, 3),
('Database System Concepts', 'Abraham Silberschatz', '9780073523323', 'Database', 4, 4),
('Artificial Intelligence', 'Stuart Russell', '9780134610993', 'AI', 2, 2),
('The Pragmatic Programmer', 'David Thomas', '9780135957059', 'Programming', 3, 3);

INSERT INTO members
(name, email, phone, joined_date)
VALUES
('Arun Kumar', 'arun@example.com', '9876543210', CURDATE()),
('Rahul Raj', 'rahul@example.com', '9876543211', CURDATE()),
('Anjali P', 'anjali@example.com', '9876543212', CURDATE());

INSERT INTO staff (name, username, role)
VALUES
('Library Admin', 'admin', 'ADMIN');

SELECT * FROM books;
SELECT * FROM members;
