from .support.base_class import BasePlugin, JobScope
from core.models import ScanContext
import socket
import ipaddress

class RevDNS(BasePlugin):
    name= "revdns"
    dependency= None
    scope = JobScope.HOST

    def execute(self, context:ScanContext):
        try:

            if not self.valid_ip(context.job.target):
                context.result.error['revdns'] = "The target should be an ip address"
                return

            dns = socket.gethostbyaddr(context.job.target)
            context.result.plg_data['revdns'] = {"hostname" : dns[0],
                                                 "aliases": dns[1],
                                                 "addresses": dns[2]}
            
            ip_check = socket.gethostbyname_ex(dns[0])
            if context.job.target in ip_check[2]:
                context.result.plg_data['revdns']["forward-confirmed"]  = True

            else:
                context.result.plg_data['revdns']["forward-confirmed"] = False
                context.result.plg_data['revdns']["alt-address"] = ip_check[2]

        except Exception as e:
            context.result.error['revdns'] = str(e)

    def valid_ip(self,ip: str) -> bool:
        
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False