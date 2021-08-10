import time
import traceback


def every(delay, task):

    next_time = time.time() + delay
    while True:
        time.sleep(max(0, next_time - time.time()))
        try:
            task()
        except Exception:
            traceback.print_exc()
        next_time += (time.time() - next_time) // delay * delay + delay
