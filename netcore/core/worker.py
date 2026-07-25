from core.plugin_manager import *
from core.models import ScanContext
from core.config import ScanConfig

def Worker(job_queue,result_queue,config: ScanConfig, Plugins: list):

    while True:
        plugin_manager = PluginManager(Plugins)
        job = job_queue.get()
        context = ScanContext(config, job)
        plugin_manager.execute(context)
        result_queue.put(context.result)
        job_queue.task_done()
