from abc import ABC, abstractmethod
from typing import Generator, Any
from dlt.sources.helpers.rest_client import RESTClient
from dlt.sources.helpers.rest_client.paginators import OffsetPaginator


class BaseExtractor(ABC):
    def __init__(self, base_url: str, limit: int = 1000):
        self.base_url = base_url
        self.limit = limit

    def create_client(self, offset: int, max_offset: int, limit_param: str, offset_param: str) -> RESTClient:
        return RESTClient(
            base_url=self.base_url,
            paginator=OffsetPaginator(
                limit=self.limit,
                offset=offset,
                maximum_offset=max_offset,
                limit_param=limit_param,
                offset_param=offset_param,
                total_path=None
            )
        )

    def load_from_source(self, offset: int, max_offset: int, limit_param: str, offset_param: str) -> Generator[Any, None, None]:
        client = self.create_client(offset, max_offset, limit_param, offset_param)
        yield from client.paginate()

    @abstractmethod
    def extract_to_postgres(self):
        pass

    @abstractmethod
    def extract_to_csv(self):
        pass
