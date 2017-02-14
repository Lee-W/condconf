from .condition import (
    ContainAnyCond, ContainAllCond, MatchAnyCond,
    ComplexAllCond, ComplexAnyCond
)


FUNCTION_TEMPLATE = """
def {function_name}({function_signature}):
    if {true_condition}:
        return True
    else:
        return False
"""


def condition_factory(cond_dict, *,
                      type_key='type', content_key='content', var_name=None):
    cond_type, content = cond_dict[type_key], cond_dict[content_key]

    args = {
        'type_key': type_key,
        'content_key': content_key,
        'var_name': var_name
    }

    cond_cls = None
    if cond_type == 'any':
        cond_cls = ContainAnyCond
    elif cond_type == 'all':
        cond_cls = ContainAllCond
    elif cond_type == 'match':
        cond_cls = MatchAnyCond
    elif cond_type == 'complex-all':
        content = (condition_factory(cond, **args) for cond in content)
        cond_cls = ComplexAllCond
    elif cond_type == 'complex-any':
        content = (condition_factory(cond, **args) for cond in content)
        cond_cls = ComplexAnyCond
    else:
        raise ValueError('{cond_type} is not supported'.format(
            cond_type=cond_type))
    return cond_cls(content, var_name=var_name)


# FIXME: text cannot be var_name, it's temp name in list comprehension
class ConditionMeta(type):
    def __new__(mcs, clsname, supers, classdict,
                cond_funcs, cond_options=None):

        if not cond_options:
            cond_options = {
                'signature': 'self',
                'var_name': 'text'
            }

        func_signature = cond_options.get('signature', None)
        var_name = cond_options.get('var_name', None)

        for cond_func in cond_funcs:
            cond = {'type': 'complex-any'}
            cond['content'] = cond_func['conditions']

            func_name = cond_func['name']

            cond_code = condition_factory(cond, var_name=var_name).generate_code()
            func_code = FUNCTION_TEMPLATE.format(
                function_name=func_name,
                function_signature=func_signature,
                true_condition=cond_code
            )
            exec(func_code)
            classdict[func_name] = eval(func_name)
        return super().__new__(mcs, clsname, supers, classdict)
