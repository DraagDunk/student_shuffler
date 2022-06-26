import tkinter as tk
from tkinter import END, VERTICAL, ttk, filedialog

from random import random, shuffle

from frames.utils import tup_split, student_list_to_str, divide_groups, remove_indices


class InputFrame(ttk.Frame):

    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)

        # Configure
        self.configure(padding=10)

        # Defining variables
        self.student_list = []
        self.student_list_var = tk.StringVar(value=self.student_list)
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
        self.create_groups_frame = CreateGroupsFrame(
            self, borderwidth=2, relief="groove")

        self.student_listbox = tk.Listbox(
            self.list_frame, height=20, width=40, listvariable=self.student_list_var, selectmode="extended")
        student_list_scrollbar = tk.Scrollbar(self.list_frame, orient=VERTICAL)
        self.student_listbox.configure(
            yscrollcommand=student_list_scrollbar.set)
        student_list_scrollbar.config(command=self.student_listbox.yview)
        load_button = ttk.Button(
            self.list_frame, text="Indlæs liste", command=self.load_students)
        save_button = ttk.Button(
            self.list_frame, text="Gem liste", command=self.save_students)

        add_student_button = ttk.Button(
            self.add_new_student_frame, text="Tilføj elev", command=self.add_student)
        rem_student_button = ttk.Button(
            self.add_new_student_frame, text="Fjern elev", command=self.remove_student)

        # Assign widgets to grid
        self.list_frame.grid(row=0, column=0, rowspan=2)
        self.student_listbox.grid(row=0, column=0, columnspan=2)
        student_list_scrollbar.grid(row=0, column=2, sticky="NS")
        load_button.grid(row=1, column=0, sticky="EW")
        save_button.grid(row=1, column=1, sticky="EW")

        self.add_new_student_frame.grid(row=0, column=1, sticky="NSEW")
        self.create_groups_frame.grid(row=1, column=1, sticky="NSEW")

        add_student_button.grid(row=2, column=1, sticky="NSEW")
        rem_student_button.grid(row=2, column=0, sticky="NSEW")

    def load_students(self, *args):
        """Load a text file into the student list."""

        self.student_list = []

        # Import data and but it into a list.
        path = filedialog.askopenfilename(
            initialdir=".",
            title="Vælg liste over elever",
            filetypes=(("Text files", "*.txt*"),)
        )

        if path:
            file = open(path, "r")
            student_list = file.read().split("\n")

            # Clean the list up a bit.
            for i, student in sorted(enumerate(student_list), reverse=True):
                if student == "":
                    _ = student_list.pop(i)

            # Register the students to the list.
            for student in student_list:
                student.replace(",", ";")
                self.add_student(student=student)
        else:
            # print("No filename provided, cancelling.")
            return

    def save_students(self, *args, **kwargs):
        """Save the list of students to a text file."""

        file = filedialog.asksaveasfile(
            mode="w",
            initialdir=".",
            title="Gem liste af elever",
            defaultextension=".txt",
            filetypes=(("Text files", "*.txt"),)
        )
        if file:
            save_string = student_list_to_str(self.student_list)
            file.write(save_string)
            file.close()
        else:
            # print("No filename provided, cancelling.")
            return

    def add_student(self, *args, **kwargs):
        """Add new student with data from the add_new_student_frame."""
        if "student" in kwargs.keys():
            new_student_string = kwargs["student"]
            new_student_tup = tup_split(new_student_string)
            new_student_name = new_student_tup[0]
            new_student_gender = new_student_tup[1]
        else:
            new_student_name = self.add_new_student_frame.new_student_var.get()
            new_student_gender = self.add_new_student_frame.student_gender_entry.gender_var.get()
            new_student_tup = (new_student_name, new_student_gender)
        self.student_list.append(new_student_tup)
        student_name_list = [tup[0] for tup in self.student_list]
        self.student_list_var.set(value=student_name_list)
        self.student_listbox.selection_clear(0, END)
        self.student_listbox.selection_set(END, END)
        self.student_listbox.yview_moveto(1)

    def remove_student(self, *args, **kwargs):
        """Remove the chosen student from the student list."""
        chosen_student_ind = list(self.student_listbox.curselection())
        self.student_list = remove_indices(
            self.student_list, chosen_student_ind)
        self.student_list_var.set([student[0]
                                  for student in self.student_list])
        self.student_listbox.selection_clear(0, END)

    def create_groups(self, *args):
        """Create groups and save them in the groups variable."""
        # Clear existing groups
        self.groups = {}

        temp_student_list = [student for student in self.student_list]
        shuffle(temp_student_list)
        if bool(self.create_groups_frame.divide_gender_var.get()):
            male_list = []
            female_list = []
            other_list = []
            for student in temp_student_list:
                name, gender = student
                if gender in ("mand", "m", "male", "dreng"):
                    male_list.append(name)
                elif gender in ("kvinde", "k", "female", "f", "pige"):
                    female_list.append(name)
                else:
                    other_list.append(name)

            for other_name in other_list:
                roll = random()
                if roll >= 0.5:
                    male_list.append(other_name)
                else:
                    female_list.append(other_name)

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
            full_list = [student[0]
                         for student in temp_student_list]
            self.groups = divide_groups(
                full_list,
                int(self.create_groups_frame.num_groups_var.get()),
                int(self.create_groups_frame.num_students_var.get())
            )


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
        student_name_entry = ttk.Entry(
            self, textvariable=self.new_student_var)
        self.student_gender_entry = StudentGenderSelection(self)

        # Assigning widgets to grid
        student_name_label.grid(row=0, column=0, padx=(0, 5))
        student_name_entry.grid(row=0, column=1)
        self.student_gender_entry.grid(row=1, column=0, columnspan=2)


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
