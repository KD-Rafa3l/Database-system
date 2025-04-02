# Manejo de facturación

import tkinter as tk
from tkinter import ttk, messagebox
from database import conectar_db

def mostrar_facturacion(root):
    ventana = tk.Toplevel(root)
    ventana.title("Módulo de Facturación")
    ventana.geometry("850x500")

    # Conectar a la base de datos
    db = conectar_db()
    cursor = db.cursor()

    # Función para cargar facturas en la tabla
    def cargar_facturas():
        for row in tabla.get_children():
            tabla.delete(row)  # Limpiar la tabla

        cursor.execute("SELECT id, cliente, fecha, total FROM facturas")
        for factura in cursor.fetchall():
            tabla.insert("", "end", values=factura)

    # Función para generar una factura
    def generar_factura():
        cliente = entry_cliente.get()
        productos = entry_productos.get()
        total = entry_total.get()

        if not cliente or not productos or not total:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
            return

        cursor.execute("INSERT INTO facturas (cliente, productos, total) VALUES (%s, %s, %s)",
                       (cliente, productos, total))
        db.commit()
        cargar_facturas()
        messagebox.showinfo("Éxito", "Factura generada correctamente.")

    # Función para eliminar una factura
    def eliminar_factura():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona una factura para eliminar.")
            return

        factura_id = tabla.item(seleccion[0])["values"][0]
        cursor.execute("DELETE FROM facturas WHERE id=%s", (factura_id,))
        db.commit()
        cargar_facturas()
        messagebox.showinfo("Éxito", "Factura eliminada.")

    # Tabla de facturas
    columnas = ("ID", "Cliente", "Fecha", "Total")
    tabla = ttk.Treeview(ventana, columns=columnas, show="headings")

    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=200)

    tabla.pack(pady=10)

    # Sección de entrada de datos
    frame_form = tk.Frame(ventana)
    frame_form.pack(pady=10)

    tk.Label(frame_form, text="Cliente:").grid(row=0, column=0)
    entry_cliente = tk.Entry(frame_form)
    entry_cliente.grid(row=0, column=1)

    tk.Label(frame_form, text="Productos:").grid(row=1, column=0)
    entry_productos = tk.Entry(frame_form)
    entry_productos.grid(row=1, column=1)

    tk.Label(frame_form, text="Total:").grid(row=2, column=0)
    entry_total = tk.Entry(frame_form)
    entry_total.grid(row=2, column=1)

    # Botones
    frame_botones = tk.Frame(ventana)
    frame_botones.pack(pady=10)

    btn_generar = tk.Button(frame_botones, text="Generar Factura", command=generar_factura)
    btn_generar.grid(row=0, column=0, padx=10)

    btn_eliminar = tk.Button(frame_botones, text="Eliminar Factura", command=eliminar_factura)
    btn_eliminar.grid(row=0, column=1, padx=10)

    btn_actualizar = tk.Button(frame_botones, text="Actualizar Lista", command=cargar_facturas)
    btn_actualizar.grid(row=0, column=2, padx=10)

    # Cargar datos al iniciar
    cargar_facturas()

    # Cerrar la base de datos cuando la ventana se cierre
    ventana.protocol("WM_DELETE_WINDOW", lambda: (db.close(), ventana.destroy()))
