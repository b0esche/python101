from abc import ABC, abstractmethod


def add(a, b):
    return a + b


if add(5, 4) > 8:
    print(add(3, 2))


class Tier(ABC):
    age = int
    name = str

    def __init__(self, name=str, age=int):
        self.name = name
        self.age = age

    @abstractmethod
    def make_sound(self):
        pass

    def greet(self):
        print(f"Hi, my name is {self.name}! I am {self.age}!")


affe = Tier("Affe", 7)
affe.greet()
