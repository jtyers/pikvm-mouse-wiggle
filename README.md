# pikvm-mouse-wiggle

Mouse wiggler for the PiKVM.

## What?

This is for where you have a system which you use via PiKVM which enacts a screen-saver, sleep or shutdown which you cannot change for whatever reason. `pikvm-mouse-wiggle` will connect to your PiKVM's API and simulate a mouse wiggle, just as if you'd uploaded a script via PiKVM's web console.

You can get USB dongles that perform this wiggling for you, but for PiKVM users this option is cheaper.

## Installation

Installation is via PyPI:
```
pip install pikvm-mouse-wiggle
```

This will give you the main script, `pikvm-mouse-wiggle`, and the `pikvm_mouse_wiggle` Python module.


## Usage

To start mouse-wiggling, specify the IP address (or hostname) of your PiKVM host, and the username and password you use to log into the web interface:

```
pikvm-mouse-wiggle -H 192.168.0.10 -u admin -p MyPassw0rd123
```

The script will now move the mouse by a few pixels every 120 seconds. Note that absolute positioning is currently used, so you may find the mouse movement annoying. To remedy this, increase the delay with `--delay <seconds>`.

Full usage:
```
usage: pikvm-mouse-wiggle [-h] -H HOSTNAME [-u USERNAME] [-p PASSWORD] [-d DELAY]

Mouse wiggler for PiKVM

options:
  -h, --help            show this help message and exit
  -H HOSTNAME, --hostname HOSTNAME
                        Hostname or IP address of the PiKVM device
  -u USERNAME, --username USERNAME
                        Username for PiKVM web interface
  -p PASSWORD, --password PASSWORD
                        Password for PiKVM web interface
  -d DELAY, --delay DELAY
                        Delay between mouse wiggles
```
You can also wiggle via Python directly if you so choose. Here's an example:

```python
from pikvm_mouse_wiggle import wiggle

wiggle(
    "hostname",
    "admin",
    "MyPassw0rd123",
    120,
)

```


# Licence

MIT Licence
