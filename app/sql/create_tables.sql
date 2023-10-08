DROP TABLE IF EXISTS Marks;
DROP TABLE IF EXISTS Subject_Teacher;
DROP TABLE IF EXISTS Students;
DROP TABLE IF EXISTS Teacher;
DROP TABLE IF EXISTS Subjects;
DROP TABLE IF EXISTS Groups;

CREATE TABLE Groups (
    group_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255)
);

CREATE TABLE Subjects (
    subject_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255)
);

CREATE TABLE Teacher (
    teacher_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    role ENUM('admin', 'user') DEFAULT 'admin',
    INDEX (role) 
);

CREATE TABLE Users (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    hashed_password VARCHAR(255),
    role ENUM('admin', 'user') DEFAULT 'user',
    user_type ENUM('teacher', 'student') DEFAULT 'student' 
);

CREATE TABLE Students (
    student_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    group_id INT UNSIGNED,
    FOREIGN KEY (group_id) REFERENCES Groups(group_id)
);


CREATE TABLE Subject_Teacher (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    subject_id INT UNSIGNED,
    teacher_id INT UNSIGNED,
    group_id INT UNSIGNED,
    FOREIGN KEY (subject_id) REFERENCES Subjects(subject_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (teacher_id) REFERENCES Teacher(teacher_id) ON DELETE CASCADE ON UPDATE CASCADE, 
    FOREIGN KEY (group_id) REFERENCES Groups(group_id) ON DELETE CASCADE ON UPDATE CASCADE,
    UNIQUE KEY unique_relationship (subject_id, teacher_id)
);


CREATE TABLE Marks (
    mark_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    student_id INT UNSIGNED,
    subject_id INT UNSIGNED,
    date DATETIME,
    mark INT,
    FOREIGN KEY (student_id) REFERENCES Students(student_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES Subjects(subject_id) ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX (date) 
);
