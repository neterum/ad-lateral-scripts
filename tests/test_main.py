# tests/test_main.py
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
