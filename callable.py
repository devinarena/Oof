
import interpreter

class Callable:
    def __init__(self):
        self.arity = 0

    def call(self, interpreter, arguments: list) -> object:
        pass
    
    def __str__(self) -> str:
        return self.__class__.__name__