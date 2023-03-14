import argparse
import os
import subprocess
import sys
import time

from pikvm_mouse_wiggle import wiggle
from pikvm_mouse_wiggle import run_with_polling


def create_parser():
    # this method exists only so I can fold it and save some scrolling in my IDE...
    parser = argparse.ArgumentParser(description="Mouse wiggler for PIKVM")
    parser.add_argument(
        "-H",
        "--hostname",
        help="Hostname or IP address of the PIKVM device",
        required=True,
    )
    parser.add_argument(
        "-u",
        "--username",
        help="Username for PIKVM web interface (can also be set via VNC_USERNAME)",
        default=os.getenv("VNC_USERNAME", "admin"),
    )
    parser.add_argument(
        "-p",
        "--password",
        help="Password for PIKVM web interface (can also be set via VNC_PASSWORD)",
        default=os.getenv("VNC_PASSWORD", "admin"),
    )
    parser.add_argument(
        "-d", "--delay", type=int, help="Delay between mouse wiggles", default=120
    )
    parser.add_argument(
        "--env",
        action="append",
        default=["VNC_USERNAME=%u", "VNC_PASSWORD=%p"],
        help="If running a command (see below), these are key=value pairs to add to the"
        "environment, subject to the same replacements as command",
    )
    parser.add_argument(
        "command",
        nargs="*",
        help="Optionally you can have pikvm-mouse-wiggle wrap a command, usually "
        "vncviewer. In this mode the script will invoke the command, setting any "
        "environment as per the --env argument, and then wiggle the mouse on the "
        "VNC server only for as long as that command is running. If the command "
        "exits (e.g. exit by the user, network error...) the script will stop as "
        "well. This avoids you needing your own scripts to invoke a VNC viewer "
        "pikvm-mouse-wiggle together. The command to run can contain the "
        "placeholders %%h, %%u and %%p, which are replaced by hostname, username"
        " and password respectively (e.g. 'vncviewer %h')",
    )

    return parser


def _main(args=None):
    if args is None:
        args = sys.argv[1:]

    args_namespace = create_parser().parse_args(args)

    # the script runs in two modes:
    # 1. if there is no command to run, we wiggle on an interval (just as v0.0.2 of this
    #    script did), and wiggle() supports this directly
    # 2. if there is a command to run, we instead use child.py to manage all the
    #    intervals and delays, as it also polls the child process to check it's alive

    print(args_namespace)
    if not args_namespace.command:
        wiggle(
            args_namespace.hostname,
            args_namespace.username,
            args_namespace.password,
            args_namespace.delay,
        )

    else:

        def _wiggle(p: subprocess.Popen) -> None:
            print("wiggle!", file=sys.stderr)
            wiggle(
                args_namespace.hostname,
                args_namespace.username,
                args_namespace.password,
            )

        def _replace_placeholders(s: str) -> str:
            for k, v in dict(hostname="%h", username="%u", password="%p").items():
                s = s.replace(v, getattr(args_namespace, k))
            return s

        cmd = [_replace_placeholders(c) for c in args_namespace.command]

        env = {}
        for e in args_namespace.env:
            p = e.split("=")
            env[p[0]] = _replace_placeholders(p[1])

        run_with_polling(
            poll2_delay_secs=args_namespace.delay,
            poll2_callback=_wiggle,
            args=cmd,
            env={
                **os.environ,
                **env,
            },
        )


def main(args=None):
    try:
        _main(args)
    except KeyboardInterrupt:
        pass  # suppress these
