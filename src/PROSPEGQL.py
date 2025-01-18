import requests
from cryptography.fernet import Fernet

class PROSPEGQL:
    def __init__(self, database, metadata_key):
        self.database = database
        self.metadata_key = metadata_key 
        self.data_key = ""

    def parse_query(self, query):
        # determina qué columnas y tablas está pidiendo el usuario.
        try:
            items = query.split(" FROM ")
            table, columns = items[1].split(" "), items[0].split("SELECT ")[1].split(",")
            return table[0], columns
        
        except IndexError:
            raise ValueError("SQL query invalida")

    def generate_acl(self, user, tabla):
        # Simplificación de la obtencion de las ACLs
        acl = {
            "Carmen": {
                "clientes": {
                    "id": ["read"], 
                    "nombre": ["read"], 
                    "ciudad": ["read"], 
                    "edad": ["read"]
                },
                "productos": { 
                    "id": ["read"],
                    "nombre": ["read", "write"],
                    "precio": ["read", "write"]},
                "ventas": {
                    "id": ["read"],
                    "fecha": ["read", "write"],
                    "cantidad": ["read", "write"],
                    "producto": ["read"]
                }
                
            },
            "Pepe": {
                "clientes": {
                    "id": ["read"], 
                    "nombre": ["read"], 
                    "ciudad": ["read"], 
                    "edad": ["read"]
                },
                "productos": {
                    "id": ["read"],
                    "nombre": ["read"],
                    "precio": ["read"]},
                "ventas": {
                    "id": ["read"],
                    "fecha": ["read"],
                    "cantidad": ["read"],
                    "producto": []
                },
                
                "Lucia": {
                    "clientes": {
                        "id": [], 
                        "nombre": ["read"], 
                        "ciudad": [], 
                        "edad": []
                    },
                    "productos": {
                        "id": ["read"],
                        "nombre": ["read"],
                        "precio": ["read"]},
                    "ventas": {
                        "id": [],
                        "fecha": [],
                        "cantidad": [],
                        "producto": []
                    }
                }
            }
        }

        return acl[user.name][tabla]

    def execute_query(self, table, columns, acl):
        # Comprobación de permisos
        for column in columns:
            if "read" not in acl[column.strip()]:
                raise PermissionError(f"Access denied for column: {column}")

        # Si usuario tiene permiso de leer, acceder a los datos
        # Asumimos que la base de datos tiene una llamada como fetch_data que devuelve los datos de la tabla
        data = self.database.fetch_data(table) 
        return data

    def get_key_from_AS(self, client):
        '''
        Manda un POST request al servidor de autenticación para que este compruebe si 
        el usuario esta autorizado y en ese caso devuelve el hash de su clave privada.
        '''
        
        url = "https://api.ejemplo.com/AS"
        data = {"cliente": client.name, "certificado_cliente": client.certificate}
        headers = {"Content-Type": "application/json"}

        try:
            hash_private_key = requests.post(url, data=data, headers=headers)
            hash_private_key.raise_for_status() 
            
            # Si el usuario no esta autorizado, se termina la operación
            if not hash_private_key:
                raise("Usuario no autorizado")
        
            return hash_private_key
        
        except requests.exceptions.RequestException as e:
            # print(f"Ha ocurrido un error durante la comunicación con el servidor de autenticación: {e}")
            return
        
    def sha256(self, input):
        '''
        Genera un hash según SHA256.
        Se deberá implementar según los estándares
        '''
        hash = ""
        return hash

    def generate_dinamic_key(self, client, metadata, worksheet_name):
        hash_AS = self.get_key_from_AS(client)
        hash_metadata = self.sha256(metadata)
        hash_worksheet_name = self.sha256(worksheet_name)
        
        # En el ensayo, utilizan la libreria CryptoJS para combinar estos hashes y generar la clave
        clave = self.generate_key(hash_AS, hash_metadata + hash_worksheet_name)
        
        return clave
    
    
    def generate_key(self, input1=None, input2=None, input3=None):
        '''
        función de generación de claves de cifrado
        Asumimos que se implementaría una función segura o se utilizaría una librería
        '''
        key = Fernet.generate_key()
        
        return key

    
    def encrypt_data(self, key, data):
        
        print("Datos antes del cifrado", data)
        
        cipher_suite = Fernet(key)
        encrypted_data = []
        for item in data:
            
            if type(item) == dict:
                encrypted_dict = {}
                for obj in item.keys():
                    name = cipher_suite.encrypt(obj.encode())
                    
                    if type(item[obj]) == list:
                        encrypted_list = []
                        for operation in item[obj]:
                            encrypted_list.append(cipher_suite.encrypt(str(operation).encode()))
                        value = encrypted_list
                    else:
                        value = cipher_suite.encrypt(str(item[obj]).encode())
                    
                    encrypted_dict[name] = value
                
                encrypted_data.append(encrypted_dict)
                
            else:
                encrypted_data.append(cipher_suite.encrypt(item.encode()))
        return encrypted_data
        
    def generate_container(self, table, data, acl, client):
        # Generación de contenedor simplificada
        
        
        # Los datos se cifran con una clave creada en el momento
        data_key = self.generate_dinamic_key(client, acl, table)
        self.data_key = data_key

        # Asumimos que se implementa una función de cifrado 
        # La tabla se cifra con la clave del AS
        encrypted_data = self.encrypt_data(data_key, data)
        
        # Los metadatos se cifran con una clave predeterminada
        metadata = self.encrypt_data(self.metadata_key, [acl])
        container = {
            "data": encrypted_data,
            "metadata": metadata
        }
        
        # Devolver resultados en formato BLOB
        return (container)

    def get_container(self, query, client):
        # 2.PROSPEGQL determina qué columnas y tablas está pidiendo el usuario.
        table, columns = self.parse_query(query)
        print("Se han determinado las columnas y la tabla que se han pedido. Tabla", table, "Columnas:", columns)
        
        # 3. genera una ACL preguntando a la base de datos sobre los privilegios de estas tablas y columnas. 
        acl = self.generate_acl(client, table)
        print("Se ha determinado la ACL del usuario", acl)
        
        # 4. PROSPEGQL realiza la query a la base de datos para obtener los resultados
        data = self.execute_query(table, columns, acl)
        print("Se ha ejecutado la query para obtener los datos según la acl. Datos:", data)
        
        # 5. Los resultados y la ACL se pasan a un generador de contenedores.
        container = self.generate_container(table, data, acl, client)

        return container
