from __future__ import annotations
from abc import ABC, abstractmethod
import pub


class Subscriber(ABC):
    @abstractmethod
    def update(self, publisher: pub.Publisher) -> None:
        """
        Receive update from publisher.
        """
        pass
