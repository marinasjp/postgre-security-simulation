class User:
    def __init__(self, name, rol):
        self.name = name
        self.certificate = self.create_cert()
        self.rol = rol
        
    def create_cert(self):
        # Crea un certificado X.509 para el usuario
        self.certificate = "certificado"
        