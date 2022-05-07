
########################################################################################
# File       : function.py
# Author     : Devin Arena
# Description: Stores information regarding functions.
# Since      : 5/7/2022
########################################################################################

import callable
import environment

class Function_(callable.Callable):
    def __init__(self, declaration) -> None:
        self.declaration = declaration
        self.arity = len(self.declaration.params)
    
    def call(self, interpreter, args: list) -> object:
        env = environment.Environment(interpreter.globals)

        for i in range(len(self.declaration.params)):
            env.define(self.declaration.params[i].lexeme, args[i])
        
        interpreter.execute_block(self.declaration.body, env)
        return None

    def __str__(self) -> str:
        return f"<fn {self.declaration.name.lexeme}>"