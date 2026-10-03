import psycopg
from psycopg.types.json import Jsonb

from database import get_connection


def create_appointment(
    name,
    phone,
    starts_at,
    ends_at,
    doctor_id,
):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT id FROM doctors WHERE id = %s",
            (doctor_id,),
        )

        doctor = cursor.fetchone()

        if doctor is None:
            raise ValueError("Doctor does not exist")
        cursor.execute(
            """SELECT id FROM patients WHERE phone = %s""",
            (phone,),
        )

        patient = cursor.fetchone()

        if patient is None:
            cursor.execute(
                """
                INSERT INTO patients(name, phone)
                VALUES (%s, %s)
                RETURNING id
                """,
                (name, phone),
            )
            patient_id = cursor.fetchone()[0]
        else:
            patient_id = patient[0]

        cursor.execute(
            """
            INSERT INTO appointments
                (starts_at, ends_at, doctor_id, patient_id)
            VALUES
                (%s, %s, %s, %s)
            RETURNING id, doctor_id, starts_at, ends_at
            """,
            (starts_at, ends_at, doctor_id, patient_id),
        )

        appointment = cursor.fetchone()

        appointment_id = appointment[0]

        cursor.execute(
            """
            INSERT INTO outbox_events
                (event_type, aggregate_id, payload)
            VALUES
                (%s, %s, %s)
            """,
            (
                "appointment_created",
                appointment_id,
                Jsonb(
                    {
                        "appointment_id": str(appointment_id),
                        "patient_id": str(patient_id),
                        "doctor_id": str(doctor_id),
                    }
                ),
            ),
        )

        connection.commit()

        return appointment

    except psycopg.errors.ForeignKeyViolation:
        connection.rollback()
        raise ValueError("Doctor does not exist")

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()


def get_appointments(doctor_id=None, patient_id=None):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT a.id, p.name, a.starts_at, a.ends_at, a.doctor_id, a.patient_id
        FROM appointments a
        JOIN patients p ON p.id = a.patient_id
    """

    conditions = []
    params = []

    if doctor_id:
        conditions.append("a.doctor_id = %s")
        params.append(doctor_id)

    if patient_id:
        conditions.append("a.patient_id = %s")
        params.append(patient_id)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    cursor.execute(query, params)

    appointments = cursor.fetchall()

    cursor.close()
    connection.close()

    return appointments
