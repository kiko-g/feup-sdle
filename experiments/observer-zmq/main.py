from random import randrange
from typing import List
from pub import Publisher
from sub import Subscriber


class Teacher(Publisher):
    _state: int = None
    _subscribers: List[Subscriber] = []

    def attach(self, subscriber: Subscriber) -> None:
        print("Teacher: Attached a student.")
        self._subscribers.append(subscriber)

    def detach(self, subscriber: Subscriber) -> None:
        self._subscribers.remove(subscriber)

    def notify(self) -> None:
        print("Teacher: Notifying student...")
        for subscriber in self._subscribers:
            subscriber.update(self)

    def some_business_logic(self) -> None:
        print("\nTeacher: I'm doing something important.")
        self._state = randrange(0, 10)

        print(f"Teacher: My state has just changed to: {self._state}")
        self.notify()


class StudentA(Subscriber):
    def update(self, publisher: Publisher) -> None:
        if publisher._state < 3:
            print("StudentA: I need help")


class StudentB(Subscriber):
    def update(self, publisher: Publisher) -> None:
        if publisher._state == 0 or publisher._state >= 2:
            print("StudentB: I know the right answer")


if __name__ == "__main__":
    publisher = Teacher()
    subscriber_a = StudentA()
    subscriber_b = StudentB()

    publisher.attach(subscriber_a)
    publisher.attach(subscriber_b)

    publisher.some_business_logic()
    publisher.some_business_logic()

    publisher.detach(subscriber_a)

    publisher.some_business_logic()
