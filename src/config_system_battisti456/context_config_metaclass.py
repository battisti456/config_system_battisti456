import sys
from typing import Any, TypeVar, override
from contextvars import ContextVar

from .config_override import Config_Override 

from .config_metaclass import Config_Metaclass

T = TypeVar('T',bound='Context_Config_Metaclass')

class Context_Config_Metaclass(Config_Metaclass):
    def __init__(
        cls:T, #type:ignore
        name: str, 
        bases: tuple[type, ...], 
        namespace: dict[str, Any], 
        overrides: tuple[Config_Override, ...] = tuple(), 
        name_set: str | None = None):
        class_name = name
        cls._contextvar:ContextVar[T] = ContextVar(class_name)
        def __getattr__(name:str) -> Any:
            if name == class_name:
                try:
                    return cls._contextvar.get()
                except LookupError:
                    ...
        sys.modules[cls.__module__].__getattr__ = __getattr__
    @override
    def __getitem__(cls: T, override: Config_Override) -> T:
        item = super().__getitem__(override)
        cls._contextvar.set(item)#type:ignore
        return item
    @override
    def __getattribute__(cls, name: str) -> Any:
        if name == '_contextvar':
            return type.__getattribute__(cls,name)
        return super().__getattribute__(name)

