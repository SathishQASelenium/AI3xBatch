a = 10
class Counter:
    counter = 0  # class attribute, shared by all [static] instances of the class

    def __init__(self, name):
        self.name = name  # public
        self.__name_private = name  # private
        self._name_protected = name  # private

    @classmethod
    def total(cls):                # class method [Non-static method] can be mentioned as classmethod or not needed to mention as classmethod
        return cls.counter

    @staticmethod
    def is_valid(name):            # static method
        return bool(name.strip())