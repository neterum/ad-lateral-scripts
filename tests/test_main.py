# tests/test_main.py
import re
import pytest
from ad_lateral_scripts.main import main

def test_main_smoke():
    rc = main([
        "-username", "jen",
        "-password", "Nexus123!",
        "-target_ip", "192.168.174.72",
        "-listen_address", "192.168.45.226",
        "-listen_port", "443",
        "-cimsession",
    ])
    assert isinstance(rc, int)
    
@pytest.mark.parametrize(
    "flag,pattern",
    [
        ("-cimsession", r"(powershell|Invoke-CimMethod|New-CimSession)"),
        ("-winrs",      r"(powershell|winrs|cmd\.exe)"),
        ("-pssession",  r"(New-PSSession|Enter-PSSession|Invoke-Command)"),
    ],
)
def test_main_produces_output_with_flags(flag, pattern, capsys):
    argv = [
        "-username", "jen",
        "-password", "Nexus123!",
        "-target_ip", "192.168.174.72",
        "-listen_address", "192.168.45.226",
        "-listen_port", "443",
        flag,
    ]
    rc = main(argv)
    out = capsys.readouterr().out

    assert rc == 0
    assert out.strip() != ""
    assert re.search(pattern, out, re.IGNORECASE), f"Output did not match {pattern!r}:\n{out}"