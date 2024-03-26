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
            "TButton": {"configure": {"background": "#0074cc", "foreground": "#ffffff", "borderwidth": 1,
                                      "bordercolor": "#005082", "highlightbackground": "#005082", "border-radius": 5,
                                      "padding": (10, 5)},
                        "map": {"background": [("active", "#005082")]}},
            "TEntry": {"configure": {"fieldbackground": "#ffffff"}},
            "Treeview": {"configure": {"background": "#001f3f", "foreground": "#ffffff"}},
        })

        # Set the theme
        style.theme_use("dark_blue")

    def create_form(self):
        # Create a frame for the form
        form_frame = ttk.Frame(self.root, padding="20", style="DarkBlue.TFrame")
        form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Banner Label
        banner_label = ttk.Label(form_frame, text="Student Management System", font=("Helvetica", 16),
                                 style="DarkBlue.TLabel")
        banner_label.grid(row=0, column=0, columnspan=4, pady=10)

        # Create labels and entry widgets
        labels = ["ID", "Name", "Gender", "Age", "Enr-date", "Midterm", "Final", "GPA"]
        self.entries = {}
        for i, label in enumerate(labels):
            ttk.Label(form_frame, text=label + ":").grid(row=i + 1, column=0, padx=5, pady=5, sticky="e")
            if label == "Gender":
                gender_var = tk.StringVar()
                gender_dropdown = ttk.Combobox(form_frame, textvariable=gender_var, values=["Male", "Female"],
                                               state="readonly")
                gender_dropdown.grid(row=i + 1, column=1, padx=5, pady=5, sticky="w")
                self.entries[label] = gender_var
            else:
                entry = ttk.Entry(form_frame, width=20)
                entry.grid(row=i + 1, column=1, padx=5, pady=5, sticky="w")
                self.entries[label] = entry

        # Create buttons with border radius and improved alignment
        ttk.Button(form_frame, text="Add", command=self.add_student, style="DarkBlue.TButton").grid(row=len(labels) + 1,
                                                                                                    column=0, pady=10,
                                                                                                    ipadx=10, ipady=5,
                                                                                                    sticky="nsew")
        ttk.Button(form_frame, text="Update", command=self.update_student, style="DarkBlue.TButton").grid(
            row=len(labels) + 1, column=1, pady=10, ipadx=0, ipady=5, sticky="nsew")
        ttk.Button(form_frame, text="Delete", command=self.delete_student, style="DarkBlue.TButton").grid(
            row=len(labels) + 2, column=0, pady=10, ipadx=10, ipady=5, sticky="nsew")
        ttk.Button(form_frame, text="Clear", command=self.clear_form, style="DarkBlue.TButton").grid(
            row=len(labels) + 2, column=1, pady=10, ipadx=10, ipady=5, sticky="nsew")

        # Search section
        ttk.Label(form_frame, text="Search:").grid(row=len(labels) + 5, column=0, padx=5, pady=5, sticky="e")
        self.search_entry = ttk.Entry(form_frame, width=20)
        self.search_entry.grid(row=len(labels) + 5, column=1, padx=5, pady=5, sticky="w")
        ttk.Button(form_frame, text="Search", command=self.search_students, style="DarkBlue.TButton").grid(
            row=len(labels) + 5, column=2, pady=10, ipadx=10, ipady=5, sticky="nsew")

    def create_student_table(self):
        # Create a frame for the student table
        table_frame = ttk.Frame(self.root, padding="20", style="DarkBlue.TFrame")
        table_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Create the student table
        columns = ["ID", "Name", "Gender", "Age", "En-date", "Midterm", "Final", "GPA"]
        self.student_table = ttk.Treeview(table_frame, columns=columns, show="headings", style="DarkBlue.Treeview")

        # Set column headings
        for col in columns:
            self.student_table.heading(col, text=col)
            self.student_table.column(col, width=80, anchor="center")  # Adjust width as needed

        self.student_table.pack(expand=True, fill="both")

        # Set a fixed height for the table_frame
        table_frame.config(height=400)

        # Configure column weights to use available space
        for col in columns:
            table_frame.columnconfigure(columns.index(col), weight=1)

    def add_student(self):
        # Get data from entry widgets
        student_data = {label: entry.get() if label != "Gender" else entry.get() for label, entry in
                        self.entries.items()}

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
        student_data = {label: entry.get() if label != "Gender" else entry.get() for label, entry in
                        self.entries.items()}

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
        confirm = messagebox.askyesno("Confirm Deletion",
                                      f"Do you really want to delete the student with ID {student_id}?")

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
            if isinstance(entry, tk.Entry):
                entry.delete(0, tk.END)
            elif isinstance(entry, tk.StringVar):
                entry.set("")

    def update_student_table(self, data=None):
        # Clear existing items in the student table
        for item in self.student_table.get_children():
            self.student_table.delete(item)

        # Insert data into the student table
        data_to_display = data if data is not None else self.students
        for student in data_to_display:
            self.student_table.insert("", "end", values=tuple(student[label] for label in student))

    def search_students(self):
        # Get the search term from the entry widget
        search_term = self.search_entry.get().lower()

        # Filter students based on the search term
        search_results = [student for student in self.students if
                          any(search_term in value.lower() for value in student.values())]

        # Update the student table with search results
        self.update_student_table(search_results)


if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagementSystem(root)

    # Center the window
    window_width = 1080
    window_height = 640
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coordinate = (screen_width - window_width) // 2
    y_coordinate = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

    root.mainloop()
