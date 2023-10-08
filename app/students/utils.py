def format_students_data(students):
    students_list = []
    for student_data in students:
        student_dict = {
            "student_id": student_data[0],
            "first_name": student_data[1],
            "last_name": student_data[2],
            "group_id": student_data[3],
        }
        students_list.append(student_dict)

    return {"students": students_list}


def is_admin(auth: dict):
    role = auth["user"][4]
    if role == "admin":
        return True
    return False


def is_teacher(auth: dict):
    user_type = auth["user"][5]
    if user_type == "teacher":
        return True
    return False
