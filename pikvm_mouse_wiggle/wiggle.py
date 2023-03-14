#!/usr/bin/python3 -u
# https://github.com/pikvm/pikvm/issues/786#issuecomment-1196425318

from contextlib import contextmanager
import json
import logging
import ssl
import time
import websocket

logger = logging.getLogger(__name__)


@contextmanager
def connect(hostname: str, username: str, password: str) -> websocket.WebSocket:
    """A context manager that opens a websocket connection to a PiKVM websocket server,
    and yields the socket. The connection is closed when the context finishes."""
    uri = f"wss://{hostname}/api/ws?stream=0"
    headers = {"X-KVMD-User": username, "X-KVMD-Passwd": password}

    ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})
    ws.connect(uri, header=headers)

    yield ws

    ws.close()


def wiggle(
    hostname: str,
    username: str,
    password: str,
    delay_secs: float | int = 0,
    ignore_errors: bool = True,
) -> None:
    """Move the mouse in the top-left corner of the screen on the given VNC server, and
    optionally do this at a regular interval.

    hostname, username and password are the VNC server connection details.

    delay_secs, if non-zero and positive, will cause the function to enter a loop which
    performs the mouse movement every <delay_secs> seconds. The only way to interrupt
    this, if ignore_errors is also True, is to use Ctrl+C.

    ignore_errors, if True, will suppress any errors encountered while communicating
    with VNC, such as if the server is down."""
    positions = [
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (0, 0),
    ]

    def _wiggle() -> None:
        try:
            with connect(hostname, username, password) as ws:
                logger.debug("connected to %s, sending mouse moves", hostname)

                for x, y in positions:
                    ws.send(
                        json.dumps(
                            {
                                "event_type": "mouse_move",
                                "event": {"to": {"x": x, "y": y}},
                            }
                        )
                    )

                    time.sleep(0.1)

        except OSError as ex:
            if not ignore_errors:
                raise ex

            logger.error("connect error (ignoring): %s", ex)

    if delay_secs > 0:
        while True:
            _wiggle()

            time.sleep(delay_secs)

    else:
        _wiggle()
