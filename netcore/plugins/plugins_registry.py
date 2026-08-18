import pkgutil
import plugins
import importlib
import inspect
from .base_class import BasePlugin

def _plugin_discovery():

    temp_registry = {}

    for pkg in pkgutil.iter_modules(plugins.__path__):                 # Iterating every module in the plugins directory

        module = importlib.import_module("plugins." + pkg.name)        # Import those modules
        plugin_classes = inspect.getmembers(module, inspect.isclass)             # Importing all the classes present in the modules

        for name, plg_class in plugin_classes:
            if (                                                       # Checking if the plugin class is the subclass of BasePlugin and
            plg_class is not BasePlugin                                # we are importing the plugin class from the right plugin module
            and issubclass(plg_class, BasePlugin)
            and plg_class.__module__ == module.__name__
            ):
                if plg_class.name in temp_registry:                    # Ensures that no plugin has the same name
                    raise ValueError(f"Duplicate plugin name: '{plg_class.name}'")
                    
                temp_registry[plg_class.name] = plg_class

    return temp_registry


registry = _plugin_discovery()