
import token

class InterpreterError(Exception):
    
    def __init__(self, token: token.Token, message: str):
        super().__init__(message)
        self.message = message
        self.token = token

class ParseError(Exception):
    
    def __init__(self, token: token.Token, message: str) -> None:
        super().__init__(message)
        self.message = message
        self.token = token
    
class Return(Exception):

    def __init__(self, value: object) -> None:
        super().__init__(value)
        self.value = value