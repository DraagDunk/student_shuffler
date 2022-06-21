import tkinter as tk
from tkinter import ttk
from random import shuffle
from random import random


def tup_split(string: str) -> tuple:
    lst = string.split(";")
    return (lst[0], lst[1])


def divide_groups(lst: list, num_g: int, num_s: int) -> dict:
    grp_dict = {}
    num_groups = num_g if num_g else len(lst)//num_s
    for i, name in enumerate(lst):
        grp_num = i % num_groups
        if str(grp_num+1) in grp_dict.keys():
            grp_dict[str(grp_num+1)].append(name)
        else:
            grp_dict[str(grp_num+1)] = [name]
    return grp_dict


def increment_rows(curr_row, curr_col, max_rows=20):
    new_row = curr_row + 1
    if new_row > 20:
        new_col = curr_col + 1
    else:
        new_col = curr_col
    return new_row, new_col


class MainWindow(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Elevblender")

        self.out_frame = OutputFrame(self)

        self.in_frame = InputFrame(self)
        self.in_frame.grid(row=0, column=0)

        create_button = ttk.Button(
            self.in_frame.create_groups_frame, text="Lav grupper", command=self.create_groups)
        create_button.grid(row=7, column=1, columnspan=2)

    def create_groups(self):
        """Create group and move to group display frame."""
        self.in_frame.create_groups()
        self.out_frame.display_groups(self.in_frame.groups)
        self.out_frame.grid(row=0, column=0)
        self.in_frame.grid_forget()


class InputFrame(ttk.Frame):

    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)

        # Defining variables
        self.student_list = ["Lars;mand", "Frank;mand",
                             "Kasper;mand", "Mads;mand",
                             "Lone;kvinde", "Jesper;mand",
                             "Klara;kvinde", "Frede;mand",
                             "Frederikke;kvinde"]
        self.student_list_var = tk.StringVar(value=self.student_list)
        self.groups = {}

        # Create widgets
        student_list = tk.Listbox(
            self, height=20, width=30, listvariable=self.student_list_var)
        load_button = ttk.Button(
            self, text="Indlæs liste", command=self.load_students)
        self.add_new_student_frame = AddNewStudentFrame(
            self, borderwidth=2, relief="groove")
        self.create_groups_frame = CreateGroupsFrame(
            self, borderwidth=2, relief="groove")

        add_student_button = ttk.Button(
            self.add_new_student_frame, text="Tilføj elev", command=self.add_student)

        # Assign widgets to grid
        student_list.grid(row=0, column=0, rowspan=2)
        load_button.grid(row=2, column=0, sticky="EW")
        self.add_new_student_frame.grid(row=0, column=1, sticky="NSEW")
        self.create_groups_frame.grid(row=1, column=1, sticky="NSEW")

        add_student_button.grid(row=3, column=1, columnspan=2)

    def load_students(self, *args):
        pass

    def add_student(self, *args):
        """Add new student with data from the add_new_student_frame."""
        new_student_string = f"{self.add_new_student_frame.new_student_var.get()};" +\
            f"{self.add_new_student_frame.student_gender_entry.gender_var.get()}"
        self.student_list.append(new_student_string)
        self.student_list_var.set(value=self.student_list)

    def create_groups(self, *args):
        """Create groups and save them in the groups variable."""
        temp_student_list = [student for student in self.student_list]
        shuffle(temp_student_list)
        if bool(self.create_groups_frame.divide_gender_var.get()):
            male_list = []
            female_list = []
            other_list = []
            for student in temp_student_list:
                name, gender = tup_split(student)
                if gender == "mand":
                    male_list.append(name)
                elif gender == "kvinde":
                    female_list.append(name)
                else:
                    other_list.append(name)

            for other_name in other_list:
                roll = random()
                if roll >= 0.5:
                    male_list.append(other_name)
                else:
                    female_list.append(other_name)

            print(male_list)
            print(female_list)
            m_ratio = len(male_list)/(len(male_list)+len(female_list))
            f_ratio = len(female_list)/(len(male_list)+len(female_list))
            male_groups = divide_groups(
                male_list,
                round(int(self.create_groups_frame.num_groups_var.get()) * m_ratio),
                int(self.create_groups_frame.num_students_var.get())
            )
            female_groups = divide_groups(
                female_list,
                round(int(self.create_groups_frame.num_groups_var.get()) * f_ratio),
                int(self.create_groups_frame.num_students_var.get())
            )
            for key in male_groups.keys():
                self.groups[f"{key}m"] = male_groups[key]
            for key in female_groups.keys():
                self.groups[f"{key}f"] = female_groups[key]

        else:
            full_list = [tup_split(student)[0]
                         for student in temp_student_list]
            self.groups = divide_groups(
                full_list,
                int(self.create_groups_frame.num_groups_var.get()),
                int(self.create_groups_frame.num_students_var.get())
            )


