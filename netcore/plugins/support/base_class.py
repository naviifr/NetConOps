import abc
from core.models import JobScope

class BasePlugin(abc.ABC):
    name = None
    dependency = None
    scope: JobScope = JobScope.PORT

    @abc.abstractmethod
    def execute(self, context):
        raise NotImplementedError