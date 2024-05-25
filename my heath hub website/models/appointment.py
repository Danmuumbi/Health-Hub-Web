from models.base_model import BaseModel

class Appointment(BaseModel):
    def __init__(self, *args, **kwargs):
        self.patient_id = ""
        self.doctor_id = ""
        self.date = ""
        self.reason = ""
        super().__init__(*args, **kwargs)
