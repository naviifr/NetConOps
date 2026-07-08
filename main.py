import socket
import threading
import queue
import time
from dataclasses import dataclass
from enum import Enum
from typing import Optional

WORKERS = 7
TIMEOUT = 2

class Status(Enum):
    OPEN = "Open"
    CLOSED = "Closed"
    TIMEOUT = "Timeout"
    UNREACHABLE = "Unreachable"
    DNS_ERROR = "DNS Resolution Failed"

@dataclass
class ScanConfig:
    timeout: int = TIMEOUT
    worker: int = WORKERS

@dataclass
class Job:
    target: str
    port: int

@dataclass
class Result:
    port: int
    status: Status
    error: Optional[str] = None

def worker(job_queue,result_queue,config):

    while True:

        job = job_queue.get()
        result_queue.put(scan_port(job,config))
        job_queue.task_done()

def scan_port(job: Job,config):

    sock = socket.socket()
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

def get_results(result_queue):
    
    a = []
    while  not result_queue.empty():
        a.append(result_queue.get())
    
    return a

def print_result(result_list):
    for i in result_list:
        print(i.port, ":", i.status.value, f"({i.error})" if i.error else "")


start = time.time()

q = queue.Queue()
result_queue = queue.Queue()
config = ScanConfig()


ports = [80,443,23,21,25,110,143,53,8080]

for i in ports:
    job = Job(target="google.com", port=i)
    q.put(job)

threads=[]

for i in range(config.worker):
    t = threading.Thread(target=worker, args=(q,result_queue,config,), daemon=True)         #creates threads(daemon=True will terminate the thread when the main program ends execution)
    threads.append(t)

for i in threads:
    i.start()

q.join()
final_result = get_results(result_queue)     #returning the results in a list form
print_result(final_result)

end = time.time()
print(end - start)                          #for calculating the execution time