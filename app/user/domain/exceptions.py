class EmailAlreadyExistsException(Exception):
    def __init__(self, email: str):
        self.email = email
        self.status_code = 401
        self.detail = f"Email {email} ya existe en el sistema."
        super().__init__()


class ValidateCharacterPasswordException(Exception):
    def __init__(self):
        self.status_code = 400
        self.detail = "La contraseña debe contener minimo 8 caracteres."
        super().__init__()
