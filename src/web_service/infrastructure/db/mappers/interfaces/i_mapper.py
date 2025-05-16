from abc import ABC, abstractmethod
from typing import Generic, TypeVar

D = TypeVar("D")
E = TypeVar("E")


class IMapper(ABC, Generic[D, E]):
    @staticmethod
    @abstractmethod
    def to_domain(entity: E) -> D:
        """
        Converts an entity to a domain model.
        :param entity: The entity to convert.
        :return: The domain model.
        """

    @staticmethod
    @abstractmethod
    def to_entity(domain: D) -> E:
        """
        Converts a domain model to an entity.
        :param domain: The domain model to convert.
        :return: The entity.
        """
