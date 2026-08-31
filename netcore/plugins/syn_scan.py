from scapy.layers.inet import IP, TCP
from scapy.sendrecv import sendp
from scapy.layers.l2 import Ether
from scapy.arch import get_if_hwaddr
from scapy.config import conf
from scapy.all import RandShort, RandInt, AsyncSniffer
from .support.base_class import BasePlugin
from core.models import ScanContext, Status
from socket import gethostbyname
import ctypes, sys
import subprocess
import re
from time import sleep

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

            received_packet = self.initiate_transmission(target_port = context.job.port, 
                                                        ip = context.job.target,
                                                        packet_former = self.packet_former,
                                                        response_bpf = self.response_bpf,
                                                        timeout = context.config.syn_timeout)
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

        if 'SA' in str(flags):
            context.result.status = Status.OPEN

        elif 'R' in str(flags):
            context.result.status = Status.CLOSED

        else:
            context.result.status = Status.FILTERED
            context.result.error['syn'] = 'Unexpected Flags'

    def get_system_gateway_mac(self,gateway_ip):
        try:
            output = subprocess.check_output(["arp", "-a", gateway_ip], text=True)
            match = re.search(r"([0-9a-fA-F]{2}[-:]){5}[0-9a-fA-F]{2}", output)
            if match:
                return match.group(0).replace("-", ":")
        except Exception:
            pass

        raise ValueError("Couldnt resolve gateway mac address")

    @staticmethod
    def packet_former(gateway_mac, my_mac, my_ip, target_ip, srcport,target_port):

        _seq = int(RandInt())

        packet = (Ether(dst= gateway_mac, src= my_mac)/
                IP(src=my_ip, dst=target_ip) /
                TCP(sport= srcport,dport=target_port, flags="S", seq = _seq)
                )

        return packet

    @staticmethod
    def response_bpf(target_ip, my_ip, target_port, srcport):
        bpf = (
                f"tcp and src host {target_ip} and dst host {my_ip} "
                f"and src port {target_port} and dst port {srcport}"
                )
        return bpf

    def initiate_transmission(self, target_port, ip, packet_former, response_bpf, timeout):

        srcport = int(RandShort())

        target_ip = gethostbyname(ip)
        my_mac = get_if_hwaddr(conf.iface)
        my_iface, my_ip, gateway = conf.route.route(target_ip)
        gateway_mac = self.get_system_gateway_mac(gateway)

        packet = packet_former(gateway_mac=gateway_mac, my_mac=my_mac, my_ip=my_ip, target_ip=target_ip, srcport=srcport, target_port=target_port)

        bpf = response_bpf(target_ip= target_ip, my_ip= my_ip, target_port= target_port, srcport= srcport)


        sniffer = AsyncSniffer(iface=my_iface, filter=bpf, store=True)
        sniffer.start()

        sleep(0.1)
        sendp(packet, iface=my_iface, verbose=False)

        sleep(timeout)
        responses = sniffer.stop()

        return responses[0] if responses else None
