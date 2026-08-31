# Process Log

Include at least three concise entries from different development moments.
Repository history and this log are evidence of process, not proof of authorship.

## Entry 1 — 8/27 - 10:15 pm

- Decision, bug, or uncertainty: I needed to make the Item class a frozen dataclass
- Evidence considered: The tests check for a FrozenInstanceError when you try to reassign qty
- Change made: @dataclass(frozen=True) and the required fields
- Test that verified the change: test_item_fields_equality_and_frozen_assignment

## Entry 2 — 8/28 - 8:01 pm

- Decision, bug, or uncertainty: I needed walk_items() to keep the exact JSON order lazily
- Evidence considered: The assignment required this order and the tests check for it
- Change made: I used nested for loops to go through the data and yielded items one by one
- Test that verified the change: test_walk_preserves_sample_order and test_map_is_lazy

## Entry 3 — 8/29 - 12:48 pm

- Decision, bug, or uncertainty: Predicate validation had to be lazy and raise QueryValidationError
- Evidence considered: The assignment states exceptions must be preserved and checked during iteration
- Change made: I created a check inside @validate_predicate to test the function as it runs
- Test that verified the change: test_non_bool_predicate_raises, test_non_callable_predicate_is_checked_lazily, and test_predicate_exception_is_preserved_as_cause
