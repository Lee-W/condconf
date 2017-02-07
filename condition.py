from abc import ABCMeta, abstractmethod


class BaseCond:
    @abstractmethod
    def generate_code(self):
        pass


class SimpleCond(BaseCond, metaclass=ABCMeta):
    def __init__(self, keywords, var_name=None):
        self.var_name = var_name or 'var'
        self.keywords = keywords

    @property
    def keywords_str(self):
        return "['{}']".format("', '".join(self.keywords))

    def __str__(self):
        return self.generate_code()


class ContainCond(SimpleCond, metaclass=ABCMeta):
    COND_TYPE = 'contain'
    CODE_TEMPLATE = '{operation}(text in {var_name} for text in {keywords_str})'

    def generate_code(self):
        return self.CODE_TEMPLATE.format(
            operation=self.OPERATION,
            var_name=self.var_name,
            keywords_str=self.keywords_str
        )


class ContainAnyCond(ContainCond):
    COND_TYPE = 'any'
    OPERATION = 'any'


class ContainAllCond(ContainCond):
    COND_TYPE = 'all'
    OPERATION = 'all'


class MatchAnyCond(SimpleCond, metaclass=ABCMeta):
    COND_TYPE = 'match'
    OPERATION = 'in'
    CODE_TEMPLATE = '{var_name} in {keywords_str}'

    def generate_code(self):
        return self.CODE_TEMPLATE.format(var_name=self.var_name,
                                         keywords_str=self.keywords_str)


class ComplexCond(metaclass=ABCMeta):
    JOIN_CODE_TEMPLATE = ' {operation} '

    def __init__(self, condtions, **kwargs):
        self.conditions = condtions

    def generate_code(self):
        cond_codes = ('({})'.format(cond.generate_code())
                      for cond in self.conditions)
        join_code_template = self.JOIN_CODE_TEMPLATE.format(operation=self.OPERATION)
        return join_code_template.join(cond_codes)


class ComplexAllCond(ComplexCond):
    COND_TYPE = 'complex-all'
    OPERATION = 'and'


class ComplexAnyCond(ComplexCond):
    COND_TYPE = 'complex-any'
    OPERATION = 'or'
