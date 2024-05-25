from models.base_model import BaseModel

class Doctor(BaseModel):
    def __init__(self, *args, **kwargs):
        self.name = ""
        self.specialty = ""
        self.experience = 0
        super().__init__(*args, **kwargs)
