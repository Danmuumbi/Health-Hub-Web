"""from models.base_model import BaseModel
from models.patient import Patient
from models.doctor import Doctor
from models.appointment import Appointment
from models.medication import Medication

classes = {
    'BaseModel': BaseModel,
    'Patient': Patient,
    'Doctor': Doctor,
    'Appointment': Appointment,
    'Medication': Medication,
}

def initialize_storage():
    from models.engine.file_storage import FileStorage
    return FileStorage()

storage = initialize_storage()
storage.reload() """
from models.base_model import BaseModel
from models.patient import Patient
from models.doctor import Doctor
from models.appointment import Appointment
from models.medication import Medication
from models.engine.file_storage import FileStorage

classes = {
    'BaseModel': BaseModel,
    'Patient': Patient,
    'Doctor': Doctor,
    'Appointment': Appointment,
    'Medication': Medication,
}

storage = FileStorage()  # Initialize storage engine directly here
storage.reload()


