import subprocess
import time
from typing import Callable


def run_with_polling(
    poll_callback: Callable[[subprocess.Popen], None] | None = None,
    poll2_callback: Callable[[subprocess.Popen], None] | None = None,
    poll_delay_secs: int | float = 0.5,
    poll2_delay_secs: int | float = 0.5,
    *args,
    **kwargs
) -> None:
    """A wrapper around subprocess.run() which polls the child process every
    <poll_delay_secs> until the process exits."""
    assert poll_delay_secs < poll2_delay_secs

    p = subprocess.Popen(*args, **kwargs)

    start = time.time()

    finished = False
    while not finished:
        if p.poll() is not None:
            finished = True
            break

        if poll_callback is not None:
            poll_callback(p)

        time.sleep(poll_delay_secs)

        now = time.time()
        delay = now - start
        if delay >= poll2_delay_secs:
            if poll2_callback is not None:
                poll2_callback(p)
            start = now
