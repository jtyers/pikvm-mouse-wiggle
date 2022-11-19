#!/usr/bin/python3 -u
# https://github.com/pikvm/pikvm/issues/786#issuecomment-1196425318

import argparse
from contextlib import contextmanager
import json
import logging
import ssl
import time
import websocket

logger = logging.getLogger(__name__)


@contextmanager
def connect(hostname, username, password):
    uri = f"wss://{hostname}/api/ws?stream=0"
    headers = {"X-KVMD-User": username, "X-KVMD-Passwd": password}

    ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})
    ws.connect(uri, header=headers)

    yield ws

    ws.close()


def wiggle(hostname, username, password, delay_secs, ignore_errors=True):
    positions = [
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (0, 0),
    ]

    while True:
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

        time.sleep(delay_secs)
