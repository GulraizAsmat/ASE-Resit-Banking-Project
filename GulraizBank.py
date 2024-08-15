import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
import os
from datetime import datetime

file_path = 'client_details.xlsx'
transaction_file_path = 'transaction_history.xlsx'

# Function to handle login
def login():
    login_window = tk.Toplevel(root)
    login_window.title("Login")
    login_window.configure(bg="green")

    tk.Label(login_window, text="Username", bg="green", fg="white").pack()
    username_entry = tk.Entry(login_window)
    username_entry.pack()

    tk.Label(login_window, text="Password", bg="green", fg="white").pack()
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack()

    tk.Button(login_window, text="Submit", command=lambda: check_login(username_entry.get(), password_entry.get(), login_window)).pack()

def check_login(username, password, login_window):
    if os.path.exists(file_path):
        df = pd.read_excel(file_path, dtype={'Last Logged in': str})
    else:
        messagebox.showwarning("Login Error", "No users found. Please create an account.")
        return

    user_row = df[(df.iloc[:, 0] == username) & (df.iloc[:, 1] == password)]
    
    if not user_row.empty:
        df.loc[df.iloc[:, 0] == username, 'Last Logged in'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        df.to_excel(file_path, index=False)
        messagebox.showinfo("Login", "Login successful!")
        login_window.destroy()
        account_management_window(username)
    else:
        messagebox.showwarning("Login Error", "Invalid username or password.")

def create_account():
    create_window = tk.Toplevel(root)
    create_window.title("Create New Account")
    create_window.configure(bg="green")

    details = ["Username", "Password", "Account Type", "Gender", "Email", "Contact", "Balance"]
    entries = {}

    for detail in details:
        tk.Label(create_window, text=detail, bg="green", fg="white").pack()
        if detail == "Account Type":
            entry = ttk.Combobox(create_window, values=["Personal", "Business"])
            entry.pack()
        elif detail == "Gender":
            entry = ttk.Combobox(create_window, values=["Male", "Female"])
            entry.pack()
        else:
            entry = tk.Entry(create_window)
            entry.pack()
        entries[detail] = entry

    tk.Button(create_window, text="Submit", command=lambda: save_account(entries, create_window)).pack()

def save_account(entries, create_window):
    details = {detail: entry.get() for detail, entry in entries.items()}
    
    if not all(details.values()):
        messagebox.showwarning("Validation Error", "All fields are required!")
        return
    
    details["Last Logged in"] = ""  # Initialize last logged in column
    
    if os.path.exists(file_path):
        df = pd.read_excel(file_path, dtype={'Last Logged in': str})
    else:
        df = pd.DataFrame(columns=details.keys())

    # Ensure Balance is converted to an integer
    details["Balance"] = int(details["Balance"])

    new_entry_df = pd.DataFrame([details])
    df = pd.concat([df, new_entry_df], ignore_index=True)

    df.to_excel(file_path, index=False)
    
    messagebox.showinfo("Account Created", "Account successfully created!")
    create_window.destroy()

def account_management_window(username):
    management_window = tk.Toplevel(root)
    management_window.title("Account Management")
    management_window.configure(bg="green")

    tk.Label(management_window, text=f"Welcome, {username}", bg="green", fg="white", font=("Helvetica", 16)).pack(pady=20)

    tk.Button(management_window, text="Close an account", command=lambda: close_account(username)).pack(pady=5)
    tk.Button(management_window, text="Deposit cash", command=lambda: deposit_cash(username)).pack(pady=5)
    tk.Button(management_window, text="Withdraw cash", command=lambda: withdraw_cash(username)).pack(pady=5)
    tk.Button(management_window, text="Transfer funds", command=lambda: transfer_funds(username)).pack(pady=5)
    tk.Button(management_window, text="Transaction history", command=lambda: transaction_history(username)).pack(pady=5)
    tk.Button(management_window, text="Account Information", command=lambda: view_account_information(username)).pack(pady=5)
    tk.Button(management_window, text="Manage Services", command=lambda: manage_services(username)).pack(pady=5)
    tk.Button(management_window, text="Manage Recurring Payments", command=lambda: manage_recurring_payments(username)).pack(pady=5)

def view_account_information(username):
    df = pd.read_excel(file_path, dtype={'Last Logged in': str})
    user_row = df[df['Username'] == username]
    
    if not user_row.empty:
        info_window = tk.Toplevel(root)
        info_window.title("Account Information")
        info_window.configure(bg="green")

        account_info = user_row.iloc[0].to_dict()
        for key, value in account_info.items():
            tk.Label(info_window, text=f"{key}: {value}", bg="green", fg="white").pack()
    else:
        messagebox.showwarning("Error", "Account information not found.")

def manage_services(username):
    services_window = tk.Toplevel(root)
    services_window.title("Manage Services")
    services_window.configure(bg="green")

    tk.Label(services_window, text="Manage Services", bg="green", fg="white", font=("Helvetica", 16)).pack(pady=20)
    tk.Button(services_window, text="Request Checkbook", command=lambda: request_service(username, "Checkbook")).pack(pady=5)
    tk.Button(services_window, text="Request Debit Card", command=lambda: request_service(username, "Debit Card")).pack(pady=5)
    tk.Button(services_window, text="Request Credit Card", command=lambda: request_service(username, "Credit Card")).pack(pady=5)

def request_service(username, service_type):
    messagebox.showinfo("Service Requested", f"{service_type} requested successfully!")
    # Additional functionality to handle service requests can be added here

def manage_recurring_payments(username):
    recurring_window = tk.Toplevel(root)
    recurring_window.title("Manage Recurring Payments")
    recurring_window.configure(bg="green")

    tk.Label(recurring_window, text="Manage Recurring Payments", bg="green", fg="white", font=("Helvetica", 16)).pack(pady=20)
    tk.Button(recurring_window, text="Set Up Recurring Payment", command=lambda: setup_recurring_payment(username)).pack(pady=5)
    tk.Button(recurring_window, text="View Recurring Payments", command=lambda: view_recurring_payments(username)).pack(pady=5)

def setup_recurring_payment(username):
    setup_window = tk.Toplevel(root)
    setup_window.title("Set Up Recurring Payment")
    setup_window.configure(bg="green")

    tk.Label(setup_window, text="Recipient:", bg="green", fg="white").pack()
    recipient_entry = tk.Entry(setup_window)
    recipient_entry.pack()

    tk.Label(setup_window, text="Amount:", bg="green", fg="white").pack()
    amount_entry = tk.Entry(setup_window)
    amount_entry.pack()

    tk.Label(setup_window, text="Frequency (e.g., Monthly):", bg="green", fg="white").pack()
    frequency_entry = tk.Entry(setup_window)
    frequency_entry.pack()

    tk.Button(setup_window, text="Submit", command=lambda: save_recurring_payment(username, recipient_entry.get(), amount_entry.get(), frequency_entry.get(), setup_window)).pack()

def save_recurring_payment(username, recipient, amount, frequency, setup_window):
    # Logic to save recurring payment details
    messagebox.showinfo("Recurring Payment Setup", "Recurring payment setup successfully!")
    setup_window.destroy()

def view_recurring_payments(username):
    # Logic to display recurring payments
    recurring_payments_window = tk.Toplevel(root)
    recurring_payments_window.title("View Recurring Payments")
    recurring_payments_window.configure(bg="green")

    tk.Label(recurring_payments_window, text="Recurring Payments", bg="green", fg="white", font=("Helvetica", 16)).pack(pady=20)
    # Fetch and display recurring payments for the user
    # For demonstration purposes, a static message is shown
    tk.Label(recurring_payments_window, text="No recurring payments found.", bg="green", fg="white").pack()

def close_account(username):
    if messagebox.askyesno("Close Account", "Are you sure you want to close your account?"):
        df = pd.read_excel(file_path, dtype={'Last Logged in': str})
        df = df[df['Username'] != username]
        df.to_excel(file_path, index=False)
        messagebox.showinfo("Account Closed", "Your account has been closed.")
        root.quit()

def deposit_cash(username):
    def submit_deposit(amount_entry):
        amount = amount_entry.get()
        if not amount.isdigit() or int(amount) <= 0:
            messagebox.showwarning("Invalid Amount", "Please enter a valid amount.")
            return

        amount = int(amount)
        df = pd.read_excel(file_path, dtype={'Last Logged in': str})
        df['Balance'] = df['Balance'].astype(int)  # Ensure Balance column is treated as int
        df.loc[df['Username'] == username, 'Balance'] += amount
        df.to_excel(file_path, index=False)

        transaction_df = pd.DataFrame({
            'Username': [username],
            'Date': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            'Type': ['Deposit'],
            'Amount': [amount]
        })

        if os.path.exists(transaction_file_path):
            transaction_history_df = pd.read_excel(transaction_file_path)
        else:
            transaction_history_df = pd.DataFrame(columns=['Username', 'Date', 'Type', 'Amount'])

        transaction_history_df = pd.concat([transaction_history_df, transaction_df], ignore_index=True)
        transaction_history_df.to_excel(transaction_file_path, index=False)

        messagebox.showinfo("Deposit Successful", f"{amount} has been deposited to your account.")
        deposit_window.destroy()

    deposit_window = tk.Toplevel(root)
    deposit_window.title("Deposit Cash")
    deposit_window.configure(bg="green")

    tk.Label(deposit_window, text="Amount to Deposit:", bg="green", fg="white").pack()
    amount_entry = tk.Entry(deposit_window)
    amount_entry.pack()

    tk.Button(deposit_window, text="Submit", command=lambda: submit_deposit(amount_entry)).pack()

def withdraw_cash(username):
    def submit_withdrawal(amount_entry):
        amount = amount_entry.get()
        if not amount.isdigit() or int(amount) <= 0:
            messagebox.showwarning("Invalid Amount", "Please enter a valid amount.")
            return

        amount = int(amount)
        df = pd.read_excel(file_path, dtype={'Last Logged in': str})
        df['Balance'] = df['Balance'].astype(int)  # Ensure Balance column is treated as int
        balance = df.loc[df['Username'] == username, 'Balance'].values[0]
        
        if amount > balance:
            messagebox.showwarning("Insufficient Funds", "You do not have enough balance.")
            return

        df.loc[df['Username'] == username, 'Balance'] -= amount
        df.to_excel(file_path, index=False)

        transaction_df = pd.DataFrame({
            'Username': [username],
            'Date': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            'Type': ['Withdrawal'],
            'Amount': [amount]
        })

        if os.path.exists(transaction_file_path):
            transaction_history_df = pd.read_excel(transaction_file_path)
        else:
            transaction_history_df = pd.DataFrame(columns=['Username', 'Date', 'Type', 'Amount'])

        transaction_history_df = pd.concat([transaction_history_df, transaction_df], ignore_index=True)
        transaction_history_df.to_excel(transaction_file_path, index=False)

        messagebox.showinfo("Withdrawal Successful", f"{amount} has been withdrawn from your account.")
        withdraw_window.destroy()

    withdraw_window = tk.Toplevel(root)
    withdraw_window.title("Withdraw Cash")
    withdraw_window.configure(bg="green")

    tk.Label(withdraw_window, text="Amount to Withdraw:", bg="green", fg="white").pack()
    amount_entry = tk.Entry(withdraw_window)
    amount_entry.pack()

    tk.Button(withdraw_window, text="Submit", command=lambda: submit_withdrawal(amount_entry)).pack()

def transfer_funds(username):
    def submit_transfer(amount_entry, recipient_entry):
        amount = amount_entry.get()
        recipient = recipient_entry.get()
        
        if not amount.isdigit() or int(amount) <= 0:
            messagebox.showwarning("Invalid Amount", "Please enter a valid amount.")
            return
        
        if recipient == username:
            messagebox.showwarning("Invalid Recipient", "You cannot transfer funds to your own account.")
            return
        
        amount = int(amount)
        df = pd.read_excel(file_path, dtype={'Last Logged in': str})
        df['Balance'] = df['Balance'].astype(int)  # Ensure Balance column is treated as int
        balance = df.loc[df['Username'] == username, 'Balance'].values[0]

        if amount > balance:
            messagebox.showwarning("Insufficient Funds", "You do not have enough balance.")
            return
        
        if recipient not in df['Username'].values:
            messagebox.showwarning("Invalid Recipient", "Recipient account does not exist.")
            return

        df.loc[df['Username'] == username, 'Balance'] -= amount
        df.loc[df['Username'] == recipient, 'Balance'] += amount
        df.to_excel(file_path, index=False)

        transaction_df = pd.DataFrame({
            'Username': [username, recipient],
            'Date': [datetime.now().strftime("%Y-%m-%d %H:%M:%S"), datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            'Type': ['Transfer Out', 'Transfer In'],
            'Amount': [-amount, amount]
        })

        if os.path.exists(transaction_file_path):
            transaction_history_df = pd.read_excel(transaction_file_path)
        else:
            transaction_history_df = pd.DataFrame(columns=['Username', 'Date', 'Type', 'Amount'])

        transaction_history_df = pd.concat([transaction_history_df, transaction_df], ignore_index=True)
        transaction_history_df.to_excel(transaction_file_path, index=False)

        messagebox.showinfo("Transfer Successful", f"{amount} has been transferred to {recipient}.")
        transfer_window.destroy()

    transfer_window = tk.Toplevel(root)
    transfer_window.title("Transfer Funds")
    transfer_window.configure(bg="green")

    tk.Label(transfer_window, text="Amount to Transfer:", bg="green", fg="white").pack()
    amount_entry = tk.Entry(transfer_window)
    amount_entry.pack()

    tk.Label(transfer_window, text="Recipient Username:", bg="green", fg="white").pack()
    recipient_entry = tk.Entry(transfer_window)
    recipient_entry.pack()

    tk.Button(transfer_window, text="Submit", command=lambda: submit_transfer(amount_entry, recipient_entry)).pack()

def transaction_history(username):
    history_window = tk.Toplevel(root)
    history_window.title("Transaction History")
    history_window.configure(bg="green")

    tk.Label(history_window, text="Filter by Date (YYYY-MM-DD):", bg="green", fg="white").pack()
    date_entry = tk.Entry(history_window)
    date_entry.pack()

    tk.Label(history_window, text="Filter by Type:", bg="green", fg="white").pack()
    type_entry = tk.Entry(history_window)
    type_entry.pack()

    tk.Label(history_window, text="Filter by Amount:", bg="green", fg="white").pack()
    amount_entry = tk.Entry(history_window)
    amount_entry.pack()

    def apply_filters():
        filters = {
            'Date': date_entry.get(),
            'Type': type_entry.get(),
            'Amount': amount_entry.get()
        }
        
        if os.path.exists(transaction_file_path):
            transaction_history_df = pd.read_excel(transaction_file_path)
        else:
            messagebox.showwarning("No Transactions", "No transaction history found.")
            return

        filtered_df = transaction_history_df[transaction_history_df['Username'] == username]

        if filters['Date']:
            filtered_df = filtered_df[filtered_df['Date'].str.contains(filters['Date'])]
        if filters['Type']:
            filtered_df = filtered_df[filtered_df['Type'].str.contains(filters['Type'])]
        if filters['Amount']:
            filtered_df = filtered_df[filtered_df['Amount'].astype(str).str.contains(filters['Amount'])]

        result_window = tk.Toplevel(history_window)
        result_window.title("Filtered Results")
        result_window.configure(bg="green")

        for index, row in filtered_df.iterrows():
            tk.Label(result_window, text=row.to_string(), bg="green", fg="white").pack()

    tk.Button(history_window, text="Apply Filters", command=apply_filters).pack()

def staff_login():
    staff_window = tk.Toplevel(root)
    staff_window.title("Staff Login")
    staff_window.configure(bg="green")

    tk.Label(staff_window, text="Staff Username", bg="green", fg="white").pack()
    staff_username_entry = tk.Entry(staff_window)
    staff_username_entry.pack()

    tk.Label(staff_window, text="Staff Password", bg="green", fg="white").pack()
    staff_password_entry = tk.Entry(staff_window, show="*")
    staff_password_entry.pack()

    tk.Button(staff_window, text="Submit", command=lambda: check_staff_login(staff_username_entry.get(), staff_password_entry.get())).pack()

def check_staff_login(username, password):
    # Dummy function to check staff login credentials
    messagebox.showinfo("Staff Login", f"Staff Username: {username}\nStaff Password: {password}")

# Main window
root = tk.Tk()
root.title("Innovative Banking App")
root.configure(bg="green")

tk.Label(root, text="Welcome to Innovative Banking App", font=("Helvetica", 16), bg="green", fg="white").pack(pady=20)

tk.Button(root, text="Login", command=login).pack(pady=10)
tk.Label(root, text="Click here to login", bg="green", fg="white").pack()

tk.Button(root, text="Create New Account", command=create_account).pack(pady=10)
tk.Label(root, text="Click here to sign up", bg="green", fg="white").pack()

tk.Button(root, text="Staff Login", command=staff_login).pack(pady=10)
tk.Label(root, text="Staff only", bg="green", fg="white").pack()

root.mainloop()
