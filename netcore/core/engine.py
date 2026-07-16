import queue
import core.models as models
import threading
import core.config as config
import core.worker as worker
import core.formatter as formatter

class Engine():

    def __init__(self,target: str, ports: list, scan_config: config.ScanConfig, plugins: list):
        
        self.target = target
        self.ports = ports
        self.scan_config = scan_config
        self.plugins = plugins
    

    def _Assign_Job(self):
        
        q = queue.Queue()

        for i in self.ports:
            job = models.Job(self.target, port=i)
            q.put(job)

        return q


    def _Wait(self, q: queue.Queue) -> None:
        
        q.join()


    def _Start_Worker(self):
        threads = []
        result_queue = queue.Queue()
        q = self._Assign_Job()

        for i in range(self.scan_config.worker):
            t = threading.Thread(target=worker.Worker, args=(q, result_queue, self.scan_config, self.plugins), daemon=True)
            threads.append(t)

        for t in threads:
            t.start()

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
    

