import socket
import re
from common_ports import ports_and_services


def get_open_ports(target, port_range, verbose=False):
    is_ip = False
    ip_address = ""

    # Check if target matches IP format (e.g. 192.168.1.1 or invalid 266.255.55.555)
    if re.match(r"^[0-9.]+$", target):
        is_ip = True
        # Validate IPv4 format
        parts = target.split(".")
        if len(parts) != 4:
            return "Error: Invalid IP address"
        for part in parts:
            if not part.isdigit() or int(part) < 0 or int(part) > 255:
                return "Error: Invalid IP address"
        ip_address = target
    else:
        # Validate and resolve Hostname
        try:
            ip_address = socket.gethostbyname(target)
        except socket.gaierror:
            return "Error: Invalid hostname"

    open_ports = []

    # Scan ports with low timeout to pass execution limit
    for port in range(port_range[0], port_range[1] + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)

        result = sock.connect_ex((ip_address, port))
        if result == 0:
            open_ports.append(port)

        sock.close()

    # Format output for verbose mode
    if verbose:
        if is_ip:
            try:
                hostname = socket.gethostbyaddr(ip_address)[0]
                output = f"Open ports for {hostname} ({ip_address})\nPORT     SERVICE"
            except (socket.herror, socket.gaierror):
                output = f"Open ports for {ip_address}\nPORT     SERVICE"
        else:
            output = f"Open ports for {target} ({ip_address})\nPORT     SERVICE"

        for port in open_ports:
            service_name = ports_and_services.get(port, "unknown")
            output += f"\n{port:<9}{service_name}"

        return output

    return open_ports