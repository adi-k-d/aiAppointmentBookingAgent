from database import get_connection
from jobs.queue import queue


def publish_events():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, event_type, aggregate_id, payload
        FROM outbox_events
        WHERE published_at IS NULL
        ORDER BY created_at
        """
    )

    events = cursor.fetchall()

    for event_id, event_type, aggregate_id, payload in events:
        queue.enqueue(
            "jobs.notifications.send_confirmation",
            str(aggregate_id),
        )

        cursor.execute(
            """
            UPDATE outbox_events
            SET published_at = now()
            WHERE id = %s
            """,
            (event_id,),
        )

    connection.commit()

    cursor.close()
    connection.close()
