from sqlalchemy.dialects.postgresql import insert

from database import get_session
from models import Notification


def create_notification(appointment_id, type):
    statement = (
        insert(Notification)
        .values(appointment_id=appointment_id, type=type)
        .on_conflict_do_nothing(index_elements=["appointment_id", "type"])
        .returning(Notification.id)
    )

    with get_session() as session:
        return session.execute(statement).first()
