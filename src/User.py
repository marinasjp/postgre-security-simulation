class User:
    def __init__(self, name):
        self.name = name
        self.certificate = self.create_cert()
        
    def create_cert(self):
        # Crea un certificado X.509 para el usuario
        self.certificate = "certificado"
        