# To convert this script into a .exe file: pyinstaller --onefile label_creator.py in anaconda prompt

import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os
import requests

class HomeWindow(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        # Create a variable to store the entered text
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.location = tk.StringVar()
        self.operator = tk.StringVar()

        error1 = os.environ.get("error1")
        error2 = os.environ.get("error2")
        print(error1)
        print(error2)

        if not error1 and not error2:
            # Create widgets for the main page
            label = tk.Label(self, text="Connect to directus and select where the CSV will be stored")
            label.pack()
        elif error1:
            # Create widgets for the main page
            label = tk.Label(self, text=error1)
            label.pack()
            
        elif error2:
            # Create widgets for the main page
            label = tk.Label(self, text=error2)
            label.pack()


        # Create text entry fields
        label_username = tk.Label(self, text="Your directus username:")
        label_username.pack()
        entry_username = tk.Entry(self, textvariable=self.username)
        entry_username.pack()

        label_password = tk.Label(self, text="Your directus password:")
        label_password.pack()
        entry_password = tk.Entry(self, textvariable=self.password, show="*")
        entry_password.pack()

        label_operator = tk.Label(self, text="operator's initials:")
        label_operator.pack()
        entry_operator = tk.Entry(self, textvariable=self.operator)
        entry_operator.pack()

        output_label = tk.Label(self, text="Select the output path for the sample list")
        output_label.pack()
        output_button = tk.Button(self, text="select path", command=self.output_folder)
        output_button.pack()

        button_submit = tk.Button(self, text="Submit", command=self.show_values)
        button_submit.pack()

    def output_folder(self):
        os.environ['output_folder'] = filedialog.askdirectory()

    def show_values(self):
        # Retrieve the entered values
        os.environ['username'] = self.username.get()
        os.environ['password'] = self.password.get()
        os.environ['operator'] = self.operator.get()
        self.testConnection()
        self.master.destroy()

    def open_CsvWindow(self):
        # Hide the main page and open Window 3
        self.pack_forget()
        CsvWindow()
        
    def testConnection(self):
        username = os.environ.get("username")
        password = os.environ.get("password")
        output_folder = os.environ.get("output_folder")

        if username and password and output_folder:
            # Define the Directus base URL
            base_url = 'http://directus.dbgi.org'

            # Define the login endpoint URL
            login_url = base_url + '/auth/login'
            # Create a session object for making requests
            session = requests.Session()
            # Send a POST request to the login endpoint
            response = session.post(login_url, json={'email': username, 'password': password})
        
            if response.status_code == 200:
                os.environ['error1'] = ""
                os.environ['error2'] = ""
                data = response.json()['data']
                access_token = data['access_token']
                os.environ['access_token'] = str(access_token)

                # Hide the main page and open Window 2
                self.open_CsvWindow()
            
            else:
                # Recreate the main page
                error1 = "Wrong directus credentials/not connected to UNIFR network"
                os.environ['error1'] = error1
                os.environ['error2'] = ""
                self.pack_forget()
                main_page = HomeWindow(window)
                main_page.pack()
                window.mainloop()

        else:
            # Recreate the main page
            error2 = "Please provide all asked values"
            os.environ['error2'] = error2
            os.environ['error1'] = ""
            self.pack_forget()
            main_page = HomeWindow(window)
            main_page.pack()
            window.mainloop()

import tkinter as tk
from tkinter import ttk

import tkinter as tk
from tkinter import ttk

class CsvWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Mass spec data:")
        self.minsize(600, 400)

        # Create a Treeview widget
        self.tree = ttk.Treeview(self, columns=("aliquot_id", "operator", "mass_spec_id"), show="headings")
        
        # Set the column headings
        self.tree.heading("aliquot_id", text="aliquot_id")
        self.tree.heading("operator", text="operator")
        self.tree.heading("mass_spec_id", text="mass_spec_id")

        # Set the column widths
        self.tree.column("aliquot_id", width=100)
        self.tree.column("operator", width=100)
        self.tree.column("mass_spec_id", width=100)

        # Bind events to update the values when editing
        self.tree.bind("<ButtonRelease-1>", self.edit_item)
        self.tree.bind("<Return>", self.edit_item)

        # Insert a blank row with Entry widgets in the aliquot_id column
        entry_aliquot_id = ttk.Entry(self.tree)
        self.tree.insert("", "end", values=(entry_aliquot_id, " ", " "))

        # Pack the Treeview widget
        self.tree.pack(pady=10)

        # Add a button to insert a new row
        insert_button = ttk.Button(self, text="Insert Row", command=self.insert_row)
        insert_button.pack(pady=10)

    def insert_row(self):
        # Insert a blank row with Entry widgets in the aliquot_id column
        entry_aliquot_id = ttk.Entry(self.tree)
        self.tree.insert("", "end", values=(entry_aliquot_id, " ", " "))

    def edit_item(self, event):
        # Get the selected item
        item = self.tree.selection()

        if item:
            # Get the values from the selected item
            values = [entry.get() if isinstance(entry, ttk.Entry) else entry for entry in self.tree.item(item, 'values')]

            # Update the Treeview with the edited values
            self.tree.item(item, values=values)



# Create the main window
window = tk.Tk()
window.title("Mass spec")
window.minsize(600, 400)

# Create the main page
main_page = HomeWindow(window)
main_page.pack()

window.mainloop()