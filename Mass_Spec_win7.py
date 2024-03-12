# To convert this script into a .exe file: pyinstaller --onefile Mass_Spec_win7.py in anaconda prompt

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
        self.operator = tk.StringVar()
        self.ms_id = tk.StringVar()
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
        frame_labels_up = tk.Frame(self)
        frame_labels_up.pack(fill="x", pady=(5, 0))

        label_username = tk.Label(frame_labels_up, text="Directus username:")
        label_username.pack(side="left", padx=8, anchor="center")
        label_password = tk.Label(frame_labels_up, text="Directus password:   ")
        label_password.pack(side="right", padx=(0, 2),anchor="center")

        frame_entries_up = tk.Frame(self)
        frame_entries_up.pack(fill="x", pady=5)

        entry_username = tk.Entry(frame_entries_up, textvariable=self.username)
        entry_username.pack(side="left", anchor="center")
        entry_password = tk.Entry(frame_entries_up, textvariable=self.password, show="*")
        entry_password.pack(side="right", anchor="center")
        
        frame_labels_om = tk.Frame(self)
        frame_labels_om.pack(fill="x", pady=(5, 0))

        label_operator = tk.Label(frame_labels_om, text="Operator's initials:")
        label_operator.pack(side="left", padx=10, anchor="center")

        label_ms = tk.Label(frame_labels_om, text="Mass spectrometer ID:")
        label_ms.pack(side="right", anchor="center")

        frame_entries_om = tk.Frame(self)
        frame_entries_om.pack(fill="x", pady=(5, 0))

        entry_operator = tk.Entry(frame_entries_om, textvariable=self.operator)
        entry_operator.pack(side="left", anchor="center")

        entry_ms = tk.Entry(frame_entries_om, textvariable=self.ms_id)
        entry_ms.pack(side="right", anchor="center")

        frame_label_rack = tk.Frame(self)
        frame_label_rack.pack(fill="x", pady=(5, 0))

        label_col_rack_number = tk.Label(frame_label_rack, text="Rack size (columns x rows)")
        label_col_rack_number.pack(side="bottom", anchor="center")

        frame_entries_rack = tk.Frame(self)
        frame_entries_rack.pack(fill="x", pady=(5, 0))

        entry_col_rack_number = tk.Entry(frame_entries_rack, textvariable=self.col_rack_number)
        self.col_rack_number.set("9")
        entry_col_rack_number.pack(side="left", anchor="center")

        label_x = tk.Label(frame_entries_rack, text="x")
        label_x.pack(side="left", padx=40, anchor="center")

        entry_row_rack_number = tk.Entry(frame_entries_rack, textvariable=self.row_rack_number)
        self.row_rack_number.set("6")
        entry_row_rack_number.pack(side="right", anchor="center")

        frame_labels_paths = tk.Frame(self)
        frame_labels_paths.pack(fill="x", pady=(5, 0))

        label_method_path = tk.Label(frame_labels_paths, text="Method file:")
        label_method_path.pack(side="left", padx=25, anchor="center")

        label_data_path = tk.Label(frame_labels_paths, text="MS data directory")
        label_data_path.pack(side="right", padx=(0, 15), anchor="center")

        frame_entries_paths = tk.Frame(self)
        frame_entries_paths.pack(fill="x", pady=(5, 0))

        self.method_path_button = tk.Button(frame_entries_paths, text="method", command=self.method_file)
        self.method_path_button.pack(side="left", padx=35, anchor="center")

        self.data_path_button = tk.Button(frame_entries_paths, text="output", command=self.data_folder)
        self.data_path_button.pack(side="right", padx=40, anchor="center")

        frame_label_io = tk.Frame(self)
        frame_label_io.pack(fill="x", pady=(5, 0))

        label_inj_volume = tk.Label(frame_label_io, text="Injection volume (µL):")
        label_inj_volume.pack(side="left")

        label_output_path = tk.Label(frame_label_io, text="Sample list output directory: ")
        label_output_path.pack(side="right")

        frame_entries_io = tk.Frame(self)
        frame_entries_io.pack(fill="x", pady=(5, 0))

        entry_inj_volume = tk.Entry(frame_entries_io, textvariable=self.inj_volume)
        self.inj_volume.set("2")
        entry_inj_volume.pack(side="left")

        self.output_path_button = tk.Button(frame_entries_io, text="output", command=self.output_folder)
        self.output_path_button.pack(side="right", anchor="center", padx=(0, 40))

        frame_submit = tk.Frame(self)
        frame_submit.pack(pady=(20, 0))

        button_submit = tk.Button(frame_submit, text="Confirm", command=self.show_values)
        button_submit.pack(side="right")

    def data_folder(self):
        data_folder = filedialog.askdirectory()
        if data_folder:
            os.environ['data_folder'] = data_folder
            parts = data_folder.split("/")
            folder = parts[-1]
            self.data_path_button.config(text=folder)
    
    def output_folder(self):
        output_folder = filedialog.askdirectory()
        if output_folder:
            os.environ['output_folder'] = output_folder
            parts = output_folder.split("/")
            folder = parts[-1]
            self.output_path_button.config(text=folder)

    def method_file(self):
        method_file = filedialog.askopenfilename(filetypes=[("methods", "*.meth")])
        #method_file = filedialog.askopenfilename().split(".")[0]
        if method_file:
            os.environ['method_file'] = method_file
            parts = method_file.split("/")
            self.file = parts[-1]
            self.method_path_button.config(text=self.file)

    def show_values(self):
        # Retrieve the entered values
        os.environ['username'] = self.username.get()
        os.environ['password'] = self.password.get()
        os.environ['operator'] = self.operator.get()
        os.environ['ms_id'] = self.ms_id.get()
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
        csv_window = CsvWindow(root=window, csv_path=f"{output_folder}/{datetime.now().strftime('%Y%m%d')}_{operator}_dbgi_{self.file}.csv")
        csv_window()
        
    def testConnection(self):
        username = os.environ.get("username")
        password = os.environ.get("password")
        operator = os.environ.get("operator")
        ms_id = os.environ.get("ms_id")
        col_rack_number = os.environ.get("col_rack_number")
        row_rack_number = os.environ.get("row_rack_number")
        inj_volume = os.environ.get("inj_volume")
        method_file = os.environ.get("method_file")
        data_folder = os.environ.get("data_folder")
        output_folder = os.environ.get("output_folder")

        if username and password and operator and ms_id and col_rack_number and row_rack_number and inj_volume and method_file and data_folder and output_folder:
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

                access_token = os.environ.get("access_token")
                base_url = 'http://directus.dbgi.org'
                collection_url = base_url + f'/items/Injection_Methods/{self.file}'
                session = requests.Session()
                session.headers.update({'Authorization': f'Bearer {access_token}'})
                #collection_url = base_url + '/items/samples'
                response = session.get(collection_url)
                value = response.status_code
                if value == 200:
                    # Hide the main page and open Window 2
                    self.open_CsvWindow()
                else:
                    # Send data to directus
                    base_url = 'http://directus.dbgi.org'
                    collection_url = base_url + '/items/Injection_Methods'
                    session = requests.Session()
                    session.headers.update({'Authorization': f'Bearer {access_token}'})

                    #Add headers
                    headers = {'Content-Type': 'application/json'}

                    data = {'method_name': self.file}
        
                    response = session.post(url=collection_url, headers=headers, json=data)
    
                    if response.status_code == 200:
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
        print("This error doesn't impact the behaviour. It will be corrected in nex versions")
        self.root = root
        self.root.title("Mass spec sample list")

        self.operator = os.environ.get("operator")
        self.ms_id = os.environ.get("ms_id")
        self.col_rack_size = int(os.environ.get("col_rack_number"))
        self.row_rack_size = int(os.environ.get("row_rack_number"))
        self.inj_volume = int(os.environ.get("inj_volume"))
        self.access_token = os.environ.get("access_token")
        self.method_file = os.environ.get("method_file")
        self.data_path = os.environ.get("data_folder")
        self.csv_path = csv_path
        self.current_position = 1
        self.current_row = 1

        # Create Treeview widget
        self.tree = ttk.Treeview(root, columns=("aliquot_id", "operator", "ms_id", "File Name", "Path", "Instrument Method", "Position", "Inj Vol"), show="headings", selectmode="browse")
        self.tree.heading("aliquot_id", text="aliquot_id")
        self.tree.heading("operator", text="operator")
        self.tree.heading("ms_id", text="ms_id")
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

        # Submit button
        submit_button = ttk.Button(root, text="Generate sample list", command=self.submit_table)

        # Grid layout for widgets
        self.tree.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
        self.aliquot_id_entry.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        submit_button.grid(row=3, column=1, columnspan=2, pady=10)
        
        

    def add_row(self, event=None):
        # Get data from entry widgets
        aliquot_id = self.aliquot_id_entry.get()

        # Check if aliquot_id is not empty
        if not aliquot_id:
            # Display an error message
            self.label.config(text="aliquot id can't be empty!", foreground="red")
            return
        
        parts = self.method_file.split("/")
        file = parts[-1]

        # Placeholder calculations for other columns
        filename = datetime.now().strftime("%Y%m%d") + "_" + self.operator + "_" + aliquot_id + "_" + file
        path = self.data_path.replace("/", "\\")
        instrument_method = self.method_file.replace("/", "\\")
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
                'ms_id': self.ms_id,
                'injection_volume': inj_volume,
                'injection_method': file}
        
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
            item_id = self.tree.insert("", "end", values=(aliquot_id, self.operator, self.ms_id, filename, path, instrument_method, position, inj_volume))

            # Scroll to the last added row
            self.tree.see(item_id)

            # Clear entry widgets
            self.aliquot_id_entry.delete(0, "end")

        # Catches forbidden access when token is expired and generates a new token
        elif response.status_code == 401:
            self.directus_reconnect()
        else:
            self.label.config(text="Directus error, check your entry!", foreground="red")

    def submit_table(self):
        # Get all items from the Treeview
        all_items = self.tree.get_children()
        # Check if there are any rows to export
        if not all_items:
            self.label.config(text="No data to export!", foreground="red")
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

        self.label.config(text=f"CSV file created: {self.csv_path}", foreground="green")

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
            # Display error statement
            self.label.config(text="Reconnexion to directus failed", foreground="red")

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