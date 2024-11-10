import tkinter as tk
from tkinter import ttk, filedialog

from frames.utils import increment, groups_to_str

from models.models import Group


class OutputFrame(ttk.Frame):

    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        self.groups = {}

        # Create widgets
        self.title_label = ttk.Label(self, text="Grupper")
        self.save_button = ttk.Button(
            self, text="Gem grupper", command=self.save_groups)

        # Create frames
        self.groups_frame = GroupsFrame(
            self, borderwidth=2, relief="groove", padding=10)

        # Assigning widgets and frames to grid
        self.title_label.grid(row=0, column=0, columnspan=2)
        self.groups_frame.grid(row=1, column=0, columnspan=2, sticky="NSEW")
        self.save_button.grid(row=2, column=1, sticky="EW")

    def display_groups(self, groups: dict):

        self.groups = groups

        for widget in self.groups_frame.winfo_children():
            widget.destroy()

        curr_row = 0
        curr_col = 0
        for group in groups:
            group_frame = GroupFrame(
                self.groups_frame, group=group)
            group_frame.grid(row=curr_row, column=curr_col, sticky="NW")
            curr_row, curr_col = increment(
                curr_row, curr_col, max=5, mode="col")

    def save_groups(self):
        """Save the list of groups to a text file."""

        file = filedialog.asksaveasfile(
            mode="w",
            initialdir=".",
            title="Gem liste af grupper",
            defaultextension=".txt",
            filetypes=(("Text files", "*.txt"),)
        )
        if file:
            save_string = groups_to_str(self.groups)
            file.write(save_string)
            file.close()
        else:
            print("No filename provided, cancelling.")
            return


class GroupsFrame(ttk.Frame):
    pass


class GroupFrame(ttk.Frame):

    def __init__(self, container, group: Group, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        self.configure(padding=10)

        group_num_label = ttk.Label(
            self, text=group.name)
        group_num_label.grid(
            row=0, column=0, sticky="W")
        curr_row = 0
        for student in group.students:
            name_label = ttk.Label(self, text=f" - {student}")
            curr_row += 1
            name_label.grid(row=curr_row, column=0,
                            sticky="W")
