import os
import logging
from uuid import UUID

from fastapi import FastAPI, HTTPException

from database import get_connection
from schemas import AppointmentCreate, AppointmentResponse, PatientCreate
from services.booking_service import book_appointment, get_appointment
from services.patient_service import register_patient

app = FastAPI()
logger = logging.getLogger(__name__)


@app.get("/")
def health_check():
    return {
        "Status": 200,
        "postgres": os.getenv("POSTGRES_URL"),
        "redis": os.getenv("REDIS_URL"),
    }


@app.get("/doctors")
def get_doctors():

    conn = get_connection()
    cursor = conn.cursor()

    doctors = cursor.execute("""select id ,name from doctors""").fetchall()
    cursor.close()
    return doctors


@app.post("/add-patient")
def create_patient(patient: PatientCreate):
    patient = register_patient(patient.name, patient.phone)
    return patient


@app.post("/book-appointment", response_model=AppointmentResponse)
def book_appointments(appointment: AppointmentCreate):
    try:
        return book_appointment(
            appointment.name,
            appointment.phone,
            appointment.starts_at,
            appointment.ends_at,
            appointment.doctor_id,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@app.get("/appointments")
def all_appointments(doctor_id: UUID | None = None, patient_id: UUID | None = None):
    try:
        return get_appointment(doctor_id, patient_id)
    except Exception as e:
        logger.exception("Failed to fetch appointments")
        raise HTTPException(
            status_code=500,
            detail="Unable to fetch appointments. Check the server logs for details.",
        ) from e
