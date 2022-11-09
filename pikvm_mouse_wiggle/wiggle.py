#!/usr/bin/python3 -u
# https://github.com/pikvm/pikvm/issues/786#issuecomment-1196425318

import argparse
from contextlib import contextmanager
import json
import ssl
import time
import websocket


@contextmanager
def connect(hostname, username, password):
    uri = f"wss://{hostname}/api/ws?stream=0"
    headers = {"X-KVMD-User": username, "X-KVMD-Passwd": password}

    ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})
    ws.connect(uri, header=headers)

    yield ws

    ws.close()


def wiggle(hostname, username, password, delay_secs):
    positions = [
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (0, 0),
    ]

    while True:
        with connect(hostname, username, password) as ws:
            print('.', end='')

            for x, y in positions:
                ws.send(json.dumps({
                    "event_type": "mouse_move",
                    "event": {
                        "to": {
                            "x":x,
                            "y":y
                        }
                    }
                }))

                time.sleep(0.1)

        time.sleep(delay_secs)

