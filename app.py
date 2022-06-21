from email.policy import default
import tkinter as tk
from tkinter import Variable, ttk


class MainWindow(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Elevblender")

        frame = InputFrame(self)
        frame.grid()


class InputFrame(ttk.Frame):

    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)

        # Defining variables
        self.student_list_var = tk.StringVar()

        # Create widgets
        student_list = tk.Listbox(
            self, height=20, width=30, listvariable=self.student_list_var)
        load_button = ttk.Button(
            self, text="Indlæs liste", command=self.load_students)
        add_new_student_frame = AddNewStudentFrame(
            self, borderwidth=2, relief="groove")
        create_groups_frame = CreateGroupsFrame(
            self, borderwidth=2, relief="groove")

        # Assign widgets to grid
        student_list.grid(row=0, column=0, rowspan=2)
        load_button.grid(row=2, column=0, sticky="EW")
        add_new_student_frame.grid(row=0, column=1, sticky="NSEW")
        create_groups_frame.grid(row=1, column=1, sticky="NSEW")

    def load_students(self, *args):
        pass


class AddNewStudentFrame(ttk.Frame):

    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        # Defining variables
        self.new_student_var = tk.StringVar()

        # Creating widgets
        student_name_label = ttk.Label(self, text="Navn på ny elev:")
        student_name_entry = ttk.Entry(self, textvariable=self.new_student_var)
        student_gender_entry = StudentGenderSelection(self)
        add_student_button = ttk.Button(
            self, text="Tilføj elev", command=self.add_student)

        # Assigning widgets to grid
        student_name_label.grid(row=1, column=1)
        student_name_entry.grid(row=1, column=2)
        student_gender_entry.grid(row=2, column=1, columnspan=2)
        add_student_button.grid(row=3, column=1, columnspan=2)

    def add_student(self, *args):
        pass


class CreateGroupsFrame(ttk.Frame):

    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        # Defining variables
        self.num_students_var = tk.StringVar(value=2)
        self.num_groups_var = tk.StringVar(value=1)
        self.divide_gender_var = tk.BooleanVar(value=False)

        # Creating widgets
        num_students_label = ttk.Label(self, text="Elever per gruppe")
        num_students_spin = ttk.Spinbox(
            self, textvariable=self.num_students_var, width=2)
        num_groups_label = ttk.Label(self, text="Antal grupper")
        num_groups_spin = ttk.Spinbox(
            self, textvariable=self.num_groups_var, width=2)
        divide_gender_check = ttk.Checkbutton(
            self, text="Kønsopdeling", variable=self.divide_gender_var)
        create_button = ttk.Button(
            self, text="Lav grupper", command=self.create_groups)

        # Assigning widgets to grid
        num_students_label.grid(row=4, column=1)
        num_students_spin.grid(row=5, column=1)
        num_groups_label.grid(row=4, column=2)
        num_groups_spin.grid(row=5, column=2)
        divide_gender_check.grid(row=6, column=1)
        create_button.grid(row=7, column=1, columnspan=2)

    def create_groups(self, *args):
        pass


class StudentGenderSelection(ttk.Frame):

    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        self.gender_var = tk.StringVar(value="other")

        male_option = ttk.Radiobutton(
            self,
            text="Mand",
            variable=self.gender_var,
            value="male"
        )
        female_option = ttk.Radiobutton(
            self,
            text="Kvinde",
            variable=self.gender_var,
            value="female"
        )
        other_option = ttk.Radiobutton(
            self,
            text="Andet",
            variable=self.gender_var,
            value="other"
        )
        male_option.grid(row=0, column=0)
        female_option.grid(row=0, column=1)
        other_option.grid(row=0, column=2)


root = MainWindow()

root.mainloop()
