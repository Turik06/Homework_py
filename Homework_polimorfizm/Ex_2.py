class Mood:
    def __init__(self, mood="neutral"):
        self.mood = mood

    def greet(self):
        raise NotImplementedError()

    def be_strict(self):
        self.mood = "strict"

    def be_kind(self):
        self.mood = "kind"


class Father(Mood):
    def __init__(self, mood="neutral"):
        super().__init__(mood)

    def greet(self):
        return "Hello!"


class Mother(Mood):
    def __init__(self, mood="neutral"):
        super().__init__(mood)

    def greet(self):
        return "Hi, honey!"

    def be_kind(self):
        self.mood = "kind"


class Daughter(Father, Mother):
    def __init__(self, mood="neutral"):
        Father.__init__(self, mood)
        Mother.__init__(self, mood)

    def greet(self):
        return "Hi, honey!"


class Son(Father, Mother):
    def __init__(self, mood="neutral"):
        Father.__init__(self, mood)
        Mother.__init__(self, mood)

    def greet(self):
        return "Hello!"



father = Father()
mother = Mother()
daughter = Daughter()
son = Son()

print(father.greet())
print(mother.greet())
print(daughter.greet())
print(son.greet())

daughter.be_strict()
print(f"daughter's mood: {daughter.mood}")
son.be_kind()
print(f"son's mood: {son.mood}")
