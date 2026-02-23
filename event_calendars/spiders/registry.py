import scrapy
from collections import UserList

from typing import TypeVar

T = TypeVar('T', bound=scrapy.Spider)


class SpiderRegistry(UserList[type[T]]):
    """Decorator for registering a list of Spider classes (not instances)."""
    #data: list[type[scrapy.Spider]]
    def __call__(self, cls: type[T]) -> type[T]:
        self.data.append(cls)
        return cls

_spiders: list[type[scrapy.Spider]] = []

def register(cls: type[T]) -> type[T]:
    _spiders.append(cls)
    return cls


def get() -> list[type[scrapy.Spider]]:
    return _spiders.copy()
