from typing import List


DEFAULT_FUNCTION_TEMPLATE = """{decorators}def {function_name}({function_args}):
    {pre_process_code}if {true_condition}:
        return True
    else:
        return False"""


class CondFunction:
    def __init__(self, func_name: str, condition, *,
                 func_args: List = None,
                 decorators: str = '',
                 pre_process_code: str = ''):
        self.func_name = func_name
        self.condition = condition
        self.func_args = func_args or []
        self.decorators = decorators
        self.pre_process_code = pre_process_code

        self.template = DEFAULT_FUNCTION_TEMPLATE

    def generate_code(self):
        template_args = {
            'decorators': self.decorators,
            'function_name': self.func_name,
            'function_args': ', '.join(self.func_args),
            'true_condition': self.condition.generate_code(),
            'pre_process_code': self.pre_process_code
        }
        return self.template.format(
            **template_args
        )

    def __repr__(self):
        return self.generate_code()
