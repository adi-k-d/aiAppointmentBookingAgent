from rq import Worker

from jobs.queue import queue, redis_connection

if __name__ == "__main__":
    worker = Worker([queue], connection=redis_connection)
    worker.work(with_scheduler=True)
