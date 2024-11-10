from models.models import Group

male_strings = ("mand", "m", "male", "dreng")
female_strings = ("kvinde", "k", "female", "f", "pige")


def student_list_to_str(student_list: list[tuple]) -> str:
    student_string = ""
    for student_tup in student_list:
        student_string += f"{student_tup[0]};{student_tup[1]}\n"
    return student_string


def groups_to_str(groups: list[Group]) -> str:
    group_string = ""
    for group in groups:
        group_string += group.to_txt()
    return group_string


def divide_groups(lst: list, num_g: int, num_s: int) -> dict:
    if num_g:
        num_groups = num_g
    elif num_s:
        num_groups = len(lst)//num_s
    else:
        print("No number of groups or number of students per group provided, defaulting to 1 group.")
        num_groups = 1

    groups = [Group(f"Gruppe {i+1}") for i in range(num_groups)]

    for i, student in enumerate(lst):
        grp_num = i % num_groups
        groups[grp_num].add_student(student)

    return groups


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
