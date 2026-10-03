from repositories.patient_repository import create_patient


def register_patient(name, phone):
    return create_patient(name, phone)
