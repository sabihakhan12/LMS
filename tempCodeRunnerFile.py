import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import pymysql

# Database Connection
def connect_to_database():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="sabiha1234",
        database="library_db",
        charset="utf8mb4"
    )

# User Authentication for Login
def authenticate():
    username = login_username_entry.get()
    password = login_password_entry.get()

    if not username or not password:
        messagebox.showerror("Error", "Username and password are required")
        return

    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            login_frame.pack_forget()
            main_frame.pack(fill="both", expand=True)
        else:
            messagebox.showerror("Error", "Invalid username or password")
    except pymysql.MySQLError as e:
        messagebox.showerror("Database Error", str(e))

# User Registration (Sign-Up)
def sign_up():
    username = login_username_entry.get()
    password = login_password_entry.get()

    if not username or not password:
        messagebox.showerror("Error", "Username and password are required")
        return

    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            messagebox.showerror("Error", "Username already exists")
            conn.close()
            return

        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "User registered successfully")
        sign_up_frame.pack_forget()
        login_frame.pack(fill="both", expand=True)
    except pymysql.MySQLError as e:
        messagebox.showerror("Database Error", str(e))

# Insert Record
def insert_record():
    name = name_entry.get()
    book_id = book_id_entry.get()
    book_name = book_name_entry.get()
    issue_date = issue_date_entry.get()
    return_date = return_date_entry.get()
    email = email_entry.get()
    phone_number = phone_entry.get()

    if not (name and book_id and book_name and issue_date and return_date and email and phone_number):
        messagebox.showerror("Error", "All fields are required")
        return

    if "@" not in email or "." not in email:
        messagebox.showerror("Error", "Invalid email address")
        return

    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        query = "INSERT INTO library_records (name, book_id, book_name, issue_date, return_date, email, phone_number) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (name, book_id, book_name, issue_date, return_date, email, phone_number))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Record inserted successfully")
        display_records()
        clear_fields()
    except pymysql.MySQLError as e:
        messagebox.showerror("Database Error", str(e))

# Update Record
def update_record():
    selected_item = records_tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a record to update")
        return

    record = records_tree.item(selected_item)["values"]
    record_id = record[0]

    name = name_entry.get()
    book_id = book_id_entry.get()
    book_name = book_name_entry.get()
    issue_date = issue_date_entry.get()
    return_date = return_date_entry.get()
    email = email_entry.get()
    phone_number = phone_entry.get()

    if not (name and book_id and book_name and issue_date and return_date and email and phone_number):
        messagebox.showerror("Error", "All fields are required")
        return

    if "@" not in email or "." not in email:
        messagebox.showerror("Error", "Invalid email address")
        return

    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        query = """UPDATE library_records
                   SET name = %s, book_id = %s, book_name = %s, issue_date = %s, return_date = %s, email = %s, phone_number = %s
                   WHERE id = %s"""
        cursor.execute(query, (name, book_id, book_name, issue_date, return_date, email, phone_number, record_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Record updated successfully")
        display_records()
        clear_fields()
    except pymysql.MySQLError as e:
        messagebox.showerror("Database Error", str(e))

# Delete Record
def delete_record():
    selected_item = records_tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a record to delete")
        return

    record = records_tree.item(selected_item)["values"]
    record_id = record[0]

    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM library_records WHERE id = %s", (record_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Record deleted successfully")
        display_records()
    except pymysql.MySQLError as e:
        messagebox.showerror("Database Error", str(e))

# Search Record
def search_record():
    search_term = search_entry.get()

    if not search_term:
        messagebox.showerror("Error", "Please enter a search term")
        return

    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        query = """SELECT * FROM library_records
                   WHERE name LIKE %s OR book_name LIKE %s"""
        cursor.execute(query, (f"%{search_term}%", f"%{search_term}%"))
        records = cursor.fetchall()
        conn.close()

        records_tree.delete(*records_tree.get_children())
        for record in records:
            records_tree.insert("", tk.END, values=record)
    except pymysql.MySQLError as e:
        messagebox.showerror("Database Error", str(e))

# Display Records
def display_records():
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        query = "SELECT * FROM library_records"
        cursor.execute(query)
        records = cursor.fetchall()
        conn.close()

        records_tree.delete(*records_tree.get_children())
        for record in records:
            records_tree.insert("", tk.END, values=record)
    except pymysql.MySQLError as e:
        messagebox.showerror("Database Error", str(e))

# Clear Fields
def clear_fields():
    name_entry.delete(0, tk.END)
    book_id_entry.delete(0, tk.END)
    book_name_entry.delete(0, tk.END)
    issue_date_entry.delete(0, tk.END)
    return_date_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)

# Main Window
root = tk.Tk()
root.title("Library Management System")
root.geometry("1000x600")
root.configure(bg="#2C3E50")

