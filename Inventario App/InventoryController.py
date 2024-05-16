import tkinter as tk
from tkinter import ttk
import sqlite3
import os
import qrcode
from PIL import Image, ImageDraw


class InventoryView:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventario de Almacén")

        self.add_frame = ttk.LabelFrame(self.root, text="Agregar Nuevo Item")
        self.add_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        self.name_label = tk.Label(self.add_frame, text="Nombre:")
        self.name_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.name_entry = tk.Entry(self.add_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        self.barcode_label = tk.Label(self.add_frame, text="Código de Barras:")
        self.barcode_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.barcode_entry = tk.Entry(self.add_frame)
        self.barcode_entry.grid(row=1, column=1, padx=5, pady=5)

        self.quantity_label = tk.Label(self.add_frame, text="Cantidad:")
        self.quantity_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.quantity_entry = tk.Entry(self.add_frame)
        self.quantity_entry.grid(row=2, column=1, padx=5, pady=5)

        self.add_button = tk.Button(self.add_frame, text="Agregar", command=self.add_item)
        self.add_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="we")

        self.print_qr_button = tk.Button(self.add_frame, text="Imprimir QR", command=self.print_qr)
        self.print_qr_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="we")

        self.list_frame = ttk.LabelFrame(self.root, text="Lista de Items")
        self.list_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        self.items_tree = ttk.Treeview(self.list_frame, columns=("ID", "Nombre", "Código de Barras", "Cantidad", "QR Code"), show="headings")
        self.items_tree.heading("ID", text="ID")
        self.items_tree.heading("Nombre", text="Nombre")
        self.items_tree.heading("Código de Barras", text="Código de Barras")
        self.items_tree.heading("Cantidad", text="Cantidad")
        self.items_tree.heading("QR Code", text="QR Code")
        self.items_tree.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        scrollbar = ttk.Scrollbar(self.list_frame, orient="vertical", command=self.items_tree.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.items_tree.configure(yscrollcommand=scrollbar.set)

        self.status_label = tk.Label(self.root, text="", fg="red")
        self.status_label.grid(row=3, column=0, padx=10, pady=5)

    def add_item(self):
        name = self.name_entry.get()
        barcode = self.barcode_entry.get()
        quantity = self.quantity_entry.get()
        if name and barcode and quantity:
            qr_code = self.controller.generate_qr_code(barcode)
            success = self.controller.add_item(name, barcode, quantity, qr_code)
            if success:
                self.status_label.config(text="¡Item agregado correctamente!", fg="green")
                self.display_items()
            else:
                self.status_label.config(text="¡El código de barras ya está en uso!", fg="red")
        else:
            self.status_label.config(text="¡Por favor, completa todos los campos!", fg="red")

    def display_items(self):
        items = self.controller.get_all_items()
        for item in self.items_tree.get_children():
            self.items_tree.delete(item)
        for row in items:
            self.items_tree.insert('', 'end', values=row)

    def print_qr(self):
        selected_item = self.get_selected_item()
        if selected_item:
            name, barcode, quantity, qr_code = selected_item
            qr_code_img = Image.open(qr_code)
            qr_code_img.show()

    def get_selected_item(self):
        selection = self.items_tree.selection()
        if selection:
            item_id = selection[0]
            item_values = self.items_tree.item(item_id, 'values')
            return item_values
        else:
            return None


class InventoryController:
    def __init__(self):
        self.model = InventoryModel('inventory.db')
        self.root = tk.Tk()
        self.view = InventoryView(self.root)
        self.view.controller = self

    def add_item(self, name, barcode, quantity, qr_code):
        return self.model.add_item(name, barcode, quantity, qr_code)

    def get_all_items(self):
        return self.model.get_all_items()

    def generate_qr_code(self, barcode):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(barcode)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        qr_code_filename = f"qr_code_{barcode}.png"
        img.save(qr_code_filename)
        return qr_code_filename


class InventoryModel:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.c = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS items
                     (id INTEGER PRIMARY KEY, name TEXT, barcode TEXT UNIQUE, quantity INTEGER, qr_code TEXT)''')
        self.conn.commit()

    def add_item(self, name, barcode, quantity, qr_code):
        try:
            self.c.execute("INSERT INTO items (name, barcode, quantity, qr_code) VALUES (?, ?, ?, ?)",
                      (name, barcode, quantity, qr_code))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_all_items(self):
        self.c.execute("SELECT * FROM items")
        return self.c.fetchall()


if __name__ == "__main__":
    app = InventoryController()
    app.root.mainloop()
