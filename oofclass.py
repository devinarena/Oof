
########################################################################################
# File       : oofclass.py
# Author     : Devin Arena
# Description: Oof Class wrapper.
# Since      : 5/19/2022
########################################################################################

import callable
import oofinstance

class OofClass(callable.Callable):

    def __init__(self, name, superclass, methods, fields):
        self.name = name
        self.superclass= superclass
        self.methods = methods
        self.fields = fields
    
    def call(self, interpreter, arguments: list) -> object:
        instance = oofinstance.OofInstance(self)
        initializer = self.find_method("init")
        if initializer:
            initializer.bind(instance).call(interpreter, arguments)
        if self.superclass:
            for field in self.superclass.fields:
                instance.set(field.name, interpreter.evaluate(field.initializer))
        for field in self.fields:
            instance.set(field.name, interpreter.evaluate(field.initializer))
        return instance
    
    def find_method(self, name):
        if name in self.methods:
            return self.methods[name]
        
        if self.superclass:
            return self.superclass.find_method(name)
        
        return None
    
    def arity(self):
        initializer = self.find_method("init")
        if not initializer:
            return 0
        return initializer.arity()
    
    def __str__(self):
        return self.name