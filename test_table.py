import tkinter as tk
from tkinter import ttk
from datetime import datetime
import csv

class CsvWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Mass spec sample list")

        self.operator = "EB"
        self.rack_size = 54
        self.current_position = 1
        self.current_box = 1

        # Create Treeview widget
        self.tree = ttk.Treeview(root, columns=("aliquot_id", "operator", "filename", "path", "instrument_method", "position", "inj_volume"), show="headings", selectmode="browse")
        self.tree.heading("aliquot_id", text="aliquot_id")
        self.tree.heading("operator", text="operator")
        self.tree.heading("filename", text="filename")
        self.tree.heading("path", text="path")
        self.tree.heading("instrument_method", text="instrument_method")
        self.tree.heading("position", text="position")
        self.tree.heading("inj_volume", text="inj_volume")

        # Bind Enter key to add row
        self.root.bind("<Return>", self.add_row)

        # Entry widgets for data input
        self.aliquot_id_entry = ttk.Entry(root)

        # Submit button
        submit_button = ttk.Button(root, text="Submit", command=self.submit_table)

        # Grid layout for widgets
        self.tree.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
        self.aliquot_id_entry.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        submit_button.grid(row=2, column=0, columnspan=2, pady=10)

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
        filename = datetime.now().strftime("%Y%m%d") + "_" + self.operator + "_" + aliquot_id
        path = ""
        instrument_method = ""
        position = f"pos {self.current_position} in box {self.current_box}"
        inj_volume = 2

        # Update position and box for the next row
        self.current_position += 1
        if self.current_position > self.rack_size:
            self.current_position = 1
            self.current_box += 1

        # Insert data into Treeview
        item_id = self.tree.insert("", "end", values=(aliquot_id, operator, filename, path, instrument_method, position, inj_volume))

        # Scroll to the last added row
        self.tree.see(item_id)

        # Clear entry widgets
        self.aliquot_id_entry.delete(0, "end")

    def submit_table(self):
        # Get all items from the Treeview
        all_items = self.tree.get_children()

        # Check if there are any rows to export
        if not all_items:
            print("No data to export.")
            return

        # Extract data from the Treeview
        data_to_export = [self.tree.item(item, 'values') for item in all_items]

        # Write data to a CSV file
        with open("table_data.csv", "w", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            # Write header
            csv_writer.writerow(["aliquot_id", "operator", "filename", "path", "instrument_method", "position", "inj_volume"])
            # Write data
            csv_writer.writerows(data_to_export)

        print("CSV file created: table_data.csv")

if __name__ == "__main__":
    root = tk.Tk()
    app = EditableTable(root)
    root.mainloop()
