import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import json
import os
import sqlite3

# --- DATOS Y FUNCIONALIDAD ---

libros = []
clientes = []
ventas = []

def conectar_bd():
    try:
        conexion = sqlite3.connect("libreria.db")
        print("Conectado a la base de datos correctamente.")
        return conexion
    except sqlite3.Error as e:
        print("Error al conectar a la base de datos:", e)
        return None

def guardar_datos():
    with open("libros.txt", "w") as f:
        json.dump(libros, f)
    with open("clientes.txt", "w") as f:
        json.dump(clientes, f)
    with open("ventas.txt", "w") as f:
        json.dump(ventas, f)

def cargar_datos():
    global libros, clientes, ventas
    if os.path.exists("libros.txt"):
        with open("libros.txt", "r") as f:
            libros[:] = json.load(f)
    if os.path.exists("clientes.txt"):
        with open("clientes.txt", "r") as f:
            clientes[:] = json.load(f)
    if os.path.exists("ventas.txt"):
        with open("ventas.txt", "r") as f:
            ventas[:] = json.load(f)

# --- MÓDULOS DE LA INTERFAZ ---

def modulo_inventario():
    ventana = tk.Toplevel()
    ventana.title("Inventario de Libros")
    ventana.geometry("500x400")
    ventana.config(bg="#f7f7f7")

    frame = tk.Frame(ventana, bg="#f7f7f7")
    frame.pack(pady=10)

    tk.Label(frame, text="Nombre del libro:").grid(row=0, column=0, sticky="e")
    entry_nombre = tk.Entry(frame, width=40)
    entry_nombre.grid(row=0, column=1)

    tk.Label(frame, text="Autor:").grid(row=1, column=0, sticky="e")
    entry_autor = tk.Entry(frame, width=40)
    entry_autor.grid(row=1, column=1)

    tk.Label(frame, text="Precio:").grid(row=2, column=0, sticky="e")
    entry_precio = tk.Entry(frame, width=40)
    entry_precio.grid(row=2, column=1)

    def agregar():
        nombre = entry_nombre.get()
        autor = entry_autor.get()
        try:
            precio = float(entry_precio.get())
        except:
            messagebox.showerror("Error", "Precio inválido.")
            return
        if nombre and autor:
            libros.append({"nombre": nombre, "autor": autor, "precio": precio})
            actualizar()
            entry_nombre.delete(0, tk.END)
            entry_autor.delete(0, tk.END)
            entry_precio.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Campos vacíos.")

    tk.Button(ventana, text="Agregar Libro", bg="#4CAF50", fg="white", command=agregar).pack(pady=5)

    lista = tk.Listbox(ventana, width=60)
    lista.pack(pady=10)

    def actualizar():
        lista.delete(0, tk.END)
        for libro in libros:
            lista.insert(tk.END, f"{libro['nombre']} | {libro['autor']} | Q{libro['precio']:.2f}")

    actualizar()

def modulo_clientes():
    ventana = tk.Toplevel()
    ventana.title("Gestión de Clientes")
    ventana.geometry("500x400")
    ventana.config(bg="#f0f0f0")

    frame = tk.Frame(ventana, bg="#f0f0f0")
    frame.pack(pady=10)

    tk.Label(frame, text="Nombre del cliente:").grid(row=0, column=0, sticky="e")
    entry_nombre = tk.Entry(frame, width=40)
    entry_nombre.grid(row=0, column=1)

    tk.Label(frame, text="NIT:").grid(row=1, column=0, sticky="e")
    entry_nit = tk.Entry(frame, width=40)
    entry_nit.grid(row=1, column=1)

    def agregar():
        nombre = entry_nombre.get()
        nit = entry_nit.get()
        if nombre and nit:
            clientes.append({"nombre": nombre, "nit": nit})
            actualizar()
            entry_nombre.delete(0, tk.END)
            entry_nit.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Campos vacíos.")

    tk.Button(ventana, text="Agregar Cliente", bg="#2196F3", fg="white", command=agregar).pack(pady=5)

    lista = tk.Listbox(ventana, width=60)
    lista.pack(pady=10)

    def actualizar():
        lista.delete(0, tk.END)
        for cliente in clientes:
            lista.insert(tk.END, f"{cliente['nombre']} - NIT: {cliente['nit']}")

    actualizar()

