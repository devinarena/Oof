
import token
import errors

values = {

}

def define(name: str, value: object) -> None:
    values[name] = value

def assign(name: str, value: object) -> None:
    if name.lexeme in values:
        values[name.lexeme] = value
        return
    
    raise errors.InterpreterError(name, "Undefined variable '" + name.lexeme + "'")

def get(name: token.Token) -> None:
    if values[name.lexeme]:
        return values[name.lexeme]
    
    raise errors.InterpreterError(name, "Undefined variable '" + name.lexeme + "'")