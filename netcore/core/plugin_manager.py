from core.models import ScanContext, Status
from plugins import plugins_registry as plugins_registry

class PluginManager:

    def __init__(self, plugin_list: list):
        self.plugins = plugin_list
            
    def execute(self, context: ScanContext):
        
        try:
            for plugin in self.plugins:
                obj = plugin()

                if context.result.status not in (Status.OPEN, None):
                            continue
                
                obj.execute(context)

        finally:
            if hasattr(context, "sock"):
                context.sock.close()

