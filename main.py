import threading
import queue
import time
from models import *
from config import *
from worker import worker
from formatter import *

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