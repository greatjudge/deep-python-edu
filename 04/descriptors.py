"""
использовал паттерн шаблонный метод,
 увидел такой способ в книжке Рамальо.
"""

import abc
from validators import MinLengthValidator, EntirelyNumericValidator


class ValidatedABC(abc.ABC):
    def __set_name__(self, owner, name):
        self.storage_name = '_' + name

    def __set__(self, instance, value):
        setattr(instance,
                self.storage_name,
                self.validated(self.storage_name[1:], value))

    def __get__(self, instance, cls):
        if instance is None:
            return self
        return getattr(instance, self.storage_name)

    @abc.abstractmethod
    def validated(self, name: str, value):
        pass


class Integer(ValidatedABC):
    def validated(self, name, value: int):
        if not isinstance(value, int):
            raise TypeError(f'{name} must be integer not {type(value)}')
        return value


class PositiveInteger(Integer):
    def validated(self, name, value: int):
        value = super().validated(name, value)
        if value < 0:
            raise ValueError(f'{name} must be >= 0, you set {value}')
        return value


class String(ValidatedABC):
    def validated(self, name: str, value: str):
        if not isinstance(value, str):
            raise TypeError(f'{name} must be str not {type(value)}')
        return value


class Password(String):
    def __init__(self, validators=None):
        if validators is None:
            self.validators = [MinLengthValidator(),
                               EntirelyNumericValidator()]
        else:
            self.validators = validators

    def validated(self, name: str, value: str):
        value = super().validated(name, value)
        for validator in self.validators:
            validator.validate(value)
        return value


