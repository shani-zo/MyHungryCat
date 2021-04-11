import time
import sched
import imghdr


def run_periodically(func: callable, itter_time: int):
    """Create scheduler for running a function periodically"""
    scheduler = sched.scheduler(time.time, time.sleep)

    def run(scheduler):
        func()
        scheduler.enter(itter_time, 1, run, (scheduler,))
    scheduler.enter(itter_time, 1, run, (scheduler,))
    scheduler.run()


def is_image_file(file_path) -> bool:
    """
    Will return if the input file is an image file.

    Args:
        file_path: path to check

    Returns:
        Is the path given belongs to an image file

    Raises:
        FileNotFoundError if the image file doesn't exist.

    """
    return bool(imghdr.what(file_path))


