
########################################################################################
# File       : function.py
# Author     : Devin Arena
# Description: Stores information regarding functions.
# Since      : 5/7/2022
########################################################################################

import callable
import environment
import errors
import oofinstance

class OofFunction(callable.Callable):
    def __init__(self, declaration, closure, is_initializer) -> None:
        self.declaration = declaration
        self.closure = closure
        self.is_initializer = is_initializer
    
    def call(self, interpreter, args: list) -> object:
        env = environment.Environment(self.closure)

        for i in range(len(self.declaration.params)):
            env.define(self.declaration.params[i].lexeme, args[i])
        
        try:
            interpreter.execute_block(self.declaration.body, env)
        except errors.Return as e:
            if self.is_initializer:
                return self.closure.get_at(0, "this")
            return e.value

        if self.is_initializer:
            return self.closure.get_at(0, "this")
        return None
    
    def bind(self, instance: oofinstance.OofInstance) -> object:
        env = environment.Environment(self.closure)
        env.define("this", instance)
        return OofFunction(self.declaration, env, self.is_initializer)

    def arity(self) -> int:
        return len(self.declaration.params)

    def __str__(self) -> str:
        return f"<fn {self.declaration.name.lexeme}>"