from abc import ABCMeta, abstractmethod

class BaseFetcher(object, metaclass=ABCMeta):
    def __init__(self) -> None:
        """"""

    @abstractmethod
    def fetch_data(self, *ars, **kargs):
        """"""