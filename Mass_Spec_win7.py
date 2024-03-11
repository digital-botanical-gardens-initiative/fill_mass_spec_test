# To convert this script into a .exe file: pyinstaller --onefile Mass_Spec.py in anaconda prompt

import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os
import requests
from datetime import datetime
import csv

class HomeWindow(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        # Create a variable to store the entered text
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.location = tk.StringVar()
        self.operator = tk.StringVar()
        self.col_rack_number = tk.IntVar()
        self.row_rack_number = tk.IntVar()
        self.inj_volume = tk.IntVar()

        error1 = os.environ.get("error1")
        error2 = os.environ.get("error2")

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

        label_col_rack_number = tk.Label(self, text="Number of columns in racks:")
        label_col_rack_number.pack()
        entry_col_rack_number = tk.Entry(self, textvariable=self.col_rack_number)
        self.col_rack_number.set("9")  # Default value
        entry_col_rack_number.pack()

        label_row_rack_number = tk.Label(self, text="Number of places in racks:")
        label_row_rack_number.pack()
        entry_row_rack_number = tk.Entry(self, textvariable=self.row_rack_number)
        self.row_rack_number.set("6")  # Default value
        entry_row_rack_number.pack()

        label_inj_volume = tk.Label(self, text="Injection volume (in µL):")
        label_inj_volume.pack()
        entry_inj_volume = tk.Entry(self, textvariable=self.inj_volume)
        self.inj_volume.set("2") # Default value
        entry_inj_volume.pack()

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
        os.environ['col_rack_number'] = str(self.col_rack_number.get())
        os.environ['row_rack_number'] = str(self.row_rack_number.get())
        os.environ['inj_volume'] = str(self.inj_volume.get())
        self.testConnection()
        self.master.destroy()

    def open_CsvWindow(self):
        # Hide the main page
        self.pack_forget()

        operator = os.environ.get("operator")

        output_folder = os.environ.get("output_folder")
        csv_window = CsvWindow(root=window, csv_path=f"{output_folder}/{datetime.now().strftime('%Y%m%d%H%M')}_{operator}_dbgi_pos.csv")
        csv_window.pack()
        
    def testConnection(self):
        username = os.environ.get("username")
        password = os.environ.get("password")
        output_folder = os.environ.get("output_folder")
        col_rack_number = os.environ.get("col_rack_number")
        row_rack_number = os.environ.get("row_rack_number")
        inj_volume = os.environ.get("inj_volume")

        if username and password and output_folder and col_rack_number and row_rack_number and inj_volume:
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

class CsvWindow:
    def __init__(self, root, csv_path):
        self.root = root
        self.root.title("Mass spec sample list")

        self.operator = os.environ.get("operator")
        self.col_rack_size = int(os.environ.get("col_rack_number"))
        self.row_rack_size = int(os.environ.get("row_rack_number"))
        self.inj_volume = int(os.environ.get("inj_volume"))
        self.access_token = os.environ.get("access_token")
        self.csv_path = csv_path
        self.current_position = 1
        self.current_row = 1

        # Create Treeview widget
        self.tree = ttk.Treeview(root, columns=("aliquot_id", "operator", "File Name", "Path", "Instrument Method", "Position", "Inj Vol"), show="headings", selectmode="browse")
        self.tree.heading("aliquot_id", text="aliquot_id")
        self.tree.heading("operator", text="operator")
        self.tree.heading("File Name", text="File Name")
        self.tree.heading("Path", text="Path")
        self.tree.heading("Instrument Method", text="Instrument Method")
        self.tree.heading("Position", text="Position")
        self.tree.heading("Inj Vol", text="Inj Vol")

        # Bind Enter key to add row
        self.root.bind("<Return>", self.add_row)

        # Entry widgets for data input
        self.aliquot_id_entry = ttk.Entry(root)

        # Error text hidden:
        self.label = ttk.Label(text="")
        self.label.grid(row=2, column=0, columnspan=2, pady=10)

        # Delete line button
        delete_button = ttk.Button(root, text="Delete selected line", command=self.delete_line)

        # Submit button
        submit_button = ttk.Button(root, text="Generate sample list", command=self.submit_table)

        # Grid layout for widgets
        self.tree.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
        self.aliquot_id_entry.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        delete_button.grid(row=3, column=0, columnspan=2, pady=10)
        submit_button.grid(row=3, column=1, columnspan=2, pady=10)
        
        

    def add_row(self, event=None):
        # Get data from entry widgets
        aliquot_id = self.aliquot_id_entry.get()

        # Check if aliquot_id is not empty
        if not aliquot_id:
            # Display an error message or handle it as needed
            print("Error: Aliquot ID cannot be empty!")
            return

        # Placeholder calculations for other columns
        operator = self.operator
        filename = datetime.now().strftime("%Y%m%d%H%M") + "_" + self.operator + "_" + aliquot_id
        path = "C:\Xcalibur\Data"
        instrument_method = r"C:\Xcalibur\methods\new_methods\Metabo_MAPP\100mm_C18_15min_DDA_ELON_pos"
        inj_volume = self.inj_volume

        # Send data to directus
        base_url = 'http://directus.dbgi.org'
        collection_url = base_url + '/items/Mass_Spectrometry_Analysis'
        session = requests.Session()
        session.headers.update({'Authorization': f'Bearer {self.access_token}'})

        #Add headers
        headers = {'Content-Type': 'application/json'}

        data = {'aliquot_id': aliquot_id,
                'mass_spec_id': filename,
                'injection_volume': inj_volume,
                'injection_method': "100mm_C18_15min_DDA_ELON_pos"}
        
        response = session.post(url=collection_url, headers=headers, json=data)

        self.label.config(text="")
    
        if response.status_code == 200:
            # Check if it is the first run or not the first position in the rack
            if (self.current_position > self.col_rack_size and self.current_position > self.col_rack_size) or (self.current_position == 1 and self.current_row == 1):
                # Open window to ask prefix
                ask_prefix_window = tk.Toplevel(self.root)
                ask_prefix_window.title("Add Prefix")
                self.ask_box = AskBoxPrefixWindow(ask_prefix_window)
                self.ask_box.pack()

                # Make CsvWindow wait for AskBoxPrefixWindow result
                ask_prefix_window.transient(self.root)
                ask_prefix_window.wait_window(self.ask_box)

            prefix = os.environ.get("prefix")
            alphabet_letter = chr(ord('A') + self.current_row - 1)
            position = f"{prefix}{alphabet_letter}{self.current_position}"

            # Update position and box for the next row
            self.current_position += 1
            if self.current_position > self.col_rack_size:
                self.current_position = 1
                self.current_row += 1

            # Check if the rack is full
            if self.current_row > self.row_rack_size:
                self.current_position = 1
                self.current_row = 1

            # display success message
            self.label.config(text="Correctly added!", foreground="green")
            # Insert data into Treeview
            item_id = self.tree.insert("", "end", values=(aliquot_id, operator, filename, path, instrument_method, position, inj_volume))

            # Scroll to the last added row
            self.tree.see(item_id)

            # Clear entry widgets
            self.aliquot_id_entry.delete(0, "end")

        # Catches forbidden access when token is expired and generates a new token
        elif response.status_code == 401:
            self.directus_reconnect()
        else:
            self.label.config(text="Directus error, check your entry!", foreground="red")

    def delete_line(self):
        print("delete line")

    def submit_table(self):
        # Get all items from the Treeview
        all_items = self.tree.get_children()
        # Check if there are any rows to export
        if not all_items:
            print("No data to export.")
            return

        # Extract data from the Treeview
        data_to_export = [self.tree.item(item, 'values')[2:] for item in all_items]  # Skip the first two elements

        # Write data to the CSV file
        with open(self.csv_path, "w", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            # Write header
            csv_writer.writerow(["File Name", "Path", "Instrument Method", "Position", "Inj Vol"])
            # Write data
            csv_writer.writerows(data_to_export)

        print(f"CSV file created: {self.csv_path}")

        # Close the Tkinter window
        self.root.destroy()

    def directus_reconnect(self):
        username = os.environ.get("username")
        password = os.environ.get("password")

        # Define the Directus base URL
        base_url = 'http://directus.dbgi.org'

        # Define the login endpoint URL
        login_url = base_url + '/auth/login'
        # Create a session object for making requests
        session = requests.Session()
        # Send a POST request to the login endpoint
        response = session.post(login_url, json={'email': username, 'password': password})
        
        if response.status_code == 200:
            data = response.json()['data']
            self.access_token = data['access_token']
            self.root.event_generate('<Return>')
            
        else:
            # Print error statement
            print("Reconnexion to directus failed")

class AskBoxPrefixWindow(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)

        self.prefix = tk.StringVar()

        # Adjust the window size
        root.geometry("300x150")  # Set the desired width and height

        # Label + textbox to enter prefix
        label_prefix = tk.Label(self, text="Box's prefix:")
        label_prefix.pack()

        entry_prefix = tk.Entry(self, textvariable=self.prefix)
        entry_prefix.pack()

        # Submit button
        button_submit = tk.Button(self, text="Submit", command=self.store_prefix)
        button_submit.pack()

    def store_prefix(self):
        os.environ['prefix'] = self.prefix.get()

        # Close the AskBoxPrefixWindow
        self.master.destroy()
        


# Create the main window
window = tk.Tk()
window.title("Mass spec")
window.minsize(600, 400)

# Create the main page
main_page = HomeWindow(window)
main_page.pack()

window.mainloop()