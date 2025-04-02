# Gestión de compras

import tkinter as tk
from tkinter import ttk, messagebox
from database import conectar_db

def mostrar_compras(root):
    ventana = tk.Toplevel(root)
    ventana.title("Módulo de Compras")
    ventana.geometry("850x500")

    # Conectar a la base de datos
    db = conectar_db()
    cursor = db.cursor()

    # Función para cargar las compras en la tabla
    def cargar_compras():
        for row in tabla.get_children():
            tabla.delete(row)  # Limpiar la tabla

        cursor.execute("SELECT id, proveedor, producto, cantidad, total, metodo_pago FROM compras")
        for compra in cursor.fetchall():
            tabla.insert("", "end", values=compra)

    # Función para registrar una nueva compra
    def registrar_compra():
        proveedor = entry_proveedor.get()
        producto = entry_producto.get()
        cantidad = entry_cantidad.get()
        total = entry_total.get()
        metodo_pago = combo_metodo_pago.get()

        if not proveedor or not producto or not cantidad or not total or not metodo_pago:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
            return

        cursor.execute("INSERT INTO compras (proveedor, producto, cantidad, total, metodo_pago) VALUES (%s, %s, %s, %s, %s)",
                       (proveedor, producto, cantidad, total, metodo_pago))
        db.commit()
        cargar_compras()
        messagebox.showinfo("Éxito", "Compra registrada correctamente.")

    # Función para eliminar una compra
    def eliminar_compra():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona una compra para eliminar.")
            return

        compra_id = tabla.item(seleccion[0])["values"][0]
        cursor.execute("DELETE FROM compras WHERE id=%s", (compra_id,))
        db.commit()
        cargar_compras()
        messagebox.showinfo("Éxito", "Compra eliminada.")

    # Tabla de compras
    columnas = ("ID", "Proveedor", "Producto", "Cantidad", "Total", "Método de Pago")
    tabla = ttk.Treeview(ventana, columns=columnas, show="headings")

    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=140)

    tabla.pack(pady=10)

    # Sección de entrada de datos
    frame_form = tk.Frame(ventana)
    frame_form.pack(pady=10)

    tk.Label(frame_form, text="Proveedor:").grid(row=0, column=0)
    entry_proveedor = tk.Entry(frame_form)
    entry_proveedor.grid(row=0, column=1)

    tk.Label(frame_form, text="Producto:").grid(row=1, column=0)
    entry_producto = tk.Entry(frame_form)
    entry_producto.grid(row=1, column=1)

    tk.Label(frame_form, text="Cantidad:").grid(row=2, column=0)
    entry_cantidad = tk.Entry(frame_form)
    entry_cantidad.grid(row=2, column=1)

    tk.Label(frame_form, text="Total:").grid(row=3, column=0)
    entry_total = tk.Entry(frame_form)
    entry_total.grid(row=3, column=1)

    tk.Label(frame_form, text="Método de Pago:").grid(row=4, column=0)
    combo_metodo_pago = ttk.Combobox(frame_form, values=["Efectivo", "Transferencia", "Crédito"])
    combo_metodo_pago.grid(row=4, column=1)

    # Botones
    frame_botones = tk.Frame(ventana)
    frame_botones.pack(pady=10)

    btn_registrar = tk.Button(frame_botones, text="Registrar Compra", command=registrar_compra)
    btn_registrar.grid(row=0, column=0, padx=10)

    btn_eliminar = tk.Button(frame_botones, text="Eliminar Compra", command=eliminar_compra)
    btn_eliminar.grid(row=0, column=1, padx=10)

    btn_actualizar = tk.Button(frame_botones, text="Actualizar Lista", command=cargar_compras)
    btn_actualizar.grid(row=0, column=2, padx=10)

    # Cargar datos al iniciar
    cargar_compras()

    # Cerrar la base de datos cuando la ventana se cierre
    ventana.protocol("WM_DELETE_WINDOW", lambda: (db.close(), ventana.destroy()))