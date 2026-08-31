from scapy.layers.inet import IP, UDP, ICMP, IPerror, UDPerror
from scapy.layers.l2 import Ether
from socket import gethostbyname
from .support.base_class import BasePlugin
from core.models import ScanContext, Status
from plugins.syn_scan import SYN_Scan

privilege = None

class UDP_Scan(BasePlugin):

    name = 'udp'
    dependency = None

    def execute(self, context: ScanContext):

        syn = SYN_Scan()

        try:

            if privilege is None:
                if syn.privilege_check() is not True:
                    print("Warning: UDP scan requires admin/root privileges. " \
                          "Re-run this tool elevated, or remove -syn to use -tcp instead")
                    return
            elif not privilege:
                return

            received_packet = syn.initiate_transmission(target_port = context.job.port,
                                                        ip = context.job.target,
                                                        packet_former = self.packet_former,
                                                        response_bpf = self.response_bpf,
                                                        timeout = context.config.udp_timeout)
            self.parse_response(received_packet, context)

        except Exception as e:
            context.result.error['syn'] = str(e)

    @staticmethod
    def packet_former(gateway_mac, my_mac, my_ip, target_ip, target_port, srcport):

        packet = (Ether(dst= gateway_mac, src= my_mac)/
        IP(src=my_ip, dst=target_ip) /
        UDP(sport= srcport, dport=target_port)
            )
        return packet

    @staticmethod
    def response_bpf(target_ip, my_ip, target_port, srcport):

        bpf=(
            f"((udp and src host {target_ip} and dst host {my_ip} "
            f"and src port {target_port} and dst port {srcport}) "
            f"or (icmp and dst host {my_ip} and icmp[0] = 3 "
            f"and icmp[30:2] = {target_port}))"
        )
        return bpf

    def parse_response(self, packet, context: ScanContext):

        if packet is None:
            context.result.status = Status.TIMEOUT
            return

        if packet.haslayer(UDP) and not packet.haslayer(ICMP):
            context.result.status = Status.OPEN
            return

        if not packet.haslayer(ICMP):
            context.result.error['udp'] = 'Received an unexpected response'
            return

        icmp = packet[ICMP]
        quoted = icmp.payload
        if not quoted.haslayer(IPerror) or not quoted.haslayer(UDPerror):
            context.result.error['udp'] = 'ICMP response did not quote a UDP probe'
            return

        quoted_ip = quoted[IPerror]
        quoted_udp = quoted[UDPerror]
        target_ip = gethostbyname(context.job.target)
        if quoted_ip.dst != target_ip or quoted_udp.dport != context.job.port:
            context.result.error['udp'] = 'ICMP response was for another probe'
            return

        if icmp.type == 3 and icmp.code == 3:
            context.result.status = Status.CLOSED

        else:
            context.result.status = Status.FILTERED
            context.result.error['udp'] = (
                f'ICMP response type={icmp.type}, code={icmp.code}'
            )
        
