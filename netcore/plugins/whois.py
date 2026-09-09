from .support.base_class import BasePlugin, JobScope
from core.models import ScanContext
import whoisdomain as whois
import ipwhois
import ipaddress
import re

class WhoIs(BasePlugin):
    name = "whois"
    scope = JobScope.HOST

    def execute(self, context: ScanContext):

        try:
            if self.valid_ip(context.job.target):
                if context.config.verbose:
                    context.result.plg_data['whois'] = self.ip_lookup(context.job.target)

                else:
                    context.result.plg_data['whois'] = self.clean_data(self.ip_lookup(context.job.target))

            elif self.valid_domain(context.job.target):
                if context.config.verbose:
                     context.result.plg_data['whois'] = self.domain_lookup(context.job.target)
                else: 
                    context.result.plg_data['whois'] = self.clean_data(self.domain_lookup(context.job.target))
                    
            else:
                context.result.error['whois'] = "Enter a valid ip/domain"

        except Exception as e:
            context.result.error['whois'] = str(e)


    def ip_lookup(self,ip):
        obj = ipwhois.IPWhois(ip)
        result = obj.lookup_rdap()
        return result

    def domain_lookup(self, domain):
        result = whois.query(domain)
        return result.__dict__

    def valid_ip(self,ip):
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False

    def valid_domain(self, domain):
        if len(domain) > 253:
            return False
        pattern = r"^(?=.{1,253}$)(?!-)(?:[A-Za-z0-9-]{1,63}\.)+[A-Za-z]{2,63}$"
        return bool(re.fullmatch(pattern, domain))

    def clean_data(self, data):
        
        if isinstance(data, dict):
            return {key: self.clean_data(value) for key, value in data.items() if value not in (None, "", "REDACTED FOR PRIVACY")}

        if isinstance(data, list):
            return [self.clean_data(value) for value in data if value not in (None, "", "REDACTED FOR PRIVACY")]

        return data


