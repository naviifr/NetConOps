import socket
from models import Job, Result, Status

def scan(job: Job,config):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(config.timeout)

    try:
        sock.connect((job.target, job.port,))
        result = Result(port=job.port, status=Status.OPEN, error=None)
        return result
    
    except TimeoutError:
        result = Result(port=job.port, status=Status.TIMEOUT)
        return result
    
    except ConnectionRefusedError as e:
        result = Result(port=job.port, status=Status.CLOSED, error=str(e))
        return result
    
    except socket.gaierror as e:
        result = Result(port=job.port, status=Status.DNS_ERROR, error=str(e))
        return result

    except OSError as e:
        result = Result(port=job.port, status=Status.UNREACHABLE, error=str(e))
        return result

    finally:
        sock.close() 
