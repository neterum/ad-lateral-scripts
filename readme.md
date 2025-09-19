# Active Directory Lateral Scripts

OSCP Pen 200 course instructed students on copying and pasting various PowerShell commands to create a reverse shell with a Common Information Model.  Users had to manually adjust code for IP addresses, ports, usernames, and passwords.  Scripts in this repository will instead take in dynamic information as arguments and print out usable PowerShell that can be pasted into target's PowerShell command prompt. Users must specific a ```-wmi``` or ```-winrs``` flag to specify the connection method.

### Usage

```
python -m ad_lateral_scripts --help
usage: __main__.py [-h] -username USERNAME -password PASSWORD -target_ip TARGET_IP -listen_address LISTEN_ADDRESS -listen_port LISTEN_PORT (-cimsession | -winrs | -pssession)

Print a PowerShell wrapper holding a base64-encoded reverse shell.

options:
  -h, --help            show this help message and exit
  -username USERNAME    Username for PSCredential
  -password PASSWORD    Password for PSCredential
  -target_ip TARGET_IP  Target IP for CimSession
  -listen_address LISTEN_ADDRESS
                        IP address to connect back to
  -listen_port LISTEN_PORT
                        Port to connect back on
  -cimsession           Use WMI/CIM PowerShell
  -winrs                Use winrs CLI
  -pssession            Use PowerShell Remoting (PSSession)
```