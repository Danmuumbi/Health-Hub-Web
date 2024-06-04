"""import unittest
from models.patient import Patient
#from models.doctor import Doctor
from models.appointment import Appointment
from models.medication import Medication
from console import HealthHubCommand  # Import the HealthHubCommand class from console.py

class TestHealthHub(unittest.TestCase):
    def setUp(self):
        # Initialize test data
        self.patient = Patient(name="John Doe", age=30, medical_history="Some history", contact_info="123-456-7890")
        #self.doctor = Doctor(name="Dr. Smith", specialty="Cardiology", experience=5)
        self.appointment = Appointment(patient_id=self.patient.id, doctor_id=self.doctor.id, date="2024-06-01", reason="Checkup")
        self.medication = Medication(name="Aspirin", dosage="500mg", patient_id=self.patient.id)

    def test_create_patient(self):
        # Test creating a patient instance
        self.assertIsInstance(self.patient, Patient)

    def test_create_doctor(self):
        # Test creating a doctor instance
        #self.assertIsInstance(self.doctor, Doctor)

    def test_create_appointment(self):
        # Test creating an appointment instance
        self.assertIsInstance(self.appointment, Appointment)

    def test_create_medication(self):
        # Test creating a medication instance
        self.assertIsInstance(self.medication, Medication)

    def test_console_commands(self):
        # Test console commands
        cmd = HealthHubCommand()
        self.assertFalse(cmd.onecmd("create"))  # Test create command without arguments
        self.assertFalse(cmd.onecmd("show"))

if __name__ == '__main__':
    unittest.main()
"""