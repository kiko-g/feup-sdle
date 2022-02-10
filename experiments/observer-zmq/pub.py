from __future__ import annotations
from abc import ABC, abstractmethod
import sub


class Publisher(ABC):
    @abstractmethod
    def attach(self, subscriber: sub.Subscriber) -> None:
        """
        Attach n subscriber to the publisher.
        """
        pass

    @abstractmethod
    def detach(self, subscriber: sub.Subscriber) -> None:
        """
        Detach a subscriber from the publisher.
        """
        pass

    @abstractmethod
    def notify(self) -> None:
        """
        Notify all subscribers about an event.
        """
        pass
