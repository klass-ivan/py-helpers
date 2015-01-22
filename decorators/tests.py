#
# Currently it's not unit tests. Just simple usage examples and checking
# =====================================================================================

import logging
from decorators.logging_decorators import log_call, log_call_using, log_result, log_result_using

__author__ = 'klass'

logging.basicConfig(level=logging.DEBUG)

@log_call('Main', logging.DEBUG, 'Function x is called with x0={x0} and delta={delta}')
def function_x(x0, x1, delta=1):
    pass


@log_result('Math', logging.INFO, 'Result is {result}')
@log_call('Math', logging.INFO, 'Calculating {x} times 2.')
def twice(x):
    return x*2


function_x(2, 3)
function_x('_x0_', 2.5, delta=8)
function_x('__2', 15, delta=12)


twice(12)


logger = logging.getLogger('LoggerInstance')

@log_result_using(logger.info, 'Square is {result}')
@log_call_using(logger.debug, 'Calculating square of {n}')
def square(n):
    return n**2

square(14)


# ========================================================================================

from class_init_decorator import InitDecorator


class CreateAttr(InitDecorator):

    @log_call('InitDecorator', logging.DEBUG, 'Applying before hook on {target_instance}')
    def decorate(self, target_instance):
        target_instance.some_extra = [1, 2, 3]


class AddData(InitDecorator):

    def __init__(self, value):
        self.value_to_add = value

    @log_call('InitDecorator', logging.DEBUG,
              'Applying after hook on {target_instance} with argument "{self.value_to_add}"')
    def decorate(self, target_instance):
        target_instance.data.append(self.value_to_add)


@AddData.after_init('!')
@AddData.after_init('tail')
@CreateAttr.before_init()
class SimpleClass(object):

    @log_call('InitDecorator',
              logging.DEBUG,
              'Original initialisation of instance to be decorated - {self}')
    def __init__(self):
        self.data = []


b = SimpleClass()
assert b.data == ['tail', '!']
assert hasattr(b, 'some_extra')