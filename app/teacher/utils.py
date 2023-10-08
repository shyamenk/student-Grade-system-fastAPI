def format_teachers_data(teacher):
    techers_list = []
    for teacher_data in teacher:
        teacher_dict = {
            "id": teacher_data[0],
            "name": teacher_data[1],
            "email": teacher_data[2],
        }
        techers_list.append(teacher_dict)

    return {"teachers": techers_list}
