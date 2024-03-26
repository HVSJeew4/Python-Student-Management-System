import tkinter as tk
from tkinter import ttk, messagebox

class StudentManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")

        # Variables to store student data
        self.students = []

        # Create a dark blue theme
        self.create_dark_blue_theme()

        # Create and configure the form
        self.create_form()

        # Create and configure the student table
        self.create_student_table()

    def create_dark_blue_theme(self):
        # Create a style object
        style = ttk.Style()

        # Configure the style with a dark blue theme
        style.theme_create("dark_blue", parent="alt", settings={
            "TFrame": {"configure": {"background": "#001f3f"}},
            "TLabel": {"configure": {"background": "#001f3f", "foreground": "#ffffff"}},
            "TButton": {"configure": {"background": "#0074cc", "foreground": "#ffffff"}, "map": {"background": [("active", "#005082")]}},
            "TEntry": {"configure": {"fieldbackground": "#ffffff"}},
            "Treeview": {"configure": {"background": "#001f3f", "foreground": "#ffffff"}},
        })

        # Set the theme
        style.theme_use("dark_blue")

    def create_form(self):
        # Create a frame for the form
        form_frame = ttk.Frame(self.root, padding="20", style="DarkBlue.TFrame")
        form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Create labels and entry widgets
        labels = ["ID", "Name", "Gender", "Age", "Enr-date", "Midterm", "Final", "GPA"]
        self.entries = {}
        for i, label in enumerate(labels):
            ttk.Label(form_frame, text=label + ":").grid(row=i, column=0, padx=5, pady=5, sticky="e")
            entry = ttk.Entry(form_frame, width=20)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="w")
            self.entries[label] = entry

        # Create buttons
        ttk.Button(form_frame, text="Add", command=self.add_student, style="DarkBlue.TButton").grid(row=len(labels), column=0, columnspan=2, pady=10)
        ttk.Button(form_frame, text="Update", command=self.update_student, style="DarkBlue.TButton").grid(row=len(labels) + 1, column=0, columnspan=2, pady=5)
        ttk.Button(form_frame, text="Delete", command=self.delete_student, style="DarkBlue.TButton").grid(row=len(labels) + 2, column=0, columnspan=2, pady=5)
        ttk.Button(form_frame, text="Clear", command=self.clear_form, style="DarkBlue.TButton").grid(row=len(labels) + 3, column=0, columnspan=2, pady=5)

    def create_student_table(self):
        # Create a frame for the student table
        table_frame = ttk.Frame(self.root, padding="20", style="DarkBlue.TFrame")
        table_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Create the student table
        columns = ["ID", "Name", "Gender", "Age", "Enr-date", "Midterm", "Final", "GPA"]
        self.student_table = ttk.Treeview(table_frame, columns=columns, show="headings", style="DarkBlue.Treeview")

        # Set column headings
        for col in columns:
            self.student_table.heading(col, text=col)
            self.student_table.column(col, width=100, anchor="center")  # Adjust width as needed

        self.student_table.pack(expand=True, fill="both")

        # Configure column weights to use available space
        for col in columns:
            table_frame.columnconfigure(columns.index(col), weight=1)

    def add_student(self):
        # Get data from entry widgets
        student_data = {label: entry.get() for label, entry in self.entries.items()}

        # Validate required fields
        if all(student_data.values()):
            # Add student to the list
            self.students.append(student_data)

            # Update the student table
            self.update_student_table()

            # Show success message
            messagebox.showinfo("Success", "Student added successfully!")

            # Clear the form
            self.clear_form()
        else:
            # Show error message for missing fields
            messagebox.showerror("Error", "Please enter all the details.")

    def update_student(self):
        # Get data from entry widgets
        student_data = {label: entry.get() for label, entry in self.entries.items()}

        # Validate required fields
        if student_data["ID"]:
            # Update student in the list
            for i, student in enumerate(self.students):
                if student["ID"] == student_data["ID"]:
                    self.students[i] = student_data

                    # Update the student table
                    self.update_student_table()

                    # Show success message
                    messagebox.showinfo("Success", "Student updated successfully!")

                    # Clear the form
                    self.clear_form()
                    return

            # Show error message if student ID not found
            messagebox.showerror("Error", "Student ID not found.")
        else:
            # Show error message for missing student ID
            messagebox.showerror("Error", "Please enter Student ID.")

    def delete_student(self):
        # Get student ID from the form
        student_id = self.entries["ID"].get()

        # Confirm deletion with a pop-up dialog
        confirm = messagebox.askyesno("Confirm Deletion", f"Do you really want to delete the student with ID {student_id}?")

        if confirm:
            # Remove student from the list
            self.students = [student for student in self.students if student["ID"] != student_id]

            # Update the student table
            self.update_student_table()

            # Show deletion success message
            messagebox.showinfo("Success", f"Student with ID {student_id} deleted successfully!")

            # Clear the form
            self.clear_form()

    def clear_form(self):
        # Clear entry widgets in the form
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def update_student_table(self):
        # Clear existing items in the student table
        for item in self.student_table.get_children():
            self.student_table.delete(item)

        # Insert data into the student table
        for student in self.students:
            self.student_table.insert("", "end", values=tuple(student[label] for label in student))

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagementSystem(root)
    # Adjust window size to fit the content
    root.geometry("800x400")
    root.mainloop()
