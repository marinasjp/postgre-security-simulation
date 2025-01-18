
class Database:
    def fetch_data(self, table):
        # Simulación de la base de datos
        if table == "clientes":
            return [
                {"id": 1, "nombre": "Mario", "ciudad": "Nueva York", "edad": "22"},
                {"id": 2, "nombre": "Maria", "ciudad": "Londres", "edad": "23"},
                {"id": 3, "nombre": "Pedro", "ciudad": "Tokio", "edad": "24"},
                {"id": 4, "nombre": "Ana", "ciudad": "Paris", "edad": "25"}
            ]
        elif table == "productos":
            return [
                {"id": 1, "nombre": "Camiseta", "precio": 20},
                {"id": 2, "nombre": "Pantalón", "precio": 30},
                {"id": 3, "nombre": "Zapatos", "precio": 40},
                {"id": 4, "nombre": "Gorra", "precio": 10}
            ]
            
        elif table == "ventas":
            return [
                {"id": 1, "cliente_id": 1, "producto_id": 1},
                {"id": 2, "cliente_id": 2, "producto_id": 2},
                {"id": 3, "cliente_id": 1, "producto_id": 3},
                {"id": 4, "cliente_id": 2, "producto_id": 4},
                {"id": 5, "cliente_id": 1, "producto_id": 2}
            ]                           
        else:
            return []