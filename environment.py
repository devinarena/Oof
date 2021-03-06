
import token
import errors

class Environment:
    def __init__(self, enclosing=None) -> None:
        self.values = {

        }
        self.enclosing = enclosing

    def define(self, name: str, value: object) -> None:
        self.values[name] = value

    def assign(self, name: str, value: object) -> None:
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return
        
        if self.enclosing:
            self.enclosing.assign(name, value)
            return
        
        raise errors.InterpreterError(name, "Undefined variable '" + name.lexeme + "'")
    
    def assign_at(self, distance: int, name: token.Token, value: object) -> None:
        self.ancestor(distance).values[name.lexeme] = value

    def get(self, name: token.Token) -> None:
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        
        if self.enclosing:
            return self.enclosing.get(name)
        
        raise errors.InterpreterError(name, "Undefined variable '" + name.lexeme + "'")
    
    def get_at(self, distance: int, name: str) -> object:
        return self.ancestor(distance).values.get(name)
    
    def ancestor(self, distance: int) -> object:
        env = self
        for _ in range(distance):
            env = env.enclosing
        return env