from __future__ import annotations

import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from abc_sources import JSONInventorySource
from engine import QueryEngine
from errors import QueryValidationError


SAMPLE = str(Path(__file__).resolve().parent.parent / "data" / "sample_small.json")


class StudentTests(unittest.TestCase):
    def engine(self) -> QueryEngine:
        return QueryEngine(JSONInventorySource(SAMPLE))

    def make_inventory_file(self, data: dict) -> str:
        with tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", suffix=".json", delete=False
        ) as file:
            json.dump(data, file)
            return file.name

    def test_missing_version_defaults_to_one(self):
        path = self.make_inventory_file({"world": "Empty", "regions": []})
        try:
            self.assertEqual(JSONInventorySource(path).version(), 1)
        finally:
            Path(path).unlink()

    def test_non_callable_predicate_is_checked_lazily(self):
        iterator = self.engine().filter_items(None)  # type: ignore[arg-type]
        with self.assertRaises(QueryValidationError):
            next(iterator)

    def test_predicate_exception_is_preserved_as_cause(self):
        def bad_predicate(_item):
            raise ValueError("boom")

        with self.assertRaises(QueryValidationError) as raised:
            list(self.engine().filter_items(bad_predicate))

        self.assertIsInstance(raised.exception.__cause__, ValueError)

    def test_empty_inventory_walk_logs_zero_after_exhaustion(self):
        path = self.make_inventory_file({"world": "Empty", "regions": []})
        try:
            output = io.StringIO()
            with redirect_stdout(output):
                items = list(QueryEngine(JSONInventorySource(path)).walk_items())
            self.assertEqual(items, [])
            self.assertEqual(output.getvalue().strip(), "[LOG] walk_items returned 0 items")
        finally:
            Path(path).unlink()

    def test_sku_search_is_case_sensitive(self):
        self.assertIsNone(self.engine().find_item_by_sku("mp-pot-md"))


if __name__ == "__main__":
    unittest.main()
