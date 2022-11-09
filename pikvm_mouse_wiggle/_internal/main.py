import argparse
import sys

from pikvm_mouse_wiggle import wiggle


def create_parser():
    # this method exists only so I can fold it and save some scrolling in my IDE...
    parser = argparse.ArgumentParser(description='Mouse wiggler for PIKVM')
    parser.add_argument('-H', '--hostname', help='Hostname or IP address of the PIKVM device', required=True)
    parser.add_argument('-u', '--username', help='Username for PIKVM web interface', default='admin')
    parser.add_argument('-p', '--password', help='Password for PIKVM web interface', default='admin')
    parser.add_argument('-d', '--delay', type=int, help='Delay between mouse wiggles', default=120)

    return parser


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    args_namespace = create_parser().parse_args(args)

    wiggle(
        args_namespace.hostname,
        args_namespace.username,
        args_namespace.password,
        args_namespace.delay,
    )

