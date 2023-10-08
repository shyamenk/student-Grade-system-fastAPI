def format_subjects_data(subjects):
    subjects_list = []
    for subject_data in subjects:
        subject_dict = {
            "subject_id": subject_data[0],
            "title": subject_data[1],
        }
        subjects_list.append(subject_dict)

    return {"subjects": subjects_list}
