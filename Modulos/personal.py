# Administración de empleados

import tkinter as tk
from tkinter import ttk, messagebox
from database import conectar_db

def mostrar_personal(root):
    ventana = tk.Toplevel(root)
    ventana.title("Módulo de Personal")
    ventana.geometry("750x400")

    # Conectar a la base de datos
    db = conectar_db()
    cursor = db.cursor()

    # Función para cargar los empleados en la tabla
    def cargar_empleados():
        for row in tabla.get_children():
            tabla.delete(row)  # Limpiar la tabla

        cursor.execute("SELECT id, nombre, cargo, horario FROM personal")
        for empleado in cursor.fetchall():
            tabla.insert("", "end", values=empleado)

    # Función para agregar un nuevo empleado
    def agregar_empleado():
        nombre = entry_nombre.get()
        cargo = entry_cargo.get()
        horario = entry_horario.get()

        if not nombre or not cargo or not horario:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
            return

        cursor.execute("INSERT INTO personal (nombre, cargo, horario) VALUES (%s, %s, %s)",
                       (nombre, cargo, horario))
        db.commit()
        cargar_empleados()
        messagebox.showinfo("Éxito", "Empleado agregado correctamente.")

    # Función para eliminar un empleado
    def eliminar_empleado():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona un empleado para eliminar.")
            return

        empleado_id = tabla.item(seleccion[0])["values"][0]
        cursor.execute("DELETE FROM personal WHERE id=%s", (empleado_id,))
        db.commit()
        cargar_empleados()
        messagebox.showinfo("Éxito", "Empleado eliminado.")

    # Función para editar un empleado
    def editar_empleado():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona un empleado para editar.")
            return

        empleado_id = tabla.item(seleccion[0])["values"][0]
        nuevo_nombre = entry_nombre.get()
        nuevo_cargo = entry_cargo.get()
        nuevo_horario = entry_horario.get()

        if not nuevo_nombre or not nuevo_cargo or not nuevo_horario:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
            return

        cursor.execute("UPDATE personal SET nombre=%s, cargo=%s, horario=%s WHERE id=%s",
                       (nuevo_nombre, nuevo_cargo, nuevo_horario, empleado_id))
        db.commit()
        cargar_empleados()
        messagebox.showinfo("Éxito", "Empleado actualizado correctamente.")

    # Tabla de empleados
    columnas = ("ID", "Nombre", "Cargo", "Horario")
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

    tk.Label(frame_form, text="Cargo:").grid(row=1, column=0)
    entry_cargo = tk.Entry(frame_form)
    entry_cargo.grid(row=1, column=1)

    tk.Label(frame_form, text="Horario:").grid(row=2, column=0)
    entry_horario = tk.Entry(frame_form)
    entry_horario.grid(row=2, column=1)

    # Botones
    frame_botones = tk.Frame(ventana)
    frame_botones.pack(pady=10)

    btn_agregar = tk.Button(frame_botones, text="Agregar Empleado", command=agregar_empleado)
    btn_agregar.grid(row=0, column=0, padx=10)

    btn_editar = tk.Button(frame_botones, text="Editar Empleado", command=editar_empleado)
    btn_editar.grid(row=0, column=1, padx=10)

    btn_eliminar = tk.Button(frame_botones, text="Eliminar Empleado", command=eliminar_empleado)
    btn_eliminar.grid(row=0, column=2, padx=10)

    btn_actualizar = tk.Button(frame_botones, text="Actualizar Lista", command=cargar_empleados)
    btn_actualizar.grid(row=0, column=3, padx=10)

    # Cargar datos al iniciar
    cargar_empleados()

    # Cerrar la base de datos cuando la ventana se cierre
    ventana.protocol("WM_DELETE_WINDOW", lambda: (db.close(), ventana.destroy()))
    