def modulo_ventas():
    ventana = tk.Toplevel()
    ventana.title("Realizar Venta")
    ventana.geometry("600x500")
    ventana.config(bg="#ffffff")

    if not clientes or not libros:
        messagebox.showwarning("Aviso", "Debe haber al menos un libro y un cliente.")
        ventana.destroy()
        return

    tk.Label(ventana, text="Seleccione Cliente:", bg="white").pack(pady=5)
    combo_clientes = ttk.Combobox(ventana, width=60, state="readonly")
    combo_clientes["values"] = [f"{c['nombre']} - NIT: {c['nit']}" for c in clientes]
    combo_clientes.pack()

    carrito = []
    lista_carrito = tk.Listbox(ventana, width=80)
    lista_carrito.pack(pady=10)

    tk.Label(ventana, text="Seleccione Libro:", bg="white").pack()
    combo_libros = ttk.Combobox(ventana, width=60, state="readonly")
    combo_libros["values"] = [f"{l['nombre']} - {l['autor']} - Q{l['precio']:.2f}" for l in libros]
    combo_libros.pack(pady=2)

    def agregar_libro():
        idx = combo_libros.current()
        if idx == -1:
            return
        cantidad = simpledialog.askinteger("Cantidad", "¿Cantidad a comprar?")
        if cantidad is None or cantidad < 1:
            return
        libro = libros[idx]
        subtotal = libro["precio"] * cantidad
        carrito.append({"libro": libro["nombre"], "cantidad": cantidad, "precio": libro["precio"], "subtotal": subtotal})
        lista_carrito.insert(tk.END, f"{cantidad} x {libro['nombre']} - Q{subtotal:.2f}")

    def finalizar_venta():
        if not carrito or combo_clientes.current() == -1:
            messagebox.showwarning("Advertencia", "Faltan datos para completar la venta.")
            return
        cliente = clientes[combo_clientes.current()]
        total = sum(item["subtotal"] for item in carrito)
        resumen = f"Cliente: {cliente['nombre']} - NIT: {cliente['nit']}\n"
        for item in carrito:
            resumen += f"{item['cantidad']} x {item['libro']} - Q{item['precio']:.2f} = Q{item['subtotal']:.2f}\n"
        resumen += f"\nTOTAL A PAGAR: Q{total:.2f}"
        messagebox.showinfo("Factura", resumen)
        ventas.append({"cliente": cliente, "detalle": carrito, "total": total})
        guardar_datos()
        ventana.destroy()

    tk.Button(ventana, text="Agregar Libro al Carrito", bg="#FF9800", fg="white", command=agregar_libro).pack(pady=5)
    tk.Button(ventana, text="Finalizar Venta", bg="#009688", fg="white", command=finalizar_venta).pack(pady=5)
    tk.Button(ventana, text="Guardar", bg="#4CAF50", fg="white", command=guardar_datos).pack(pady=5)
    tk.Button(ventana, text="Regresar", bg="#f44336", fg="white", command=ventana.destroy).pack(pady=5)

# --- VENTANA PRINCIPAL ---

def ventana_principal():
    cargar_datos()
    conectar_bd()

    root = tk.Tk()
    root.title("Sistema de Librería")
    root.geometry("500x400")
    root.config(bg="#e6e6e6")

    tk.Label(root, text="📚 Librería Rafa mi patron", font=("Helvetica", 18, "bold"), bg="#e6e6e6").pack(pady=20)

    tk.Button(root, text="📦 Módulo de Inventario", width=30, height=2, bg="#cce5ff", command=modulo_inventario).pack(pady=5)
    tk.Button(root, text="👤 Módulo de Clientes", width=30, height=2, bg="#d4edda", command=modulo_clientes).pack(pady=5)
    tk.Button(root, text="🧾 Módulo de Ventas", width=30, height=2, bg="#fff3cd", command=modulo_ventas).pack(pady=5)
    tk.Button(root, text="💾 Guardar y Salir", width=30, height=2, bg="#f8d7da", command=lambda: (guardar_datos(), root.destroy())).pack(pady=20)

    root.mainloop()

# --- INICIO DEL PROGRAMA ---
if __name__ == "__main__":
    ventana_principal()
