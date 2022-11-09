#!/usr/bin/python3 -u
# https://github.com/pikvm/pikvm/issues/786#issuecomment-1196425318

import argparse
from contextlib import contextmanager
import json
import ssl
import time
import websocket


def create_parser():
    # this method exists only so I can fold it and save some scrolling in my IDE...
    parser = argparse.ArgumentParser(description='Mouse wiggler for PIKVM')
    parser.add_argument('-H', '--hostname', help='Hostname or IP address of the PIKVM device', required=True)
    parser.add_argument('-u', '--username', help='Username for PIKVM web interface', default='admin')
    parser.add_argument('-p', '--password', help='Password for PIKVM web interface', default='admin')
    parser.add_argument('-d', '--delay', type=int, help='Delay between mouse wiggles', default=120)

    return parser


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
            print('moving to', end='')

            for x, y in positions:
                print(' ', (x, y), end='')

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

            print('')

        time.sleep(delay_secs)


args = create_parser().parse_args()

wiggle(
    args.hostname,
    args.username,
    args.password,
    args.delay,
)
