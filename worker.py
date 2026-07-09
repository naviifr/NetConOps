from tcp_connect import scan_port

def worker(job_queue,result_queue,config):

    while True:

        job = job_queue.get()
        result_queue.put(scan_port(job,config))
        job_queue.task_done()
