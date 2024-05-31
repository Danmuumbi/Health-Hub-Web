from models.base_model import BaseModel

class Medication(BaseModel):
    def __init__(self, *args, **kwargs):
        self.name = ""
        self.dosage = ""
        self.patient_id = ""
        super().__init__(*args, **kwargs)
