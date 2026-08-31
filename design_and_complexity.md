# Design and Complexity

## Traversal

Explain your recursive or iterative traversal, how it preserves JSON order, why
it is lazy, and its time and auxiliary-space complexity.

I used nested for loops to go through the regions, dungeons, rooms, chests, and
items. This helps the program keep the original JSON order. It's lazy because
I used yield to return one item at a time. The time complexity is O(n) and the
space complexity is O(1).

## Binary Search

Explain the cost of materializing and sorting the items, the cost of one binary
search, and why binary search requires the sorted view.

Making the list cost O(n) time and space and sorting it costs O(n log n). The
binary search costs O(log n) time and O(1) space. I had to sort the data first
because binary search works by comparing the middle element and then removing half
of the list, therefore if it isn't sorted it can't know which half to remove.

## Decorators

Explain how the decorators improve modularity and safety. Identify precisely
when logging and predicate validation occur.

Decorators help improve modularity and safety because they separate the logging
and error checking from the main query code. @logged_query only prints the log
after the loop is done. @validate_predicate checks the filter function while the
loop is running and raises a QueryValidationError if something fails.