class AddNewStudentFrame(ttk.Frame):

    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        # Defining variables
        self.new_student_var = tk.StringVar()

        # Creating widgets
        student_name_label = ttk.Label(self, text="Navn på ny elev:")
        student_name_entry = ttk.Entry(self, textvariable=self.new_student_var)
        self.student_gender_entry = StudentGenderSelection(self)

        # Assigning widgets to grid
        student_name_label.grid(row=1, column=1)
        student_name_entry.grid(row=1, column=2)
        self.student_gender_entry.grid(row=2, column=1, columnspan=2)


class CreateGroupsFrame(ttk.Frame):

    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        # Defining variables
        self.num_students_var = tk.StringVar(value=0)
        self.num_groups_var = tk.StringVar(value=0)
        self.divide_gender_var = tk.BooleanVar(value=False)

        # Creating widgets
        num_students_label = ttk.Label(self, text="Elever per gruppe")
        num_students_spin = ttk.Spinbox(
            self, textvariable=self.num_students_var, width=2, from_=0, to=5)
        num_groups_label = ttk.Label(self, text="Antal grupper")
        num_groups_spin = ttk.Spinbox(
            self, textvariable=self.num_groups_var, width=2, from_=0, to=10)
        divide_gender_check = ttk.Checkbutton(
            self, text="Kønsopdeling", variable=self.divide_gender_var)

        # Assigning widgets to grid
        num_students_label.grid(row=4, column=1)
        num_students_spin.grid(row=5, column=1)
        num_groups_label.grid(row=4, column=2)
        num_groups_spin.grid(row=5, column=2)
        divide_gender_check.grid(row=6, column=1)


class StudentGenderSelection(ttk.Frame):

    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        self.gender_var = tk.StringVar(value="andet")

        male_option = ttk.Radiobutton(
            self,
            text="Mand",
            variable=self.gender_var,
            value="mand"
        )
        female_option = ttk.Radiobutton(
            self,
            text="Kvinde",
            variable=self.gender_var,
            value="kvinde"
        )
        other_option = ttk.Radiobutton(
            self,
            text="Andet",
            variable=self.gender_var,
            value="andet"
        )
        male_option.grid(row=0, column=0)
        female_option.grid(row=0, column=1)
        other_option.grid(row=0, column=2)


class OutputFrame(ttk.Frame):

    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        self.title_label = ttk.Label(self, text="Grupper")
        self.title_label.grid(row=0, column=0)

    def display_groups(self, groups):
        curr_row = 0
        curr_col = 0
        for group_num in groups.keys():
            group_num_label = ttk.Label(self, text=f"Gruppe {group_num}")
            curr_row, curr_col = increment_rows(
                curr_row, curr_col, max_rows=20)
            group_num_label.grid(row=curr_row, column=curr_col, sticky="W")
            for name in groups[group_num]:
                name_label = ttk.Label(self, text=f" - {name}")
                curr_row += 1
                name_label.grid(row=curr_row, column=curr_col, sticky="W")


root = MainWindow()

root.mainloop()
