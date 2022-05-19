
########################################################################################
# File       : oofinstance.py
# Author     : Devin Arena
# Description: Wrapper for OofInstance.
# Since      : 5/19/2022
########################################################################################

import token
import errors

class OofInstance:

    def __init__(self, class_) -> None:
        self.class_ = class_
        self.fields = {}
    
    def get(self, name: token.Token) -> object:
        if name.lexeme in self.fields:
            return self.fields[name.lexeme]

        method = self.class_.find_method(name.lexeme)
        if method:
            return method.bind(self)
        
        raise errors.InterpreterError(name, "Undefined property '" + name.lexeme + "'.")
    
    def set(self, name: token.Token, value: object) -> None:
        self.fields[name.lexeme] = value
    
    def __str__(self) -> str:
        return self.class_.name + " instance"
        