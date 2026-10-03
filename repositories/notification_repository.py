from database import get_connection


def create_notification(appointment_id, type):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO notifications(appointment_id, type)
            VALUES (%s, %s)
            ON CONFLICT (appointment_id, type)
            DO NOTHING
            RETURNING id
            """,
            (appointment_id, type),
        )

        result = cursor.fetchone()
        connection.commit()

        return result

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()
