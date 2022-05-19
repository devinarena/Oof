# Oof
Oof is an incredibly basic and meme-y interpreted programming language. It started as a fun project to learn about interpreters and compilers. Created through following along with the amazing https://craftinginterpreters.com/.

## Development
Oof is basically done and I do not anticipate working on it anymore. The reasons for this are simply 1) I created it as a joke while following along with Part II of CraftingInterpreters, AST walks are incredibly slow and this language is not worth using for large scale projects and 2) I'm working on a real interpreted langauge based off of Part III of the same CraftingInterpreters.

## Requirements
Python3

## Usage
python oof.py \<file\>
  
## Examples
Oof's standard library is incredibly small. However, it does provide all the functionality of a basic programming language.

### Hello World
```
output "Hello World!"; // outputs hello world
```

### Variables
Oof is dynamically typed.
```
set x = 3;
output x; // outputs 3
```

### Loops
Oof supports both for and while loops.
```
for (set x = 1; x <= 10; x = x + 1) {
    output x; // prints 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 on separate lines
}
```
is equivalent to
```
{
    set x = 1;

    while (x <= 10) {
        output x;
        x = x + 1;
    } // outputs 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 on separate lines
}
```
### Functions
Oof supports all your functional magic such as recursion.
```
fun fib(n) {
    if (n == 0 or n == 1) {
        ret 1;
    }
    ret fib(n - 1) + fib(n - 2);
}

for (set i = 0; i < 10; i = i + 1)
    output fib(i); // outputs 1 1 2 3 5 8 13 21 34 55
```
### Classes
Oof allows you to create classes just like any other programming language.
In oof, init is the constructor.
```
class MyClass {
    fun init() {
        output "I'm a class!";
    }
}

set obj = MyClass(); // outputs I'm a class!
```
Oof is very dynamic with what it allows for properties:
```
class MyClass {
    fun init() {
    }
}

fun test() {
    ret 1;
}

set obj = MyClass();
obj.b = test;
output obj.b(); // outputs 1
```
Oof uses the 'this' keyword to access properties of a class.
```
class MyClass {
    fun init() {
        this.x = 1;
    }

    fun run() {
        output this.x;
    }
}

set obj = MyClass();
obj.run(); // outputs 1
```
Oof allows for inheritance using the extends << keyword.
```
class A {
    set x = 1;
}

class B << A {
    fun print() {
        output this.x;
    }
}

set b = B();
b.print(); // outputs 1
```
By default, oof overrides inherited functions. 'super' can be used to access the parent function.
```
class A {
    fun myFun() {
        output "1";
    }
}

class B << A {
    fun myFun() {
        super.myFun();
        output "2";
    }
}

set b = B();
b.myFun(); // outputs 1 and 2
```
### The Standard Library
Oof has 1 standard library function and its clock(). I did not want to add any for the simple reason this project has served its purpose.
```
output clock(); // outputs Unix time in seconds
```
## License and Contribute
MIT. You are free to do with this code what you wish (though it is quite messy). If for whatever reason you'd like to improve oof, feel free to contribute.
