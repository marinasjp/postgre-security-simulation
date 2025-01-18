
class Database:
    '''
    Clase que simula una base de datos.
    '''
    
    def __init__(self):
        self.clientes = [
                {"id": 1, "nombre": "Mario", "ciudad": "Nueva York", "edad": "22"},
                {"id": 2, "nombre": "Maria", "ciudad": "Londres", "edad": "23"},
                {"id": 3, "nombre": "Pedro", "ciudad": "Tokio", "edad": "24"},
                {"id": 4, "nombre": "Ana", "ciudad": "Paris", "edad": "25"}
            ]
        self.productos = [
                {"id": 1, "nombre": "Camiseta", "precio": 20},
                {"id": 2, "nombre": "Pantalón", "precio": 30},
                {"id": 3, "nombre": "Zapatos", "precio": 40},
                {"id": 4, "nombre": "Gorra", "precio": 10}
            ]
        
        self.ventas = [
                {"id": 1, "cliente_id": 1, "producto_id": 1},
                {"id": 2, "cliente_id": 2, "producto_id": 2},
                {"id": 3, "cliente_id": 1, "producto_id": 3},
                {"id": 4, "cliente_id": 2, "producto_id": 4},
                {"id": 5, "cliente_id": 1, "producto_id": 2}
            ]
    
    def fetch_data(self, table, columns):
        # Simulación de la base de datos
        table = getattr(self, table, None)
        if table is None:
            raise ValueError(f"Tabla {table} no existe.")
        
        result = []
        for row in table:
            filtered_row = {col: row.get(col, None) for col in columns}
            result.append(filtered_row)
        
        return result