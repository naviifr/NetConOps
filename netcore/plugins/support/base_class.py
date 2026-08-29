import abc

class BasePlugin(abc.ABC):
    name = None
    dependency = None

    @abc.abstractmethod
    def execute(self, context):
        raise NotImplementedError