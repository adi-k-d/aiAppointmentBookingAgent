from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from database import get_session
from models import Appointment, Doctor, OutboxEvent, Patient


def create_appointment(
    name,
    phone,
    starts_at,
    ends_at,
    doctor_id,
):
    with get_session() as session:
        try:
            if session.get(Doctor, doctor_id) is None:
                raise ValueError("Doctor does not exist")

            patient = session.scalars(
                select(Patient).where(Patient.phone == phone)
            ).first()

            if patient is None:
                patient = Patient(name=name, phone=phone)
                session.add(patient)
                session.flush()

            appointment = Appointment(
                starts_at=starts_at,
                ends_at=ends_at,
                doctor_id=doctor_id,
                patient_id=patient.id,
            )
            session.add(appointment)
            session.flush()

            session.add(
                OutboxEvent(
                    event_type="Appointment Created",
                    aggregate_id=appointment.id,
                    payload={
                        "appointment_id": str(appointment.id),
                        "patient_id": str(patient.id),
                        "doctor_id": str(doctor_id),
                    },
                )
            )

            return {
                "id": appointment.id,
                "name": patient.name,
                "doctor_id": appointment.doctor_id,
                "patient_id": appointment.patient_id,
                "starts_at": appointment.starts_at,
                "ends_at": appointment.ends_at,
            }

        except IntegrityError:
            # Doctor deleted between the existence check and the insert.
            raise ValueError("Doctor does not exist")


def get_appointments(doctor_id=None, patient_id=None):
    query = select(
        Appointment.id,
        Patient.name,
        Appointment.starts_at,
        Appointment.ends_at,
        Appointment.doctor_id,
        Appointment.patient_id,
    ).join(Patient, Patient.id == Appointment.patient_id)
    if doctor_id is not None:
        query = query.where(Appointment.doctor_id == doctor_id)

    if patient_id is not None:
        query = query.where(Appointment.patient_id == patient_id)

    with get_session() as session:
        return [dict(row) for row in session.execute(query).mappings()]