# Load background image
background_image = Image.open("assets/background.jpg")  # Replace with your image path
background_image = background_image.resize((1000, 600))  # Adjust to your window size
background_photo = ImageTk.PhotoImage(background_image)

# Login Frame with Background
login_frame = tk.Frame(root, bg="#2C3E80")
login_canvas = tk.Canvas(login_frame, width=1000, height=600)
login_canvas.pack(fill="both", expand=True)
login_canvas.create_image(0, 0, anchor="nw", image=background_photo)

login_label = tk.Label(login_frame, text="Library Management System", font=("Arial", 43, "bold"), bg="#2C3E50", fg="#ECF0F1")
login_canvas.create_window(500, 80, window=login_label)
login_la = tk.Label(login_frame, text="Login", font=("Arial", 30, "bold"), bg="#2C3E50", fg="#ECF0F1")
login_canvas.create_window(500, 150, window=login_la)

username_label = tk.Label(login_frame, text="Username:", font=("Arial", 14), bg="#2C3E50", fg="#ECF0F1")
login_canvas.create_window(370, 200, window=username_label)

password_label = tk.Label(login_frame, text="Password:", font=("Arial", 14), bg="#2C3E50", fg="#ECF0F1")
login_canvas.create_window(370, 250, window=password_label)

# Login Frame Widgets
login_username_entry = tk.Entry(login_frame, font=("Arial", 14), width=30)
login_canvas.create_window(600, 200, window=login_username_entry)

login_password_entry = tk.Entry(login_frame, font=("Arial", 14), width=30, show="*")
login_canvas.create_window(600, 250, window=login_password_entry)

# Modify `authenticate` function to use these widgets
def authenticate():
    username = login_username_entry.get()
    password = login_password_entry.get()

    if not username or not password:
        messagebox.showerror("Error", "Username and password are required")
        return

    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            messagebox.showinfo("Success", "Login successful")
            login_frame.pack_forget()
            main_frame.pack(fill="both", expand=True)
        else:
            messagebox.showerror("Error", "Invalid username or password")
    except pymysql.MySQLError as e:
        messagebox.showerror("Database Error", str(e))


login_button = tk.Button(login_frame, text="Login", font=("Arial", 14), command=authenticate, bg="#3498DB", fg="#FFFFFF")
login_canvas.create_window(500, 300, window=login_button)

sign_up_button = tk.Button(login_frame, text="Sign Up", font=("Arial", 12), command=lambda: (login_frame.pack_forget(), sign_up_frame.pack(fill="both", expand=True)), bg="#2ECC71", fg="#FFFFFF")
login_canvas.create_window(500, 350, window=sign_up_button)

# Sign-Up Frame with Background
sign_up_frame = tk.Frame(root, bg="#2C3E50")
sign_up_canvas = tk.Canvas(sign_up_frame, width=1000, height=600)
sign_up_canvas.pack(fill="both", expand=True)
sign_up_canvas.create_image(0, 0, anchor="nw", image=background_photo)

sign_up_label = tk.Label(sign_up_frame, text="Sign Up", font=("Arial", 30, "bold"), bg="#2C3E50", fg="#ECF0F1")
sign_up_canvas.create_window(500, 100, window=sign_up_label)

sign_up_username_label = tk.Label(sign_up_frame, text="Username:", font=("Arial", 14), bg="#2C3E50", fg="#ECF0F1")
sign_up_canvas.create_window(370, 200, window=sign_up_username_label)

sign_up_password_label = tk.Label(sign_up_frame, text="Password:", font=("Arial", 14), bg="#2C3E50", fg="#ECF0F1")
sign_up_canvas.create_window(370, 250, window=sign_up_password_label)

# Sign-Up Frame Widgets
sign_up_username_entry = tk.Entry(sign_up_frame, font=("Arial", 14), width=30)
sign_up_canvas.create_window(600, 200, window=sign_up_username_entry)

sign_up_password_entry = tk.Entry(sign_up_frame, font=("Arial", 14), width=30, show="*")
sign_up_canvas.create_window(600, 250, window=sign_up_password_entry)

# Modify `sign_up` function to use these widgets
def sign_up():
    username = sign_up_username_entry.get()
    password = sign_up_password_entry.get()

    if not username or not password:
        messagebox.showerror("Error", "Username and password are required")
        return

    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            messagebox.showerror("Error", "Username already exists")
            conn.close()
            return

        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "User registered successfully")
        sign_up_frame.pack_forget()
        login_frame.pack(fill="both", expand=True)
    except pymysql.MySQLError as e:
        messagebox.showerror("Database Error", str(e))

register_button = tk.Button(sign_up_frame, text="Register", font=("Arial", 14), command=sign_up, bg="#3498DB", fg="#FFFFFF")
sign_up_canvas.create_window(500, 300, window=register_button)

