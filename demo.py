"""Minimal demo showing that the strip_command() override is not needed
on the FITELnet driver.

Connects to a real F220 over SSH, runs ``show version``, and prints:

  - the raw value returned by ``send_command()``
  - the first line
  - whether the output starts with just the command (i.e. the hostname
    prefix has already been stripped by ``command_echo_read``)
  - whether the hostname ``TEST-HOST#`` appears anywhere in the output

The corresponding raw channel data is captured in ``session_log_ssh.log``
next to this script, so the wire-level echo can be compared against the
cleaned output.
"""
import os

from netmiko import ConnectHandler

HERE = os.path.dirname(os.path.abspath(__file__))
SESSION_LOG = os.path.join(HERE, "session_log_ssh.log")

device = {
    "device_type": "furukawa_fitelnet",
    "host": "192.168.100.160",
    "username": "operator",
    "password": "",
    "secret": "temp123",
    "session_log": SESSION_LOG,
    "session_log_file_mode": "write",
}


def main() -> None:
    with ConnectHandler(**device) as conn:
        output = conn.send_command("show version")

    print("=" * 70)
    print("send_command('show version') returned value (verbatim):")
    print("=" * 70)
    print(output)
    print("=" * 70)

    first_line = output.splitlines()[0] if output.splitlines() else ""
    print(f"first line                     : {first_line!r}")
    print(f"starts with 'show version'?    : {output.lstrip().startswith('show version')}")
    print(f"contains 'TEST-HOST#'?         : {'TEST-HOST#' in output}")
    print(f"length                         : {len(output)} chars")
    print("=" * 70)
    print(f"raw channel data captured at   : {SESSION_LOG}")


if __name__ == "__main__":
    main()
