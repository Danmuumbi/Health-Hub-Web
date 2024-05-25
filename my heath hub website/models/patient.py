from models.base_model import BaseModel

class Patient(BaseModel):
    def __init__(self, *args, **kwargs):
        self.name = ""
        self.age = 0
        self.medical_history = ""
        self.contact_info = ""
        super().__init__(*args, **kwargs)
