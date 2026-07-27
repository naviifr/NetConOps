from core.models import ScanContext
from plugins import plugins_registry as plugins_registry

class PluginManager:

    def __init__(self, plugin_list: list):
        self.plugins = plugin_list
            
    def execute(self, context: ScanContext):
        
        try:
            for plugin in self.plugins:
                obj = plugin()
                obj.execute(context)

        finally:
            if context.sock:
                context.sock.close()

