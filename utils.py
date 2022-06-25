def tup_split(string: str, delimiter: str = ";") -> tuple:
    lst = string.split(delimiter)
    return (lst[0], lst[1])


def student_list_to_str(student_list: list[tuple]) -> str:
    student_string = ""
    for student_tup in student_list:
        student_string += f"{student_tup[0]};{student_tup[1]}\n"
    return student_string


def group_dir_to_str(group_dir: dict) -> str:
    group_string = ""
    for key in group_dir.keys():
        group_string += f"Gruppe {key}\n"
        for student in group_dir[key]:
            group_string += f"- {student}\n"
        group_string += "\n"
    return group_string


def divide_groups(lst: list, num_g: int, num_s: int) -> dict:
    grp_dict = {}
    if num_g:
        num_groups = num_g
    elif num_s:
        num_groups = len(lst)//num_s
    else:
        print("No number of groups or number of students per group provided, defaulting to 1 group.")
        num_groups = 1

    for i, name in enumerate(lst):
        grp_num = i % num_groups
        if str(grp_num+1) in grp_dict.keys():
            grp_dict[str(grp_num+1)].append(name)
        else:
            grp_dict[str(grp_num+1)] = [name]
    return grp_dict


def increment(curr_row, curr_col, max=5, mode="col"):
    """Increment the row or column first, depending on the mode, then the other
    if the first exceeds the max."""

    if mode == "col":
        inc1 = curr_col
        inc2 = curr_row
    else:
        inc1 = curr_row
        inc2 = curr_col

    if inc1 >= max:
        inc1 = 0
        inc2 += 1
    else:
        inc1 += 1

    if mode == "col":
        return inc2, inc1
    else:
        return inc1, inc2
