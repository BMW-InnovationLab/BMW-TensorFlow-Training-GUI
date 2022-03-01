import socket
from typing import List
from domain.services.contract.abstract_port_scanner_service import AbstractPortScannerService
from shared.helpers.alias_provider_sql import get_all_ports


class PortScannerService(AbstractPortScannerService):

    def get_used_ports(self) -> List[str]:

        used_ports: List[str] = get_all_ports()

        for port in range(1, 65535):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((socket._LOCALHOST, port))
            if result == 0:
                used_ports.append(str(port))
            sock.close()

        return used_ports
