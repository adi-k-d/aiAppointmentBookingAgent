import time

from jobs.outbox_publisher import publish_events

if __name__ == "__main__":
    while True:
        try:
            publish_events()
        except Exception as e:
            print(f"publish failed: {e}")
        time.sleep(2)
