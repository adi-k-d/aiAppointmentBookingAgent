from database import get_session
from models import Patient


def create_patient(name, phone):
    with get_session() as session:
        patient = Patient(name=name, phone=phone)
        session.add(patient)
        session.flush()

        return {"id": patient.id, "name": patient.name, "phone": patient.phone}
