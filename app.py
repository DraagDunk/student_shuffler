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
        self.num_students_var = tk.StringVar(value=2)
        self.new_student_var = tk.StringVar()
        self.num_groups_var = tk.StringVar(value=1)
        self.divide_gender_var = tk.BooleanVar(value=False)

        # Create widgets
        student_list = tk.Listbox(
            self, height=20, width=30, listvariable=self.student_list_var)
        load_button = ttk.Button(
            self, text="Indlæs liste", command=self.load_students)
        student_name_entry = ttk.Entry(self, textvariable=self.new_student_var)
        student_gender_entry = StudentGenderSelection(self)
        add_student_button = ttk.Button(
            self, text="Tilføj elev", command=self.add_student)
        num_students_label = ttk.Label(self, text="Elever per gruppe")
        num_students_spin = ttk.Spinbox(
            self, textvariable=self.num_students_var)
        num_groups_label = ttk.Label(self, text="Antal grupper")
        num_groups_spin = ttk.Spinbox(self, textvariable=self.num_groups_var)
        divide_gender_check = ttk.Checkbutton(
            self, text="Kønsopdeling", variable=self.divide_gender_var)
        create_button = ttk.Button(
            self, text="Lav grupper", command=self.create_groups)

        # Assign widgets to grid
        student_list.grid(row=0, column=0, rowspan=10)
        load_button.grid(row=0, column=1)
        student_name_entry.grid(row=1, column=1)
        student_gender_entry.grid(row=2, column=1)
        add_student_button.grid(row=3, column=1)
        num_students_label.grid(row=4, column=1)
        num_students_spin.grid(row=5, column=1)
        num_groups_label.grid(row=6, column=1)
        num_groups_spin.grid(row=7, column=1)
        divide_gender_check.grid(row=8, column=1)
        create_button.grid(row=9, column=1)

        for child in self.winfo_children():
            if not isinstance(child, tk.Listbox):
                child.grid_configure(padx=5, pady=5)

    def create_groups(self, *args):
        pass

    def load_students(self, *args):
        pass

    def add_student(self, *args):
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
