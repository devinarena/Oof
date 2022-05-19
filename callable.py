
import interpreter

class Callable:
    def __init__(self):
        pass

    def call(self, interpreter, arguments: list) -> object:
        pass

    def arity(self) -> int:
        return 0
    
    def __str__(self) -> str:
        return self.__class__.__name__