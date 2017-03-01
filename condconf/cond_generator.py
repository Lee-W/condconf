import logging


from .cond import (
    ContainAnyCond, ContainAllCond, MatchAnyCond,
    ComplexAllCond, ComplexAnyCond
)

from .cond_function import CondFunction


logger = logging.getLogger(__name__)


def cond_factory(cond_dict, *,
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
        content = [cond_factory(cond, **args) for cond in content]
        cond_cls = ComplexAllCond
    elif cond_type == 'complex-any':
        content = [cond_factory(cond, **args) for cond in content]
        cond_cls = ComplexAnyCond
    else:
        raise ValueError(
            '{cond_type} is not supported'.format(cond_type=cond_type)
        )
    return cond_cls(content, var_name=var_name)


def cond_func_generator(cond_func_configs, *, template_args=None):
    if not template_args:
        template_args = dict()

    var_name = template_args.get('var_name')
    if not var_name:
        var_name = 'var'
    else:
        template_args.pop('var_name')

    for cond_func_config in cond_func_configs:
        func_name = cond_func_config['name']
        cond = cond_factory(cond_func_config['condition'],
                            var_name=var_name)
        cond_func = CondFunction(func_name, cond, **template_args)
        yield cond_func


class CondMeta(type):
    def __new__(mcs, clsname, supers, classdict, *, cond_funcs):
        for cond_func in cond_funcs:
            func_code = cond_func.generate_code()
            logger.debug(func_code)
            exec(func_code)
            classdict[cond_func.func_name] = eval(cond_func.func_name)
        return super().__new__(mcs, clsname, supers, classdict)
