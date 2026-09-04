import queue
import core.models as models
import threading
import core.config as config
import core.worker as worker
import core.formatter.terminal as terminal
from plugins.support.plugins_registry import registry

class Engine():

    def __init__(self,target: str, ports: list, scan_config: config.ScanConfig, plugin_input: list):
        
        self.target = target
        self.ports = ports
        self.scan_config = scan_config
        self.plugins = plugin_input
    
    def _Dependency_check(self):

        plg_list =[]

        def resolve_dependency(temp_plg, plugin_exec: list):

            dependents = registry[temp_plg].dependency
                        
            if dependents is not None:
                if registry[dependents] not in plugin_exec:
                    resolve_dependency(dependents,plugin_exec)
                    if registry[dependents] not in plugin_exec:
                        plugin_exec.append((registry[dependents]))

            if registry[temp_plg] not in plugin_exec:
                plugin_exec.append((registry[temp_plg]))

        for i in self.plugins:
        
            resolve_dependency(i,plg_list)

        return plg_list
        

    def _Assign_Job(self):
        
        q = queue.Queue()

        for i in self.plugins:
            if i.scope == models.JobScope.HOST:
                job = models.Job(target=self.target, scope= models.JobScope.HOST)
                q.put(job)
                break

        for i in self.ports:
            job = models.Job(target=self.target, port=i, scope= models.JobScope.PORT)
            q.put(job)

        return q


    def _Wait(self, q: queue.Queue) -> None:
        
        q.join()


    def _Start_Worker(self):
        threads = []
        result_queue = queue.Queue()

        self.plugins = self._Dependency_check()
        job_queue = self._Assign_Job()

        for i in range(self.scan_config.worker):
            t = threading.Thread(target=worker.Worker, args=(job_queue, result_queue, self.scan_config, self.plugins), daemon=True)
            threads.append(t)

        for t in threads:
            t.start()

        self._Wait(job_queue)
        return result_queue
    
    
    def _Format_Results(self, result_queue: queue.Queue):
        
        results = terminal.get_results(result_queue)       
        return results

    def run(self):
        result_queue = self._Start_Worker()
        results = self._Format_Results(result_queue)
        return results
    

