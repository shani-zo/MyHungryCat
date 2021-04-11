import time
import sched


def run_periodically(func, itter_time):
    """Create scheduler for running a function periodically"""
    scheduler = sched.scheduler(time.time, time.sleep)

    def run(scheduler):
        func()
        scheduler.enter(itter_time, 1, run, (scheduler,))
    scheduler.enter(itter_time, 1, run, (scheduler,))
    scheduler.run()