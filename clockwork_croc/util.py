import logging
import inspect
from functools import wraps

def get_logger(name, fmt=None, level=None):
    bascially_config_log()

    logger = logging.getLogger(name)

    if fmt is not None:
        logger.setFormat(fmt, style='{')

    if level is not None:
        logger.setLevel(level)

    return logger


def bascially_config_log():
    logging.basicConfig(
        format='🤖🐊 {name} {message}',
        style='{',
        level=logging.DEBUG
    )

def memoize(f):
    not_set = object()
    memo = not_set

    @wraps(f)
    def wrapper(*args, **kwargs):
        nonlocal memo
        if memo is not_set:
            memo = f(*args, **kwargs)
        return memo

    return wrapper

def chain(instance_method):
    '''
    Wraps a method by discarding its return value and returning its first
    argument instead. The function must accept a least one positional argument,
    or an argument error 

    Using this on a class instance method allows chaining
    calls on the same receiver, for example

        class Foo:
            @chain
            def bar(self):
                print('Bar!')
                return 'Unused!'

            @chain
            def baz(self):
                print('Baz!')
                return 'Wasted!'

        Foo().bar().baz()
        > 'Bar!'
        > 'Baz!'
    '''
    method_signature = inspect.signature(instance_method)
    if len(method_signature.parameters) < 1:
        raise TypeError(
            'Chainable methods must accept at least one positional argument.'
        )

    @wraps(instance_method)
    def wrapper(self, *args, **kwargs):
        instance_method(self, *args, **kwargs)
        return self

    return wrapper
