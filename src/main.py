
from PROSPEGQL import PROSPEGQL
from Database import Database
from User import User
from cryptography.fernet import Fernet


def decrypt_data(data):
    
    encrypted_data = []

    for results in data.keys():
        if results == "data":
            cipher_suite = Fernet(prospeql.data_key)
        else:
            cipher_suite = Fernet(metadatakey)
        
        for item in data[results]:
            
            if type(item) == dict:
                encrypted_dict = {}
                for obj in item.keys():
                    name = cipher_suite.decrypt(obj).decode()
                    
                    if type(item[obj]) == list:
                        encrypted_list = []
                        for operation in item[obj]:
                            unencrypted = cipher_suite.decrypt(operation).decode()
                            encrypted_list.append(unencrypted)
                        value = encrypted_list
                    else:
                        value = cipher_suite.decrypt(item[obj]).decode() 
                    
                    encrypted_dict[name] = value
                
                encrypted_data.append(encrypted_dict)
                
            else:
                encrypted_data.append(cipher_suite.decrypt(item).decode())
    return encrypted_data
    

def send_to_UI(resultados):
    '''
    Los resultados de la query se envían a una interfaz gráfica o aplicación
    La implementación de esta función dependerá de cómo visualizará el cliente los resultados.
    Los resultados están en formato BLOB.
    '''
    print("======== RESULTADOS DE LA QUERY ========")

    print("Resultados cifrados: \n")
    print(resultados)
    print()
    
    print("Resultados descifrados: \n")

    resultados_descifrados = decrypt_data(resultados)
    print(resultados_descifrados)
    
    print("======== FIN DE RESULTADOS ========")

def get_current_user():
    '''
    Obtener el usuario que hace la query.
    '''
    user = User ("Carmen", "gerente")
    return user


if __name__=="__main__":
    global metadatakey
    db = Database()
    metadatakey = Fernet.generate_key()
    prospeql = PROSPEGQL(db, metadatakey)
    
    client = get_current_user()


    try:
        # 1. Un usuario hace una query usando las funciones de PROSPEGQL
        query = "SELECT id, nombre, edad FROM clientes"
        print("El usuario", client.name, "ejecuta la query:", query)
        results = prospeql.get_container(query, client)
        
        send_to_UI(results) 
        
    except Exception as e:
        raise("Error:", e)