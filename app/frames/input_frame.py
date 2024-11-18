import json

import tkinter as tk
from tkinter import END, VERTICAL, ttk, filedialog

from random import random, shuffle

from frames.utils import divide_groups

from models.models import ClassRoom, Student


class InputFrame(ttk.Frame):

    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)

        # Configure
        self.configure(padding=10)

        # Defining variables
        self.classroom = ClassRoom()
        self.classroom_var = tk.StringVar(value=self.classroom.students)
        self.groups = {}

        # Create list frame
        self.list_frame = ttk.Frame(self)
        self.list_frame.rowconfigure(0, weight=1)
        self.list_frame.rowconfigure(1, weight=0)
        self.list_frame.columnconfigure(0, weight=1)
        self.list_frame.columnconfigure(1, weight=1)
        self.list_frame.columnconfigure(2, weight=0)

        # Create widgets
        self.add_new_student_frame = AddNewStudentFrame(
            self, borderwidth=2, relief="groove")
        self.edit_student_frame = EditStudentFrame(
            self, borderwidth=2, relief="groove")
        self.create_groups_frame = CreateGroupsFrame(
            self, borderwidth=2, relief="groove")

        # Box with a list of students in classroom ...
        self.classroombox = tk.Listbox(
            self.list_frame, height=20, width=40, listvariable=self.classroom_var, selectmode="extended")
        # ... with a vertical scrollbar ...
        classroom_scrollbar = tk.Scrollbar(self.list_frame, orient=VERTICAL)
        self.classroombox.configure(
            yscrollcommand=classroom_scrollbar.set)
        classroom_scrollbar.config(command=self.classroombox.yview)
        # ... where you edit students by double clicking them ...
        self.classroombox.bind("<Double-Button-1>", self.edit_student)
        # ... and a load button ...
        load_button = ttk.Button(
            self.list_frame, text="Indlæs liste", command=self.load_students)
        # ... and a save button.
        save_button = ttk.Button(
            self.list_frame, text="Gem liste", command=self.save_students)

        add_student_button = ttk.Button(
            self.add_new_student_frame, text="Tilføj elev", command=self.add_student)
        rem_student_button = ttk.Button(
            self.add_new_student_frame, text="Fjern elev", command=self.remove_student)

        # Assign widgets to grid
        self.list_frame.grid(row=0, column=0, rowspan=2)
        self.classroombox.grid(row=0, column=0, columnspan=2)
        classroom_scrollbar.grid(row=0, column=2, sticky="NS")
        load_button.grid(row=1, column=0, sticky="EW")
        save_button.grid(row=1, column=1, sticky="EW")

        self.add_new_student_frame.grid(row=0, column=1, sticky="NSEW")
        self.create_groups_frame.grid(row=1, column=1, sticky="NSEW")

        add_student_button.grid(row=2, column=1, sticky="NSEW")
        rem_student_button.grid(row=2, column=0, sticky="NSEW")

    def load_students(self, *args):
        """Load a json file into the student list."""

        # Import data and put it into a list.
        path = filedialog.askopenfilename(
            initialdir=".",
            title="Vælg liste over elever",
            filetypes=(("JSON files", "*.json*"),)
        )

        if path:
            with open(path, "r") as file:
                cr_json = json.load(file)

            self.classroom = ClassRoom.from_json_object(cr_json)
            self.classroom_var.set(self.classroom.students)
        else:
            print("No filename provided, cancelling.")
            return

    def save_students(self, *args, **kwargs):
        """Save the list of students to a json file."""

        file = filedialog.asksaveasfile(
            mode="w",
            initialdir=".",
            title="Gem liste af elever",
            defaultextension=".json",
            filetypes=(("JSON files", "*.json"),)
        )
        if file:
            cr_json = self.classroom.to_json_object()
            json.dump(cr_json, file)
            file.close()
        else:
            print("No filename provided, cancelling.")
            return

    def add_student(self, *args, **kwargs):
        """Add new student with data from the add_new_student_frame."""

        # Add a student given by the "create_groups"-method.
        if "student" in kwargs.keys():
            new_student_string = kwargs["student"]
            new_student_tup = new_student_string.split(";")
            new_student_name = new_student_tup[0]
            new_student_gender = new_student_tup[1]

        # Add a student from the "new_student_var"-field.
        else:
            new_student_name = self.add_new_student_frame.new_student_var.get()
            new_student_gender = self.add_new_student_frame.student_gender_entry.gender_var.get()
            new_student = Student(new_student_name, new_student_gender)

        # Throw away student if no name was provided.
        if not new_student_name or not new_student_gender:
            print(
                f"No student name and/or gender provided for {new_student_name or 'none'}"
                f" ({new_student_gender or 'none'}), skipping.")
            return

        # Add the student to the classroom.
        self.classroom.add_student(new_student)
        self.classroom_var.set(self.classroom.students)

        # Set the selection to the new student, and scroll list to the bottom.
        self.classroombox.selection_clear(0, END)
        self.classroombox.selection_set(END, END)
        self.classroombox.yview_moveto(1)

        # Clear the variable and focus on the field again.
        self.add_new_student_frame.new_student_var.set("")
        self.add_new_student_frame.student_name_entry.focus()

    def edit_student(self, *args, **kwargs):
        student = self.classroom.students[self.classroombox.curselection()[0]]
        self.go_to_edit_frame()
        self.edit_student_frame.load_student(student)

    def remove_student(self, *args, **kwargs):
        """Remove the chosen student from the student list."""
        chosen_student = self.classroom.students[self.classroombox.curselection(
        )[0]]
        self.classroom.remove_student(chosen_student)
        self.classroom_var.set(self.classroom.students)
        self.classroombox.selection_clear(0, END)

    def create_groups(self, *args):
        """Create groups and save them in the groups variable."""
        # Clear existing groups

        temp_classroom = [student for student in self.classroom.students]
        shuffle(temp_classroom)
        if bool(self.create_groups_frame.divide_gender_var.get()):
            print("HERE")
            male_list = []
            female_list = []
            other_list = []
            for student in temp_classroom:
                if student.is_male:
                    male_list.append(student)
                elif student.is_female:
                    female_list.append(student)
                else:
                    other_list.append(student)

            for other_st in other_list:
                roll = random()
                if roll >= 0.5:
                    male_list.append(other_st)
                else:
                    female_list.append(other_st)

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
            print("male_groups:", male_groups)
            print("female_groups:", female_groups)

            for group in male_groups:
                group.name += "m"
            for group in female_groups:
                group.name += "f"

            self.groups = male_groups + female_groups

        else:
            self.groups = divide_groups(
                temp_classroom,
                int(self.create_groups_frame.num_groups_var.get()),
                int(self.create_groups_frame.num_students_var.get())
            )

    def go_to_edit_frame(self):
        """Switches the add-frame to the edit frame."""
        self.edit_student_frame.grid(row=0, column=1, sticky="NSEW")
        self.add_new_student_frame.grid_forget()

    def go_to_add_frame(self):
        """Switches the edit-frame to the add-frame."""
        self.add_new_student_frame.grid(row=0, column=1, sticky="NSEW")
        self.edit_student_frame.grid_forget()


