from repositories.appointment_repository import create_appointment, get_appointments


def book_appointment(name, phone, doctor_id, starts_at, ends_at):
    return create_appointment(name, phone, doctor_id, starts_at, ends_at)


def get_appointment(doctor_id, patient_id):
    return get_appointments(doctor_id, patient_id)
