def format_groups_data(groups):
    groups_list = []
    for group_data in groups:
        group_dict = {
            "group_id": group_data[0],
            "name": group_data[1],
        }
        groups_list.append(group_dict)

    return {"groups": groups_list}