class AddNewStudentFrame(ttk.Frame):

    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        # Configure frame
        self.configure(padding=10)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Defining variables
        self.new_student_var = tk.StringVar()

        # Creating widgets
        student_name_label = ttk.Label(
            self, text="Navn på ny elev:")
        self.student_name_entry = ttk.Entry(
            self, textvariable=self.new_student_var)
        self.student_gender_entry = StudentGenderSelection(self)

        # Assigning widgets to grid
        student_name_label.grid(row=0, column=0, padx=(0, 5))
        self.student_name_entry.grid(row=0, column=1)
        self.student_gender_entry.grid(row=1, column=0, columnspan=2)


class EditStudentFrame(ttk.Frame):

    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        # Configure frame
        self.configure(padding=10)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Defining variables
        self.student_var = tk.StringVar()

        # Creating widgets
        student_name_label = ttk.Label(
            self, text="Navn på ny elev:")
        self.student_name_entry = ttk.Entry(
            self, textvariable=self.student_var)
        self.student_gender_entry = StudentGenderSelection(self)

        # Assigning widgets to grid
        student_name_label.grid(row=0, column=0, padx=(0, 5))
        self.student_name_entry.grid(row=0, column=1)
        self.student_gender_entry.grid(row=1, column=0, columnspan=2)

    def load_student(student: str):


class CreateGroupsFrame(ttk.Frame):

    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        # Configure
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.configure(padding=10)

        # Defining variables
        self.num_students_var = tk.StringVar(value=3)
        self.num_groups_var = tk.StringVar(value=0)
        self.divide_gender_var = tk.BooleanVar(value=False)

        # Create frames
        self.num_students_frame = ttk.Frame(self)
        self.num_groups_frame = ttk.Frame(self)

        # Creating widgets
        num_students_label = ttk.Label(
            self.num_students_frame,
            text="Elever per gruppe"
        )
        num_students_spin = ttk.Spinbox(
            self.num_students_frame,
            textvariable=self.num_students_var,
            width=2,
            from_=0, to=5
        )
        num_groups_label = ttk.Label(
            self.num_groups_frame,
            text="Antal grupper"
        )
        num_groups_spin = ttk.Spinbox(
            self.num_groups_frame,
            textvariable=self.num_groups_var,
            width=2,
            from_=0, to=10
        )
        divide_gender_check = ttk.Checkbutton(
            self,
            text="Kønsopdeling",
            variable=self.divide_gender_var
        )

        # Assigning widgets to grid in frames
        num_students_label.grid(row=4, column=1, sticky="EW")
        num_students_spin.grid(row=5, column=1)
        num_groups_label.grid(row=4, column=2, sticky="EW")
        num_groups_spin.grid(row=5, column=2)

        # Assigning frames and widget to grid
        self.num_students_frame.grid(row=0, column=0)
        self.num_groups_frame.grid(row=0, column=1)
        divide_gender_check.grid(row=1, column=0, columnspan=2)


class StudentGenderSelection(ttk.Frame):

    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        self.gender_var = tk.StringVar(value="o")

        male_option = ttk.Radiobutton(
            self,
            text="Mand",
            variable=self.gender_var,
            value="m"
        )
        female_option = ttk.Radiobutton(
            self,
            text="Kvinde",
            variable=self.gender_var,
            value="f"
        )
        other_option = ttk.Radiobutton(
            self,
            text="Andet",
            variable=self.gender_var,
            value="o"
        )
        male_option.grid(row=0, column=0)
        female_option.grid(row=0, column=1)
        other_option.grid(row=0, column=2)
