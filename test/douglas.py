
class Dog:
    def __init__(self, name):
        self.name = name
        self.hunger = 0
        self.happiness = 10

    def bark(self):
        return f"{self.name} says Woof!"

    def feed(self):
        self.hunger = max(0, self.hunger - 1)
        return f"{self.name} has been fed. Hunger: {self.hunger}"

    def play(self):
        self.happiness += 1
        return f"{self.name} is happy! Happiness: {self.happiness}"

    def __str__(self):
        return f"Dog: {self.name}, Hunger: {self.hunger}, Happiness: {self.happiness}"


douglas = Dog("Douglas")
print(douglas.bark())
print(douglas)
