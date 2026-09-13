from core.models import ScanContext, Status
from plugins.support import plugins_registry as plugins_registry

class PluginManager:

    def __init__(self, plugin_list: list):
        self.plugins = plugin_list
            
    def execute(self, context: ScanContext):
        
        try:
            for plugin in self.plugins:

                if context.job.scope != plugin.scope:
                    continue

                if context.result.status not in (Status.OPEN, None):
                    continue

                obj = plugin()
                obj.execute(context)

        finally:
            if hasattr(context, "sock"):
                context.sock.close()

