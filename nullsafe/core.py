from typing import Any, Generic, TypeVar
from functools import wraps


T = TypeVar("T")


class NullSafe:

    def __getattr__(self, k: str):
        return undefined

    def __getitem__(self, k: str):
        return undefined

    def __bool__(self):
        return False

    def __eq__(self, o: object) -> bool:
        if o is None or o is undefined or isinstance(o, NullSafe):
            return True
        return False

    def __repr__(self) -> str:
        return "undefined"

    def __str__(self) -> str:
        return "undefined"

    def __setattr__(self, name: str, value: Any) -> None:
        raise AttributeError(f"'{self.__class__.__name__}' object can't set attribute")


undefined = NullSafe()


class NullSafeProxy(Generic[T]):
    
    __o: T

    def __init__(self, o: T) -> None:
        self.__o = o

    def __getitem__(self, k: str) -> Any:
        try:
            val = self.__o.__getitem__(k)
            if val is None:
                return undefined
            return val
        except (KeyError, AttributeError):
            return undefined

    def __getattr__(self, name: str) -> Any:
        val = getattr(self.__o, name, undefined)
        return undefined if val is None else val

    def __setattr__(self, name: str, value: Any) -> None:
        if name == "_NullSafeProxy__o":
            return super().__setattr__(name, value)
        raise AttributeError(f"'{self.__class__.__name__}' object can't set attribute")


def nullsafe(o: T) -> T:
    if o == None:
        return undefined
    return NullSafeProxy(o)
