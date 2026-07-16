from core.models import ScanContext, Plugin
import core.config as config
from plugins import plugins_registry as plugins_registry

class PluginManager:

    def __init__(self, plugin_list: list):
        
        self.plugins = []
        self.plugin_final = []
        
        for i in plugin_list:
            self.plugin_final.append(Plugin(i))

        for j in self.plugin_final:
            self.plugins.append((plugins_registry.Registry[j]))


    def execute(self, context: ScanContext, config : config.ScanConfig):
        
        try:
            for plugin in self.plugins:
                obj = plugin(context, config)
                obj.execute()

        finally:
            if context.sock:
                context.sock.close()

