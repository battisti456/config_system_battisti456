from dataclasses import dataclass
from typing import Any, Callable, Optional


@dataclass(frozen=True)
class Config_Item():
    description:str
    checker:Callable[[Any],bool]

class Float(Config_Item):
    def __init__(
            self,
            *,
            description:Optional[str] = None,
            min_value:Optional[float] = None,
            max_value:Optional[float] = None):
        add_text:str = 'a floating point number'
        if min_value is not None and max_value is not None:
            add_text += f" between {min_value} and {max_value}"
        elif min_value is not None:
            add_text += f" more than {min_value}"
        elif max_value is not None:
            add_text += f" less than {max_value}"
        if description is not None:
            add_text += f"; {description}"
        def checker(value:Any) -> bool:
            if not isinstance(value,float|int):
                return False
            if min_value is not None:
                if value < min_value:
                    return False
            if max_value is not None:
                if value > max_value:
                    return False
            return True
        super().__init__(add_text,checker)

class Integer(Config_Item):
    def __init__(
            self,
            *,
            description:Optional[str] = None,
            min_value:Optional[int] = None,
            max_value:Optional[int] = None
    ):
        add_text:str = 'an integer'
        if min_value is not None and max_value is not None:
            add_text += f" between {min_value} and {max_value}"
        elif min_value is not None:
            add_text += f" more than {min_value}"
        elif max_value is not None:
            add_text += f" less than {max_value}"
        if description is not None:
            add_text += f"; {description}"
        def checker(value:Any) -> bool:
            if int(value) != value:
                return False
            if min_value is not None:
                if value < min_value:
                    return False
            if max_value is not None:
                if value > max_value:
                    return False
            return True
        super().__init__(add_text,checker)

class Ratio(Config_Item):
    def __init__(
            self,
            *,
            description:Optional[str] = None):
        add_text:str = 'a ratio (value between 0 and 1)'
        if description is not None:
            add_text += f"; {description}"
        def checker(value:Any) -> bool:
            if not isinstance(value,float|int):
                return False
            return True
        super().__init__(add_text,checker)