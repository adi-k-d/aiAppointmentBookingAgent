from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class PatientCreate(BaseModel):
    name: str
    phone: str


class AppointmentCreate(BaseModel):
    name: str
    phone: str
    starts_at: datetime
    ends_at: datetime
    doctor_id: UUID


class AppointmentResponse(BaseModel):
    id: UUID
    name: str

    starts_at: datetime
    ends_at: datetime
    doctor_id: UUID
    patient_id: UUID
