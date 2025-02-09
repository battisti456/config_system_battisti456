from typing import Annotated, Any, TypeVar, get_args, get_origin, override

from typeguard import TypeCheckError, check_type

from .config_item import Config_Item
from .config_override import Config_Override

T = TypeVar('T', bound='Config_Metaclass')

def merge_base_overrides(bases:tuple[type, ...]) -> tuple[Config_Override, ...]:
    overrides:tuple[tuple[Config_Override, ...], ...] = tuple(
        base._overrides for base in bases if hasattr(base,'_overrides')#type: ignore
    )
    to_return:list[Config_Override] = []
    for override_group in overrides:
        for config_override in override_group:
            if config_override not in to_return:
                to_return.append(config_override)
    return tuple(to_return)

class Config_Metaclass(type):
    _overrides: tuple['Config_Override',...]
    _name: str
    def __new__(mcs, name:str, bases:tuple[type, ...], namespace:dict[str, Any], overrides:tuple['Config_Override', ...] = tuple(), name_set: str| None = None) -> None:
        namespace['_overrides'] = merge_base_overrides(bases) + overrides
        if name_set is None:
            namespace['_name'] = namespace['__module__']
        else:
            namespace['_name'] = name_set
        return super().__new__(mcs,name,bases,namespace)#type:ignore
    @override
    def __getattribute__(cls, name: str) -> Any:
        if name in ('_overrides','_name'):
            return type.__getattribute__(cls,name)
        for config_override in reversed(cls._overrides):
            if config_override.defines_property(cls._name, name):
                return config_override.get_property(cls._name, name)
        return type.__getattribute__(cls,name)
    def __getitem__(cls:T, override: 'Config_Override') -> T:
        class _(cls,overrides = cls._overrides + (override,), name_set = cls._name):
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
