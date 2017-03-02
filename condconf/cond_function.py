from typing import List

from .cond import BaseCond


DEFAULT_FUNCTION_TEMPLATE = """{decorators}
def {function_name}({function_args}):
    {pre_process_code}
    if {true_condition}:
        return True
    else:
        return False"""


class CondFunction:
    def __init__(self, func_name: str, condition: BaseCond, *,
                 func_args: List = None,
                 decorators: List = None,
                 pre_process_code: str = ''):
        self.func_name = func_name
        self.condition = condition
        self.decorators = decorators or []
        self.func_args = func_args or []
        self.pre_process_code = pre_process_code

        self.template = DEFAULT_FUNCTION_TEMPLATE

    def generate_code(self):
        template_args = {
            'decorators': self.__join_decorators(self.decorators),
            'function_name': self.func_name,
            'function_args': ', '.join(self.func_args),
            'true_condition': self.condition.generate_code(),
            'pre_process_code': self.pre_process_code
        }
        return self.template.format(
            **template_args
        )

    @staticmethod
    def __join_decorators(decorators_lst):
        if decorators_lst:
            return '@' + '\n@'.join(decorators_lst) + '\n'
        else:
            return ''

    def __repr__(self):
        return self.generate_code()
