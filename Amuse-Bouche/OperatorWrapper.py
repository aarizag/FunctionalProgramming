from typing import  Dict, Callable, TypeVar, List, Any
from functools import wraps


# Debug Tools

SILENT_TRACE = True

T1 = TypeVar('T1')
def trace(func: Callable[..., T1]) -> Callable[..., T1]:
    """
    Print the function arguments and the type
    Adapted from the @debug decorator of Hjelle, Primer on Python Decorators
    (https://realpython.com/primer-on-python-decorators/#debugging-code)
    """

    @wraps(func)
    def wrapper_trace(*args: List[Any], **kwargs: List[Any]) -> T1:
        if not SILENT_TRACE:
            args_str = [str(a) for a in args]
            funcType = {
                '__lt__': ' < ',
                '__gt__': ' > ',
                '__or__': ' | ',
                '__xor__': ' ^ ',
                '__truediv__': ' / ',
                '__and__': ' & ',
                '__mod__': ' % ',
                '__mul__': ' * ',
            }.get(func.__name__, '')

            fullArgsStr = funcType.join(args_str)

            print(fullArgsStr)
        value = func(*args, **kwargs)
        return value

    return wrapper_trace

# End Debug Tools
class Meta(type):
    @trace
    def __lt__(self, other):
        return self._createStreak('<', other)

    @trace
    def __gt__(self, other):
        return self._createStreak('>', other)

    @trace
    def __or__(self, other):
        return self._createStreak('|', other)

    @trace
    def __xor__(self, other):
        return self._createStreak('^', other)

    @trace
    def __truediv__(self, other):
        return self._createStreak('/', other)

    @trace
    def __and__(self, other):
        return self._createStreak('&', other)

    @trace
    def __mod__(self, other):
        return self._createStreak('%', other)

    @trace
    def __mul__(self, other):
        return self._createStreak('*', other)

    def _createStreak(self, symbol, other):
        if other is X:
            return OperatorStreak([symbol])
        elif isinstance(other, OperatorStreak):
            return OperatorStreak([symbol]) + other
        else:
            return OperatorStreak([symbol], other)


class X(metaclass=Meta): # X is a placeholder name. I chose it since it is short
    pass

class OperatorStreak():
    def __init__(self, streak: List[str] = [], value=None):
        self.streak = streak
        self.value = value # Keeps track of second value of overall operator

    @trace
    def __lt__(self, other):
        return self._performOperator('<', other)

    @trace
    def __gt__(self, other):
        return self._performOperator('>', other)

    @trace
    def __or__(self, other):
        return self._performOperator('|', other)

    @trace
    def __xor__(self, other):
        return self._performOperator('^', other)

    @trace
    def __truediv__(self, other):
        return self._performOperator('/', other)

    @trace
    def __and__(self, other):
        return self._performOperator('&', other)

    @trace
    def __mod__(self, other):
        return self._performOperator('%', other)

    @trace
    def __mul__(self, other):
        return self._performOperator('*', other)

    def _performOperator(self, symbol, other):
        self.streak.append(symbol)
        if isinstance(other, OperatorStreak):
            return self + other
        else:
            return OperatorStreak(self.streak, other)


    def __add__(self, other): # Other must be of type OperatorStreak
        return OperatorStreak(self.streak + other.streak, other.value) # Value should never come from left side

    def reset(self):
        self.streak = []
        self.value = None

    def append(self, val):
        self.streak.append(val)

class MyWrapper():
    # This is a map of all operators to their functions
    # To make this simple, I only selected these 3 operators
    # This Wrapper can be made more complex by adding the rest of the one character operators
    #     or attempting to implement two character operators
    operators = {
        '<': '__lt__',
        '>': '__gt__',
        '|': '__or__',
        '^': '__xor__',
        '/': '__truediv__',
        '&': '__and__',
        '%': '__mod__',
        '*': '__mul__',
    }
    
    def __init__(self, cls):
        self.wrappedClass = cls
        self.types = cls.types if hasattr(cls, 'types') else {} # Set for quick lookup if a valid operator was found
        self.streak = OperatorStreak()

    def __call__(self, value):
        self.wrapped = self.wrappedClass(value)
        return self

    def __getattr__(self, attr):
        if callable(attr):
            return self.attr
        else:
            return self.wrapped.__getattribute__(attr)

    @trace
    def __lt__(self, other):
        return self._performOperator('<', other)

    @trace
    def __gt__(self, other):
        return self._performOperator('>', other)

    @trace
    def __or__(self, other):
        return self._performOperator('|', other)

    @trace
    def __xor__(self, other):
        return self._performOperator('^', other)

    @trace
    def __truediv__(self, other):
        return self._performOperator('/', other)

    @trace
    def __and__(self, other):
        return self._performOperator('&', other)

    @trace
    def __mod__(self, other):
        return self._performOperator('%', other)

    @trace
    def __mul__(self, other):
        return self._performOperator('*', other)

    def _performOperator(self, symbol, other):
        operator = self.operators[symbol]
        # Keeps track of streak of operators
        self.streak.append(symbol)

        # Check if we have matched an operator
        def testOperator():
            myOperator = ''.join(self.streak.streak)
            return myOperator in self.types

        if other is X:
            return self
        # Combines streaks of operators (if weird order of operations)
        elif isinstance(other, OperatorStreak):
            self.streak = self.streak + other
            # Value will be given from other
            if self.streak.value:
                if testOperator():
                    return self._runOperator()
                else:
                    raise Exception ("Invalid Operator")
            return self
        else:
            # Attempt to correctly execute some operator
            # We already attempted to use our operator and failed
            self.streak.value = other
            if testOperator():
                return self._runOperator()
            elif(self.streak.streak):
                    raise Exception ("Invalid Operator")
            else:
                # Performs Operator Normally
                return self.wrapped.__getattribute__(operator)(other) # Int does not have __dict__ atr?

    def _runOperator(self):
        operator = ''.join(self.streak.streak)
        value = self.streak.value
        # Resets Streak
        self.streak.reset()
        return self.types[operator](self.wrapped, value)