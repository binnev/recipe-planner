import operator
from copy import deepcopy
from typing import Callable, Any

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


class InMemoryQuerySet(list):
    """
    In-memory list of dictionaries with some django queryset-like filtering abilities. Sometimes
    storing and manipulating data in memory is better for performance than using database
    queries. However, we miss the django queryset syntax. The aim of this class is to provide
    familiar django-like syntax for data that is stored in memory.

    This means we can do nice query operations like this:
        data.filter(distance__gte=20, owner="trainline").exclude(mode="bus")

    Which, for a native list, would require a statement like this:
        filter(lambda item: item["distance"] >= 20 and owner == "trainline" and mode != "bus", data)
    """

    def filter(self, **kwargs) -> "InMemoryQuerySet":
        func = lambda item: self._filter_item(item, **kwargs)
        return InMemoryQuerySet(filter(func, self))

    def exclude(self, **kwargs) -> "InMemoryQuerySet":
        func = lambda item: not self._filter_item(item, **kwargs)
        return InMemoryQuerySet(filter(func, self))

    def get(self, **kwargs) -> dict:
        qs = self.filter(**kwargs)
        if len(qs) == 0:
            raise ObjectDoesNotExist
        if len(qs) > 1:
            raise MultipleObjectsReturned
        return self.filter(**kwargs)[0]

    @classmethod
    def _filter_item(cls, item: dict, **kwargs):
        for key, value in kwargs.items():
            key, operation = cls.map_operation(key)
            attribute = item[key] if isinstance(item, dict) else getattr(item, key)
            if not operation(attribute, value):
                return False
        return True

    @staticmethod
    def map_operation(key) -> (str, Callable):
        mapping = dict(
            lt=operator.lt,
            lte=operator.le,
            gt=operator.gt,
            gte=operator.ge,
        )
        if "__" in key:
            key, operation = key.split("__")
            operation = mapping.get(operation)
        else:
            operation = operator.eq
        return key, operation

    def all(self) -> list:
        return list(deepcopy(self))

    def exists(self) -> bool:
        return bool(self)

    def first(self) -> Any:
        return self[0] if self.exists() else None

    def last(self) -> Any:
        return self[-1] if self.exists() else None

    def count(self) -> int:
        return len(self)
