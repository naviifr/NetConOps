import tcp_connect

def Worker(job_queue,result_queue,config):

    while True:

        job = job_queue.get()
        result_queue.put(tcp_connect.scan(job,config))
        job_queue.task_done()
