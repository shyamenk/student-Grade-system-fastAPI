# Project Overview

This project is a FastAPI application that provides a RESTful API for managing student marks and related information. It includes CRUD operations for managing marks, students, groups, subjects, and their relationships. Additionally, it implements JWT for securing the API and includes Swagger documentation for easy API exploration.

# Setup and Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/shyamenk/Part-2-Backend.git
   ```

2. **Navigate to the project directory**:

   ```bash
   cd Part-2-Backend
   ```

3. **Rename `.env.local` to `.env` and add your environment variables**:

   ```env
   DB_HOST="********"
   DB_PORT="********"
   DB_USERNAME="******"
   DB_PASSWORD="*******"
   DB_NAME="************"
   ```

4. **Create a Virtual Environment** (Optional but recommended):

   ```bash
   python -m venv venv
   ```

   Activate the virtual environment:

   - On Windows:

     ```bash
     .\venv\Scripts\activate
     ```

   - On Linux:

     ```bash
     source venv/bin/activate
     ```

5. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

6. **Install MariaDB**:

Download and install MariaDB from the official website: [MariaDB Downloads](https://mariadb.org/download/)

Make sure to follow the installation instructions for your specific operating system.

2.  **Start the MariaDB Server**:

Once installed, start the MariaDB server. The exact process may vary depending on your operating system. You can usually start it from the command line or through a control panel.

For example, on Linux, you can start it using:

```sql
sudo systemctl start mariadb
```

On Windows, you can start it from the Start Menu.

3.  **Access the MariaDB Shell**:

Open a command prompt or terminal and enter the following command to access the MariaDB shell:

```css
mysql -u root -p
```

You'll be prompted to enter the root password you set during the installation.

4.  **Create a New Database**:

In the MariaDB shell, you can create a new database using the following command:

```sql
CREATE DATABASE your_database_name;
```

Replace `your_database_name` with the desired name for your database.

5.  **Create a User and Grant Privileges**:

It's a good practice to create a dedicated user for your database. This way, you can restrict access and only grant the necessary privileges.

```sql
CREATE USER 'your_username'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON your_database_name.* TO 'your_username'@'localhost';
FLUSH PRIVILEGES;
```

Replace `your_username` with the desired username and `your_password` with a strong password.

6.  **Run the SQL Scripts**:

    Run the following SQL scripts to create and populate the tables:

    - Create tables: Find the `create_tables.sql` in the app/sql folder and run the script in the MariaDB terminal or GUI.
    - Populate tables: Find the `populate_tables.sql` in the app/sql folder and run the script in the MariaDB terminal or GUI.

    Remember to replace the placeholders (`your_database_name`, `your_username`, `your_password`) with your actual choices.

Remember to replace the placeholders (`your_database_name`, `your_username`, `your_password`) with your actual choices.

7.  **Run the Application**:

    ```bash
    uvicorn app.main:app --reload
    ```

8.  **Access Swagger UI**:

    Open your web browser and go to:

    [http://localhost:8000/docs](http://localhost:8000/docs)

# Usage

Once the application is running, you can interact with the API using tools like Postman or by making HTTP requests directly.

1. **Create a User**

- Endpoint: `POST http://localhost:8000/v1/api/auth/register`

- Example Request Body:

  ```json
  {
    "name": "string",
    "email": "user@example.com",
    "password": "string",
    "role": "admin",
    "user_type": "teacher"
  }
  ```

2. **Login**

- Endpoint: `POST http://localhost:8000/v1/api/auth/token`

- Example Response:

  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzaHlhbWVua0BnbWFpbC5jb20iLCJpZCI6MSwiZXhwIjoxNjk0OTg5MjA2fQ.fbM3rpb9OWLFKN50FfCCEOLV-5ibdhyC0mdALNLldwE",
    "token_type": "bearer"
  }
  ```

3. **Access Routes**

Once you have obtained the access token, you can use it to access all the routes.

# API Endpoints and Functionalities

The API provides the following endpoints and functionalities:

1. **Auth**

- `POST /auth/register`: User registration
- `POST /auth/token`: Login for JWT Token
- `GET /auth/profile`: View Profile

2. **Marks**:

- `GET /marks`: Get a list of all marks.
- `GET /marks/{mark_id}`: Get details of a specific mark by ID.
- `POST /marks`: Add a new mark.
- `PUT /marks/{mark_id}`: Update an existing mark.
- `DELETE /marks/{mark_id}`: Delete a mark by ID.

3. **Students**:

- `GET /students`: Get a list of all students.
- `GET /students/{student_id}`: Get details of a specific student by ID.
- `POST /students`: Add a new student.
- `PUT /students/{student_id}`: Update an existing student.
- `DELETE /students/{student_id}`: Delete a student by ID.

4. **Groups**:

- `GET /groups`: Get a list of all groups.
- `GET /groups/{group_id}`: Get details of a specific group by ID.
- `POST /groups`: Add a new group.
- `PUT /groups/{group_id}`: Update an existing group.
- `DELETE /groups/{group_id}`: Delete a group by ID.

5. **Subjects**:

- `GET /subjects`: Get a list of all subjects.
- `GET /subjects/{subject_id}`: Get details of a specific subject by ID.
- `POST /subjects`: Add a new subject.
- `PUT /subjects/{subject_id}`: Update an existing subject.
- `DELETE /subjects/{subject_id}`: Delete a subject by ID.

6. **Subject/Teacher**:

- `GET /subject_teacher/add`: Add a subject-teacher relationship.
- `DELETE /subject_teacher.delete/{subject_id}/{teacher_id}`: Delete a subject-teacher relationship.

7. **Functional Requirements**:

- `GET /marks/student/{student_id}`: Get marks for a particular student ID.
- `GET /students/teacher/{teacher_id}`: Get the number of students for a particular teacher ID.
- `GET /marks/student/subject/{student_id}`: Get the list of marks in each subject for a particular student ID.
