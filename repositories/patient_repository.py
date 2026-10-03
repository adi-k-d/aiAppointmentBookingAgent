from database import get_connection


def create_patient(name, phone):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """insert into patients (name,phone) values (%s,%s) returning id,name,phone""",
        (name, phone),
    )
    patient = cursor.fetchone()
    connection.commit()

    cursor.close()
    connection.close()

    return patient