back_to_login_button = tk.Button(sign_up_frame, text="Back to Login", font=("Arial", 12), command=lambda: (sign_up_frame.pack_forget(), login_frame.pack(fill="both", expand=True)), bg="#E74C3C", fg="#FFFFFF")
sign_up_canvas.create_window(500, 350, window=back_to_login_button)


main_frame = tk.Frame(root, bg="#34259E")
main_canvas = tk.Canvas(main_frame, width=1000, height=800)
main_canvas.pack(fill="both", expand=True)
main_canvas.create_image(0, 0, anchor="nw", image=background_photo)

main_label = tk.Label(main_frame, text="Library Management System", font=("Arial", 24, "bold"), bg="#34495E", fg="#ECF0F1")
main_canvas.create_window(500, 32, window=main_label)

form_frame = tk.Frame(main_frame, bg="#34495E")
main_canvas.create_window(500, 175, window=form_frame)

tk.Label(form_frame, text="Name:", font=("Arial", 12), bg="#34495E", fg="#ECF0F1").grid(row=0, column=0, padx=10, pady=5, sticky="w")
name_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
name_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(form_frame, text="Book ID:", font=("Arial", 12), bg="#34495E", fg="#ECF0F1").grid(row=1, column=0, padx=10, pady=5, sticky="w")
book_id_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
book_id_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(form_frame, text="Book Name:", font=("Arial", 12), bg="#34495E", fg="#ECF0F1").grid(row=2, column=0, padx=10, pady=5, sticky="w")
book_name_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
book_name_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(form_frame, text="Issue Date (YYYY-MM-DD):", font=("Arial", 12), bg="#34495E", fg="#ECF0F1").grid(row=3, column=0, padx=10, pady=5, sticky="w")
issue_date_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
issue_date_entry.grid(row=3, column=1, padx=10, pady=5)

tk.Label(form_frame, text="Return Date (YYYY-MM-DD):", font=("Arial", 12), bg="#34495E", fg="#ECF0F1").grid(row=4, column=0, padx=10, pady=5, sticky="w")
return_date_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
return_date_entry.grid(row=4, column=1, padx=10, pady=5)

tk.Label(form_frame, text="Email:", font=("Arial", 12), bg="#34495E", fg="#ECF0F1").grid(row=5, column=0, padx=10, pady=5, sticky="w")
email_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
email_entry.grid(row=5, column=1, padx=10, pady=5)

tk.Label(form_frame, text="Phone Number:", font=("Arial", 12), bg="#34495E", fg="#ECF0F1").grid(row=6, column=0, padx=10, pady=5, sticky="w")
phone_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
phone_entry.grid(row=6, column=1, padx=10, pady=5)

# Action Buttons
action_frame = tk.Frame(main_frame, bg="#34495E")
main_canvas.create_window(500, 342, window=action_frame)

insert_button = tk.Button(action_frame, text="Insert Record", font=("Arial", 12), command=insert_record, bg="#27AE60", fg="#FFFFFF")
insert_button.grid(row=0, column=0, padx=10, pady=5)

update_button = tk.Button(action_frame, text="Update Record", font=("Arial", 12), command=update_record, bg="#F39C12", fg="#FFFFFF")
update_button.grid(row=0, column=1, padx=10, pady=5)

delete_button = tk.Button(action_frame, text="Delete Record", font=("Arial", 12), command=delete_record, bg="#E74C3C", fg="#FFFFFF")
delete_button.grid(row=0, column=2, padx=10, pady=5)

search_label = tk.Label(action_frame, text="Search:", font=("Arial", 12), bg="#34495E", fg="#ECF0F1")
search_label.grid(row=1, column=0, padx=10, pady=5)
search_entry = tk.Entry(action_frame, font=("Arial", 12), width=30)
search_entry.grid(row=1, column=1, padx=10, pady=5)

search_button = tk.Button(action_frame, text="Search", font=("Arial", 12), command=search_record, bg="#3498DB", fg="#FFFFFF")
search_button.grid(row=1, column=2, padx=10, pady=5)

records_frame = tk.Frame(main_frame, bg="#34495E")
main_canvas.create_window(500, 500, window=records_frame)

columns = ("id", "name", "book_id", "book_name", "issue_date", "return_date", "email", "phone_number")
records_tree = ttk.Treeview(records_frame, columns=columns, show="headings", height=10)

for col in columns:
    records_tree.heading(col, text=col.capitalize())
    records_tree.column(col, width=100)

records_tree.pack(side="left", fill="both", expand=True)

scrollbar = ttk.Scrollbar(records_frame, orient="vertical", command=records_tree.yview)
records_tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")


login_frame.pack(fill="both", expand=True)

root.mainloop()

