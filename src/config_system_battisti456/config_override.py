from typing import Any, Mapping, override


class Config_Override():
    def defines_property(self,path: str, name: str) -> bool:
        raise NotImplementedError()
    def get_property(self, path: str, name: str) -> Any:
        raise NotImplementedError()

type RecursiveMapping = Mapping[str,'Any|RecursiveMapping']

class Recursive_Mapping_Config_Override(Config_Override):
    def __init__(self,mapping:RecursiveMapping):
        self.mapping = mapping
    @override
    def defines_property(self, path: str, name: str) -> bool:
        current_mapping:Any|RecursiveMapping = self.mapping
        for element in path.split('.') + [name]:
            if not isinstance(current_mapping,Mapping):
                return False
            if element in current_mapping.keys():
                current_mapping = current_mapping[element]
            else:
                return False
        return True
    @override
    def get_property(self, path: str, name: str) -> Any:
        current_mapping:Any|RecursiveMapping = self.mapping
        for element in path.split('.') + [name]:
            current_mapping = current_mapping[element]
        return current_mapping