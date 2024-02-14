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

            # Only update the "aliquot_id" column
            entry_aliquot_id = ttk.Entry(self.tree)
            entry_aliquot_id.insert(0, values[0])  # Populate the Entry with the current value
            self.tree.item(item, values=(entry_aliquot_id, values[1], values[2]))


if __name__ == "__main__":
    app = CsvWindow()
    app.mainloop()
