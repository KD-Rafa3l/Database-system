# Gestión de ventas

import tkinter as tk
from tkinter import ttk, messagebox
from database import conectar_db

def mostrar_ventas(root):
    ventana = tk.Toplevel(root)
    ventana.title("Módulo de Ventas")
    ventana.geometry("700x400")

    # Conectar a la base de datos
    db = conectar_db()
    cursor = db.cursor()

    # Función para cargar las ventas en la tabla
    def cargar_ventas():
        for row in tabla.get_children():
            tabla.delete(row)  # Limpiar la tabla

        cursor.execute("SELECT id, producto, cantidad, precio, total FROM ventas")
        for venta in cursor.fetchall():
            tabla.insert("", "end", values=venta)

    # Función para agregar una venta
    def agregar_venta():
        producto = entry_producto.get()
        cantidad = entry_cantidad.get()
        precio = entry_precio.get()

        if not producto or not cantidad or not precio:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
            return
        
        try:
            cantidad = int(cantidad)
            precio = float(precio)
            total = cantidad * precio
        except ValueError:
            messagebox.showwarning("Error", "Cantidad y Precio deben ser numéricos.")
            return

        cursor.execute("INSERT INTO ventas (producto, cantidad, precio, total) VALUES (%s, %s, %s, %s)",
                       (producto, cantidad, precio, total))
        db.commit()
        cargar_ventas()
        messagebox.showinfo("Éxito", "Venta registrada correctamente.")

    # Función para borrar una venta
    def borrar_venta():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona una venta para eliminar.")
            return

        venta_id = tabla.item(seleccion[0])["values"][0]
        cursor.execute("DELETE FROM ventas WHERE id=%s", (venta_id,))
        db.commit()
        cargar_ventas()
        messagebox.showinfo("Éxito", "Venta eliminada.")

    # Tabla de ventas
    columnas = ("ID", "Producto", "Cantidad", "Precio", "Total")
    tabla = ttk.Treeview(ventana, columns=columnas, show="headings")
    
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=100)
    
    tabla.pack(pady=10)

    # Sección de entrada de datos
    frame_form = tk.Frame(ventana)
    frame_form.pack(pady=10)

    tk.Label(frame_form, text="Producto:").grid(row=0, column=0)
    entry_producto = tk.Entry(frame_form)
    entry_producto.grid(row=0, column=1)

    tk.Label(frame_form, text="Cantidad:").grid(row=1, column=0)
    entry_cantidad = tk.Entry(frame_form)
    entry_cantidad.grid(row=1, column=1)

    tk.Label(frame_form, text="Precio:").grid(row=2, column=0)
    entry_precio = tk.Entry(frame_form)
    entry_precio.grid(row=2, column=1)

    # Botones
    frame_botones = tk.Frame(ventana)
    frame_botones.pack(pady=10)

    btn_agregar = tk.Button(frame_botones, text="Agregar Venta", command=agregar_venta)
    btn_agregar.grid(row=0, column=0, padx=10)

    btn_eliminar = tk.Button(frame_botones, text="Eliminar Venta", command=borrar_venta)
    btn_eliminar.grid(row=0, column=1, padx=10)

    btn_actualizar = tk.Button(frame_botones, text="Actualizar Lista", command=cargar_ventas)
    btn_actualizar.grid(row=0, column=2, padx=10)

    # Cargar datos al iniciar
    cargar_ventas()

    # Cerrar la base de datos cuando la ventana se cierre
    ventana.protocol("WM_DELETE_WINDOW", lambda: (db.close(), ventana.destroy()))
    