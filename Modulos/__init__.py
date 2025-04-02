# Hace que la carpeta sea un paquete importable

# Importa automáticamente los módulos cuando se importa "modulos"
from .ventas import mostrar_ventas
from .compras import mostrar_compras
from .inventario import mostrar_inventario
from .facturacion import mostrar_facturacion
from .personal import mostrar_personal

# Lista de módulos disponibles
__all__ = ["ventas", "compras", "inventario", "facturacion", "personal"]
