import tkinter as tk
from tkinter import ttk
import qrcode
import os

class InventoryView:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventario de Almacén")

        # Frame para agregar elementos
        self.add_frame = ttk.LabelFrame(self.root, text="Agregar Nuevo Item")
        self.add_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        # Resto del código de la interfaz de agregar elementos...

        # Frame para mostrar la imagen del código de barras o QR
        self.image_frame = ttk.LabelFrame(self.root, text="Imagen del Código de Barras o QR")
        self.image_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        self.barcode_image_label = tk.Label(self.image_frame)
        self.barcode_image_label.grid(row=0, column=0, padx=5, pady=5)

        # Botón para imprimir el código de barras o QR
        self.print_button = tk.Button(self.image_frame, text="Generar Código de Barras o QR", command=self.print_code)
        self.print_button.grid(row=1, column=0, padx=5, pady=5)

        # Frame para mostrar lista de elementos
        self.list_frame = ttk.LabelFrame(self.root, text="Lista de Items")
        self.list_frame.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        self.items_tree = ttk.Treeview(self.list_frame, columns=("ID", "Nombre", "Código de Barras", "Cantidad", "QR"), show="headings")
        self.items_tree.heading("ID", text="ID")
        self.items_tree.heading("Nombre", text="Nombre")
        self.items_tree.heading("Código de Barras", text="Código de Barras")
        self.items_tree.heading("Cantidad", text="Cantidad")
        self.items_tree.heading("QR", text="QR")
        self.items_tree.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        scrollbar = ttk.Scrollbar(self.list_frame, orient="vertical", command=self.items_tree.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.items_tree.configure(yscrollcommand=scrollbar.set)

        # Status Label
        self.status_label = tk.Label(self.root, text="", fg="red")
        self.status_label.grid(row=3, column=0, padx=10, pady=5)
    
    def get_selected_item(self):
    # Obtener el elemento seleccionado en la lista de elementos
        selected_item = self.items_tree.selection()
        if selected_item:
        # Obtener los valores del elemento seleccionado
            item_values = self.items_tree.item(selected_item, 'values')
            return item_values
        else:
        # Si no se seleccionó ningún elemento, devolver None
            return None



    def display_items(self, items):
        # Limpiar árbol de elementos
        for item in self.items_tree.get_children():
            self.items_tree.delete(item)

        # Obtener todos los items y mostrarlos en el árbol
        for row in items:
            self.items_tree.insert('', 'end', values=row)

    def show_code_image(self, image_path):
        try:
            image = tk.PhotoImage(file=image_path)
            self.barcode_image_label.config(image=image)
            self.barcode_image_label.image = image
        except Exception as e:
            print("Error al mostrar la imagen del código:", e)

    def print_code(self):
        selected_item = self.get_selected_item()
        if selected_item:
            name, barcode, quantity, qr_code = selected_item
            # Generar código QR
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(f"Nombre: {name}\nCódigo de Barras: {barcode}\nCantidad: {quantity}")
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")

            # Guardar el código QR temporalmente en un archivo
            qr_code_path = "temp_qr_code.png"
            img.save(qr_code_path)

            # Mostrar el código QR en la interfaz
            self.show_code_image(qr_code_path)

            # Eliminar el archivo temporal después de mostrar el código QR
            os.remove(qr_code_path)


