from repositories.notification_repository import create_notification


def send_confirmation(appointment_id):
    notification = create_notification(appointment_id, "confirmation")

    if notification is None:
        print(f"Notification already exists for appointment {appointment_id}")
        return

    print(f"📨 Sending confirmation for appointment {appointment_id}")

    # Later:
    # send WhatsApp / email here

    print(f"✅ Confirmation sent for appointment {appointment_id}")
