
from PROSPEGQL import PROSPEGQL
from Database import Database
from User import User
from cryptography.fernet import Fernet
import configparser
import logging


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
    logging.info("======== RESULTADOS DE LA QUERY ========")

    logging.info("Resultados cifrados: \n%s", resultados)

    resultados_descifrados = decrypt_data(resultados)
    logging.info("Resultados descifrados: \n%s", resultados_descifrados)

    logging.info("======== FIN DE RESULTADOS ========")

def get_current_user(user_name):
    '''
    Obtener el usuario que hace la query.
    '''
    user = User (user_name)
    
    return user


def read_config():
    # Create a ConfigParser object
    config = configparser.ConfigParser()

    # Read the configuration file
    config.read('./config.ini')

    # Access values from the configuration file
    log_level = config.get('General', 'log_level')
    user = config.get('General', 'user')
    columns = config.get('General', 'columnas')
    tabla = config.get('General', 'tabla')
    db_name = config.get('Database', 'db_name')
    db_host = config.get('Database', 'db_host')
    db_port = config.get('Database', 'db_port')

    # Return a dictionary with the retrieved values
    config_values = {
        'log_level': log_level,
        'user': user,
        'columnas': columns,
        'tabla': tabla,
        'db_name': db_name,
        'db_host': db_host,
        'db_port': db_port
    }

    return config_values


if __name__=="__main__":
    config_data = read_config()
    if config_data['log_level'] == 'info':
        logging.basicConfig(filename="resultados_query_"+ config_data["user"] + ".log", level=logging.INFO)


    db = Database()
    metadatakey = Fernet.generate_key()
    prospeql = PROSPEGQL(db, metadatakey)
    
    client = get_current_user(config_data["user"])
        


    try:
        columns = config_data["columnas"]
        # 1. Un usuario hace una query usando las funciones de PROSPEGQL
        query = "SELECT " + columns + " FROM " + config_data["tabla"]
        logging.info("El usuario %s ejecuta la query: %s\n", client.name, query)
        results = prospeql.get_container(query, client)
        
        send_to_UI(results) 
        
    except Exception as e:
        print("Error:", e)