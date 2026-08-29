from __future__ import annotations

from collections.abc import Callable, Iterator
from typing import Any, TypeVar

from abc_sources import InventorySource
from decorators import logged_query, validate_predicate
from models import Item

T = TypeVar("T")
U = TypeVar("U")


class QueryEngine:
    """Queries over a hierarchical inventory source."""

    def __init__(self, source: InventorySource):
        self.source = source

    def _walk_node(self, node: Any) -> Iterator[Item]:
        """Yield Items lazily in documented JSON order.

        You may implement this traversal recursively or with an explicit stack.
        Do not first build a complete list of Item objects.
        """
        for region in node.get("regions", []):
            for dungeon in region.get("dungeons", []):
                for room in dungeon.get("rooms", []):
                    for chest in room.get("chests", []):
                        for item_data in chest.get("items", []):
                            yield Item(
                                sku=item_data["sku"],
                                name=item_data["name"],
                                rarity=item_data["rarity"],
                                qty=item_data["qty"],
                                base_price=float(item_data["base_price"]),
                                tags=list(item_data["tags"]),
                            )

    @logged_query
    def walk_items(self) -> Iterator[Item]:
        yield from self._walk_node(self.source.root())

    @validate_predicate
    def filter_items(self, pred: Callable[[Item], bool]) -> Iterator[Item]:
        for item in self.walk_items():
            if pred(item):
                yield item

    def map_items(self, fn: Callable[[Item], T]) -> Iterator[T]:
        for item in self.walk_items():
            yield fn(item)

    def reduce_items(self, reducer: Callable[[U, Item], U], initial: U) -> U:
        result = initial
        for item in self.walk_items():
            result = reducer(result, item)
        return result

    def find_item_by_sku(self, sku: str) -> Item | None:
        """Sort by SKU and use a student-written binary-search loop.

        Linear search, dictionary lookup, and the bisect module do not satisfy
        the assignment requirement.
        """
        items = sorted(self.walk_items(), key=lambda item: item.sku)
        lo = 0
        hi = len(items) - 1

        while lo <= hi:
            mid = (lo + hi) // 2
            mid_sku = items[mid].sku
            if mid_sku == sku:
                return items[mid]
            if mid_sku < sku:
                lo = mid + 1
            else:
                hi = mid - 1

        return None
