import queue
import models
import threading
import config
import worker
import formatter

class Engine():

    def __init__(self,target: str, ports: list, scan_config: config.ScanConfig):
        
        self.target = target
        self.ports = ports
        self.scan_config = scan_config
    

    def _Assign_Job(self):
        
        q = queue.Queue()

        for i in self.ports:
            job = models.Job(self.target, port=i)
            q.put(job)

        return q


    def _Wait(self, q: queue.Queue) -> None:
        
        q.join()


    def _Start_Worker(self):
        
        threads=[]
        result_queue= queue.Queue()
        q= self._Assign_Job()

        for i in range(self.scan_config.worker):
            t = threading.Thread(target=worker.Worker, args=(q,result_queue,self.scan_config,), daemon=True)         #creates threads(daemon=True will terminate the thread when the main program ends execution)
            threads.append(t)
        
        for i in threads:
            i.start()

        self._Wait(q)
        return result_queue
    
    
    def _Format_Results(self, result_queue: queue.Queue):
        
        results = formatter.get_results(result_queue)       
        return results

    def run(self):
        self._Assign_Job()
        result_queue = self._Start_Worker()
        results = self._Format_Results(result_queue)
        return results
    

