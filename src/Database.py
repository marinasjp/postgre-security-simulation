class Database:
    def fetch_data(self, table):
        # Simulación de la base de datos
        if table == "clientes":
            return [
                {"id": 1, "nombre": "Mario", "ciudad": "Nueva York", "edad": "22"},
                {"id": 2, "nombre": "Maria", "ciudad": "Londres", "edad": "23"}
            ]
        else:
            return []