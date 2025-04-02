# Control de stock

import tkinter as tk
from tkinter import ttk, messagebox
from database import conectar_db

def mostrar_inventario(root):
    ventana = tk.Toplevel(root)
    ventana.title("Módulo de Inventario")
    ventana.geometry("800x400")

    # Conectar a la base de datos
    db = conectar_db()
    cursor = db.cursor()

    # Función para cargar productos en la tabla
    def cargar_productos():
        for row in tabla.get_children():
            tabla.delete(row)  # Limpiar la tabla

        cursor.execute("SELECT id, nombre, categoria, stock, precio FROM inventario")
        for producto in cursor.fetchall():
            tabla.insert("", "end", values=producto)

        verificar_stock()

    # Función para agregar un nuevo producto
    def agregar_producto():
        nombre = entry_nombre.get()
        categoria = entry_categoria.get()
        stock = entry_stock.get()
        precio = entry_precio.get()

        if not nombre or not categoria or not stock or not precio:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
            return

        cursor.execute("INSERT INTO inventario (nombre, categoria, stock, precio) VALUES (%s, %s, %s, %s)",
                       (nombre, categoria, stock, precio))
        db.commit()
        cargar_productos()
        messagebox.showinfo("Éxito", "Producto agregado correctamente.")

    # Función para eliminar un producto
    def eliminar_producto():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona un producto para eliminar.")
            return

        producto_id = tabla.item(seleccion[0])["values"][0]
        cursor.execute("DELETE FROM inventario WHERE id=%s", (producto_id,))
        db.commit()
        cargar_productos()
        messagebox.showinfo("Éxito", "Producto eliminado.")

    # Función para editar un producto
    def editar_producto():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona un producto para editar.")
            return

        producto_id = tabla.item(seleccion[0])["values"][0]
        nuevo_nombre = entry_nombre.get()
        nueva_categoria = entry_categoria.get()
        nuevo_stock = entry_stock.get()
        nuevo_precio = entry_precio.get()

        if not nuevo_nombre or not nueva_categoria or not nuevo_stock or not nuevo_precio:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
            return

        cursor.execute("UPDATE inventario SET nombre=%s, categoria=%s, stock=%s, precio=%s WHERE id=%s",
                       (nuevo_nombre, nueva_categoria, nuevo_stock, nuevo_precio, producto_id))
        db.commit()
        cargar_productos()
        messagebox.showinfo("Éxito", "Producto actualizado correctamente.")

    # Función para verificar productos con bajo stock
    def verificar_stock():
        cursor.execute("SELECT nombre, stock FROM inventario WHERE stock < 5")
        productos_bajo_stock = cursor.fetchall()

        if productos_bajo_stock:
            mensaje = "\n".join([f"{producto[0]} - Stock: {producto[1]}" for producto in productos_bajo_stock])
            messagebox.showwarning("¡Atención!", f"Los siguientes productos tienen bajo stock:\n\n{mensaje}")

    # Tabla de productos
    columnas = ("ID", "Nombre", "Categoría", "Stock", "Precio")
    tabla = ttk.Treeview(ventana, columns=columnas, show="headings")

    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=150)

    tabla.pack(pady=10)

    # Sección de entrada de datos
    frame_form = tk.Frame(ventana)
    frame_form.pack(pady=10)

    tk.Label(frame_form, text="Nombre:").grid(row=0, column=0)
    entry_nombre = tk.Entry(frame_form)
    entry_nombre.grid(row=0, column=1)

    tk.Label(frame_form, text="Categoría:").grid(row=1, column=0)
    entry_categoria = tk.Entry(frame_form)
    entry_categoria.grid(row=1, column=1)

    tk.Label(frame_form, text="Stock:").grid(row=2, column=0)
    entry_stock = tk.Entry(frame_form)
    entry_stock.grid(row=2, column=1)

    tk.Label(frame_form, text="Precio:").grid(row=3, column=0)
    entry_precio = tk.Entry(frame_form)
    entry_precio.grid(row=3, column=1)

    # Botones
    frame_botones = tk.Frame(ventana)
    frame_botones.pack(pady=10)

    btn_agregar = tk.Button(frame_botones, text="Agregar Producto", command=agregar_producto)
    btn_agregar.grid(row=0, column=0, padx=10)

    btn_editar = tk.Button(frame_botones, text="Editar Producto", command=editar_producto)
    btn_editar.grid(row=0, column=1, padx=10)

    btn_eliminar = tk.Button(frame_botones, text="Eliminar Producto", command=eliminar_producto)
    btn_eliminar.grid(row=0, column=2, padx=10)

    btn_actualizar = tk.Button(frame_botones, text="Actualizar Lista", command=cargar_productos)
    btn_actualizar.grid(row=0, column=3, padx=10)

    # Cargar datos al iniciar
    cargar_productos()

    # Cerrar la base de datos cuando la ventana se cierre
    ventana.protocol("WM_DELETE_WINDOW", lambda: (db.close(), ventana.destroy()))
    