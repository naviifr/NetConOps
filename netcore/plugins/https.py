from .base_class import BasePlugin
from core.models import ScanContext
from plugins.http import HTTP

class HTTPS(BasePlugin):
    name = 'https'
    dependency = 'tls'

    def execute(self, context: ScanContext):

        if context.sock is None:
            return

        if context.result is None:
            return


        http = HTTP()
        sock = context.sock

        try:

            if 'tls' in context.result.plg_data:
                
                if context.result.plg_data['tls']["application_protocol"] == "http/1.0":

                    http.send_request(context.job.target, sock, "HTTP/1.0")
                    
                elif context.result.plg_data['tls']["application_protocol"] == "h2":
                    context.result.error["http"] = "h2 is not supported"
                    return

                else:

                    http.send_request(context.job.target, sock)

                data = http.receive_response(sock, context.config.header_size)

                results = http.parse_response(data)
                context.result.plg_data['https'] = results

        except Exception as e:
            context.result.error['https'] = str(e)
        