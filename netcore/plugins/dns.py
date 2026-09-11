from .support.base_class import BasePlugin, JobScope
from core.models import ScanContext
import dns.resolver
import dns.exception

RECORD_TYPE = {
        "A": lambda r: str(r.address),
        "AAAA": lambda r: str(r.address),
        "NS": lambda r: str(r.target),
        "MX": lambda r: {
            "exchange": str(r.exchange),
            "preference": r.preference
        },
    }

class DNS(BasePlugin):
    name = 'dns'
    scope = JobScope.HOST

    def execute(self, context: ScanContext):

        context.result.plg_data['dns'] = {}
        try:
            for record, extract in RECORD_TYPE.items():
                answers = self.resolve_record(context.job.target, record)
                if answers:
                    context.result.plg_data['dns'][record] = [extract(i) for i in answers]

        except dns.exception.DNSException as error:
            context.result.error['dns'] = str(error)

    def resolve_record(self, target, record_type):
        try:
            return dns.resolver.resolve(target, record_type)
        except dns.resolver.NoAnswer:
            return None
