class Animal:
    def __init__(self, name, species):
        self.name = name
        self.species = species

    def speak(self):
        return f"{self.name} makes a sound."

    def describe(self):
        return f"{self.name} is a {self.species}."

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name, "Dog")
        self.breed = breed

    def speak(self):
        return f"{self.name} barks!"

    def describe(self):
        return f"{self.name} is a {self.breed} {self.species}."

class Cat(Animal):
    def __init__(self, name, color):
        super().__init__(name, "Cat")
        self.color = color

    def speak(self):
        return f"{self.name} meows!"

    def describe(self):
        return f"{self.name} is a {self.color} {self.species}."

# Example usage
dog = Dog("Buddy", "Golden Retriever")
cat = Cat("Whiskers", "Black")

print(dog.describe())
print(dog.speak())
print(cat.describe())
print(cat.speak())