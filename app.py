import tkinter as tk
from tkinter import ttk

from frames import InputFrame
from frames import OutputFrame


class MainWindow(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Elevblender")

        self.out_frame = OutputFrame(self)
        self.out_frame.grid(row=0, column=0, sticky="NSEW")

        back_button = ttk.Button(
            self.out_frame,
            text="← Tilbage",
            command=self.return_to_input
        )
        back_button.grid(row=2, column=0, sticky="EW")

        self.in_frame = InputFrame(self)
        self.in_frame.grid(row=0, column=0)

        create_button = ttk.Button(
            self.in_frame.create_groups_frame,
            text="Lav grupper",
            command=self.create_groups
        )
        create_button.grid(row=2, column=0, columnspan=2, sticky="NSEW")

    def create_groups(self):
        """Create group and move to group display frame."""
        self.in_frame.create_groups()
        self.out_frame.display_groups(self.in_frame.groups)
        self.go_to_output()

    def go_to_output(self):
        """Go to the output frame."""
        self.out_frame.tkraise()
        # self.out_frame.grid(row=0, column=0)
        # self.in_frame.grid_forget()

    def return_to_input(self):
        """Returns to the input frame."""
        self.in_frame.tkraise()
        # self.in_frame.grid(row=0, column=0)
        # self.out_frame.grid_forget()


root = MainWindow()

# Keybind functions


def handle_return(event):
    """Adds new student when return is pressed."""
    focus_is_add_new = root.focus_get(
    ) == root.in_frame.add_new_student_frame.student_name_entry

    if focus_is_add_new:
        root.in_frame.add_student()


def handle_tab(event):
    """Rotates selected gender when tab is pressed."""
    focus_is_add_new = root.focus_get(
    ) == root.in_frame.add_new_student_frame.student_name_entry

    if focus_is_add_new:
        curr_val = root.in_frame.add_new_student_frame.student_gender_entry.gender_var.get()
        choices = ["mand", "kvinde", "andet"]
        choice_index = [i for i in range(
            len(choices)) if choices[i] == curr_val][0]
        new_index = (choice_index + 1) % len(choices)
        root.in_frame.add_new_student_frame.student_gender_entry.gender_var.set(
            choices[new_index])
        root.in_frame.add_new_student_frame.student_name_entry.focus_set()


# Define keybinds
root.bind("<Return>", handle_return)

root.unbind_all("<<NextWindow>>")
root.bind("<Tab>", handle_tab)

root.mainloop()
