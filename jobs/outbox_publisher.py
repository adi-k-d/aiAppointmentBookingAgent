from sqlalchemy import func, select

from database import get_session
from jobs.queue import queue
from models import OutboxEvent


def publish_events():
    with get_session() as session:
        events = session.scalars(
            select(OutboxEvent)
            .where(OutboxEvent.published_at.is_(None))
            .order_by(OutboxEvent.created_at)
        ).all()

        for event in events:
            queue.enqueue(
                "jobs.notifications.send_confirmation",
                str(event.aggregate_id),
            )
            event.published_at = func.now()
