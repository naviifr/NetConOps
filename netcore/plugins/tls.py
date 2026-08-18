from .base_class import BasePlugin
from core.models import ScanContext, Status
from cryptography import x509
from cryptography.x509.oid import ExtensionOID
from cryptography.x509 import SubjectAlternativeName
import ssl

class TLS(BasePlugin):
    name = "tls"
    dependency = "tcp"

    def execute(self, context: ScanContext):

        sslcntxt = ssl.create_default_context()
        sslcntxt.check_hostname =  False
        sslcntxt.verify_mode =  ssl.CERT_NONE
        sslcntxt.set_alpn_protocols([
            # "h2",            # HTTP/2
            "http/1.1",      # HTTP/1.1
            "http/1.0",      # HTTP/1.0 
            "acme-tls/1",    # ACME
            "imap",          # IMAP
            "pop3",          # POP3
            "dot",           # DNS-over-TLS
            "mqtt",          # IoT Messaging
        ])

        if context.sock is None or context.result is  None:
            return 

        if context.result.status is not Status.OPEN:
            return
        
        try:
            sslsock = sslcntxt.wrap_socket(context.sock, server_hostname=context.job.target)
    
            cipher = sslsock.cipher()
            if cipher is None:
                context.result.error['tls'] = "cipher not found"
                return

            ver = sslsock.version()
            alpn = sslsock.selected_alpn_protocol()

            context.result.plg_data["tls"] = {
                'version' : str(ver),
                'cipher' :  cipher[0],
                'cipher_bits': cipher[2],
                'application_protocol': str(alpn)
            }

            der_cert= sslsock.getpeercert(binary_form=True)

            if der_cert:
                cert = x509.load_der_x509_certificate(der_cert)    #since cert verification is disabled, python doesnt store the certificate dictionary

                context.result.plg_data["tls"]["cert_subject"] = cert.subject.rfc4514_string()
                context.result.plg_data["tls"]["cert_issuer"] = cert.issuer.rfc4514_string()
                context.result.plg_data["tls"]["cert_valid_from"] = cert.not_valid_before_utc.isoformat()
                context.result.plg_data["tls"]["cert_valid_until"] = cert.not_valid_after_utc.isoformat()
                context.result.plg_data["tls"]["cert_serial_number"] = hex(cert.serial_number)

                try:
                    san = cert.extensions.get_extension_for_oid(ExtensionOID.SUBJECT_ALTERNATIVE_NAME)

                    if isinstance(san.value, SubjectAlternativeName):
                        san = san.value.get_values_for_type(x509.DNSName)
                        temp = ""
                        for i in san:
                            temp = temp + f"{i},\n\t\t   "

                        context.result.plg_data["tls"]["cert_SANs"]  = temp

                except x509.ExtensionNotFound as e:
                    context.result.error['tls'] = str(e)

            context.sock = sslsock                  
            
        except ssl.SSLError as e :
            if "WRONG_VERSION_NUMBER" in str(e):
                context.result.error['tls'] = "The port does not support SSL/TLS"
                context.sock = None
            else:
                context.result.error['tls'] = str(e)
        except ConnectionResetError as e:
            context.result.error['tls'] = str(e)
        except OSError as e:
            context.result.error['tls'] = str(e)
        except Exception as e:
            context.result.error['tls'] = str(e)


