from scapy.layers.inet import IP, TCP
from scapy.sendrecv import sr1
from .base_class import BasePlugin
from core.models import ScanContext, Status
from socket import gethostbyname
import ctypes, sys

privilege = None

class SYN_Scan(BasePlugin):

    name = 'syn'
    dependency = None

    def execute(self, context: ScanContext):

        try:

            if privilege is None:
                if self.privilege_check() is not True:
                    print("Warning: SYN scan requires admin/root privileges. " \
                          "Re-run this tool elevated, or remove -syn to use -tcp instead")
                    return
            elif not privilege:
                return
            
            target_ip = gethostbyname(context.job.target)
            received_packet = sr1(
                (
                IP(dst=target_ip) /
                TCP(dport=context.job.port, flags="S")
                ),
                timeout=2,
                verbose=0
                )

            self.parse_response(received_packet, context)

        except Exception as e:
            context.result.error['syn'] = str(e)

    def privilege_check(self):
        global privilege
        if sys.platform == "win32":
            try:
                if ctypes.windll.shell32.IsUserAnAdmin() != 0:
                    privilege = True
                    return privilege
                else:
                    privilege = False
                    return privilege

            except Exception:
                privilege = False
                return False

    def parse_response(self, packet, context: ScanContext):

        if packet is None:
            context.result.status = Status.FILTERED
            return

        if not packet.haslayer(TCP):
            context.result.error['syn'] = 'Received non TCP response'
            return

        tcp_layer = packet[TCP]
        flags = tcp_layer.flags

        if str(flags) == 'SA':
            context.result.status = Status.OPEN

        elif str (flags) == 'RA':
            context.result.status = Status.CLOSED

        else:
            context.result.status = Status.FILTERED
            context.result.error['syn'] = 'Unexpected Flags'