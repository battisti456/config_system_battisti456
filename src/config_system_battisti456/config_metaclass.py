from typing import Annotated, Any, TypeVar, get_args, get_origin, override

from typeguard import TypeCheckError, check_type

from .config_item import Config_Item
from .config_override import Config_Override

T = TypeVar('T', bound='Config_Metaclass')

class Config_Metaclass(type):
    _overrides: tuple['Config_Override',...]
    _name: str
    def __init_subclass__(cls, overrides:tuple['Config_Override', ...] = tuple(), name_set: str| None = None) -> None:
        cls._overrides = overrides
        if name_set is None:
            cls._name = cls.__module__
        else:
            cls._name = name_set
        return super().__init_subclass__()
    @override
    def __getattribute__(cls, name: str) -> Any:
        if name in ('_overrides','_name'):
            return type.__getattribute__(cls,name)
        for config_override in cls._overrides.__reversed__():
            if config_override.defines_property(cls.__name, name):
                return config_override.get_property(cls.__name, name)
        return super().__getattribute__(name)
    def __getitem__(cls:T, override: 'Config_Override') -> T:
        class _(cls,overrides = cls.__overrides + (override,), name_set = T.__name):#type:ignore
            ...
        return _
    def _get_description(cls, name:str) -> str:
        type_hint = cls.__annotations__[name]
        if get_origin(type_hint) is Annotated:
            args = get_args(type_hint)
            if isinstance(args[1],Config_Item):
                return args[1].description
        return str(type_hint)
    def _check_value(cls, name:str, value:Any) -> bool:
        type_hint = cls.__annotations__[name]
        if get_origin(type_hint) is Annotated:
            args = get_args(type_hint)
            if isinstance(args[1],Config_Item):
                return args[1].checker(value)
        try:
            check_type(value,type_hint)
            return True
        except TypeCheckError:
            return False
