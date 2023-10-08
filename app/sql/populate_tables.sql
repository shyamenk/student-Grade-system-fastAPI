INSERT INTO Groups (name) VALUES 
('Group A'),
('Group B'),
('Group C'),
('Group D'),
('Group E'),
('Group F'),
('Group G'),
('Group H'),
('Group I'),
('Group J');

INSERT INTO Subjects (title) VALUES 
('Mathematics'),
('Science'),
('History'),
('English'),
('Geography'),
('Computer Science'),
('Physics'),
('Chemistry'),
('Biology'),
('Music');

INSERT INTO Students (first_name, last_name, group_id) VALUES 
('John', 'Doe', 1),
('Jane', 'Smith', 2),
('Michael', 'Johnson', 3),
('Emily', 'Brown', 4),
('Daniel', 'Wilson', 5),
('Olivia', 'Davis', 6),
('William', 'Taylor', 7),
('Sofia', 'Anderson', 8),
('Ethan', 'Martinez', 9),
('Ava', 'Garcia', 10);

INSERT INTO Teacher (name, email) VALUES 
('Mr. Anderson', 'anderson@example.com'),
('Ms. Davis', 'davis@example.com'),
('Mr. Wilson', 'wilson@example.com'),
('Ms. Taylor', 'taylor@example.com'),
('Mr. Martinez', 'martinez@example.com'),
('Ms. Garcia', 'garcia@example.com'),
('Mr. Brown', 'brown@example.com'),
('Ms. Smith', 'smith@example.com'),
('Mr. Johnson', 'johnson@example.com'),
( 'Ms. Anderson', 'anderson2@example.com');

INSERT INTO Subject_Teacher (subject_id, teacher_id, group_id) VALUES 
(1, 1, 1),
(2, 2, 2),
(3, 3, 3),
(4, 4, 4),
(5, 5, 5),
(6, 6, 6),
(7, 7, 7),
(8, 8, 8),
(9, 9, 9),
(10, 10, 10);

INSERT INTO Marks (student_id, subject_id, date, mark) VALUES 
(1, 1, '2023-09-20', 90),
(1, 2, '2023-09-21', 85),
(2, 1, '2023-09-20', 75),
(2, 2, '2023-09-21', 80),
(3, 1, '2023-09-20', 95),
(3, 2, '2023-09-21', 70),
(4, 3, '2023-09-20', 65),
(4, 4, '2023-09-21', 88),
(5, 3, '2023-09-20', 92),
(5, 4, '2023-09-21', 78),
(6, 5, '2023-09-20', 85),
(6, 6, '2023-09-21', 90),
(7, 7, '2023-09-20', 70),
(7, 8, '2023-09-21', 85),
(8, 9, '2023-09-20', 95),
(8, 10, '2023-09-21', 80),
(9, 1, '2023-09-20', 75),
(9, 2, '2023-09-21', 85),
(10, 3, '2023-09-20', 88),
(10, 4, '2023-09-21', 95);
