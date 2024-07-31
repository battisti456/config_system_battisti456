from dataclasses import dataclass
from typing import Any, Callable, TypedDict, Unpack, NotRequired, TypeVar, Generic, Sequence

from typeguard import check_type, TypeCheckError


@dataclass(frozen=True)
class Config_Item():
    description:str
    checker:Callable[[Any],bool]
    level:int = 0

class ConfigArgs(TypedDict):
    level:int
    description:NotRequired[str]

NumVar = TypeVar('NumVar',bound=int|float)

class OnlyNumArgs(Generic[NumVar],TypedDict, total = False):
    min_value:NumVar
    max_value:NumVar

class NumArgs(Generic[NumVar],ConfigArgs,OnlyNumArgs[NumVar]):
    ...

class _Num(Generic[NumVar],Config_Item):
    NUM_DESCRIPTION:str
    def __init__(self,**kwargs:Unpack[NumArgs[NumVar]]):
        add_text:str = self.NUM_DESCRIPTION
        if 'min_value' in kwargs and 'max_value' in kwargs:
            add_text += f" between {kwargs['min_value']} and {kwargs['max_value']}"
        elif 'min_value' in kwargs:
            add_text += f" more than {kwargs['min_value']}"
        elif 'max_value' in kwargs:
            add_text += f" less than {kwargs['max_value']}"
        if 'description' in kwargs:
            add_text += f"; {kwargs['description']}"
        def checker(value:Any) -> bool:
            if not isinstance(value,float|int):
                return False
            try:
                check_type(value,NumVar)
            except TypeCheckError:
                return False
            if 'min_value' in kwargs:
                if value < kwargs['min_value']:
                    return False
            if 'max_value' in kwargs:
                if value > kwargs['max_value']:
                    return False
            return True
        super().__init__(add_text,checker,kwargs['level'])

class Float(_Num[float|int]):
    NUM_DESCRIPTION = 'a floating point number'
class Integer(_Num[int]):
    NUM_DESCRIPTION = 'an integer'

class Ratio(Config_Item):
    def __init__(self,**kwargs:Unpack[ConfigArgs]):
        add_text:str = 'a ratio (value between 0 and 1)'
        if 'description' in kwargs:
            add_text += f"; {kwargs['description']}"
        def checker(value:Any) -> bool:
            if not isinstance(value,float|int):
                return False
            return True
        super().__init__(add_text,checker,kwargs['level'])

class RangeArgs(Generic[NumVar],ConfigArgs,OnlyNumArgs[NumVar]):
    ...

class _Range(Generic[NumVar],Config_Item):
    NUM_DESCRIPTION:str
    def __init__(self,**kwargs:Unpack[RangeArgs[NumVar]]):
        add_text:str = self.NUM_DESCRIPTION
        if 'min_value' in kwargs and 'max_value' in kwargs:
            add_text += f" between {kwargs['min_value']} and {kwargs['max_value']}"
        elif 'min_value' in kwargs:
            add_text += f" more than {kwargs['min_value']}"
        elif 'max_value' in kwargs:
            add_text += f" less than {kwargs['max_value']}"
        if 'description' in kwargs:
            add_text += f"; {kwargs['description']}"
        def checker(value:Any) -> bool:
            if not isinstance(value,Sequence):
                return False
            if not len(value) == 2:#type:ignore
                return False
            
            try:
                check_type(value[0],NumVar)#type:ignore
                check_type(value[1],NumVar)#type:ignore
            except TypeCheckError:
                return False
            if 'min_value' in kwargs:
                if value[0] < kwargs['min_value']:
                    return False
            if 'max_value' in kwargs:
                if value[1] > kwargs['max_value']:
                    return False
            if value[0] > value[1]:
                return False
            return True
        super().__init__(add_text,checker,kwargs['level'])

class FloatRange(_Range[float|int]):
    NUM_DESCRIPTION = "a range represented by an array of two floats"
class IntRange(_Range[int]):
    NUM_DESCRIPTION = "a range represented by an array of two integers"

class String(Config_Item):
    def __init__(self,**kwargs:Unpack[ConfigArgs]):
        add_text:str = "a string"
        if 'description' in kwargs:
            add_text += f"; {kwargs['description']}"
        def checker(value:Any) -> bool:
            return isinstance(value,str)
        super().__init__(add_text,checker,kwargs['level'])

class Bool(Config_Item):
    def __init__(self,**kwargs:Unpack[ConfigArgs]):
        add_text:str = "a boolean"
        if 'description' in kwargs:
            add_text += f"; {kwargs['description']}"
        def checker(value:Any) -> bool:
            return isinstance(value,bool)
        super().__init__(add_text,checker,kwargs['level'])