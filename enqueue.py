from rq import Retry

from jobs.notifications import send_confirmation
from jobs.queue import queue

job = queue.enqueue(send_confirmation, 1, retry=Retry(max=3))

print(job)
