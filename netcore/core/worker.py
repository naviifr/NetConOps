from core.plugin_manager import *
from core.models import ScanContext, Result
from core.config import ScanConfig

def Worker(job_queue,result_queue,config: ScanConfig, Plugins: list):

    while True:
        plugin_manager = PluginManager(Plugins)
        job = job_queue.get()
        result = Result(job.target,job.port)
        context = ScanContext(config, job, result)
        plugin_manager.execute(context)
        result_queue.put(context.result)
        job_queue.task_done()
