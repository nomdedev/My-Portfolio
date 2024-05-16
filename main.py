import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from controller import InventoryController

def main():
    root = tk.Tk()
    app = InventoryController()
    app.setup(root)  # Inicializa el controlador con la raíz de la ventana principal
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root, app))  # Configura la acción al cerrar la ventana
    root.mainloop()

def on_closing(root, controller):
    if messagebox.askokcancel("Salir", "¿Está seguro que desea salir?"):
        controller.save_data()  # Guarda los datos antes de salir
        root.destroy()

if __name__ == "__main__":
    main()
