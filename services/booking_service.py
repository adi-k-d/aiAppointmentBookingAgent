from repositories.appointment_repository import create_appointment, get_appointments


def book_appointment(name, phone, starts_at, ends_at, doctor_id):
    return create_appointment(name, phone, starts_at, ends_at, doctor_id)


def get_appointment(doctor_id, patient_id):
    return get_appointments(doctor_id, patient_id)
