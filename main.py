# Ventana principal con menú de navegación

import tkinter as tk
from modulos import ventas, compras, inventario, facturacion, personal

# Crear ventana principal
root = tk.Tk()
root.title("Sistema de Gestión")
root.geometry("600x400")

# Funciones para abrir módulos
def abrir_ventas():
    ventas.mostrar_ventas(root)

def abrir_compras():
    compras.mostrar_compras(root)

def abrir_inventario():
    inventario.mostrar_inventario(root)

def abrir_facturacion():
    facturacion.mostrar_facturacion(root)

def abrir_personal():
    personal.mostrar_personal(root)

# Botones para cada módulo
tk.Button(root, text="Ventas", command=abrir_ventas).pack(pady=10)
tk.Button(root, text="Compras", command=abrir_compras).pack(pady=10)
tk.Button(root, text="Inventario", command=abrir_inventario).pack(pady=10)
tk.Button(root, text="Facturación", command=abrir_facturacion).pack(pady=10)
tk.Button(root, text="Personal", command=abrir_personal).pack(pady=10)

root.mainloop()