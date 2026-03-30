Single-Table Data Retrieval
===========================

In this module, we focus on extracting information from a single table using SQL DML.

Core Concepts
-------------
* **Selection:** Choosing specific columns.
* **Filtering:** Using the ``WHERE`` clause with operators (``<``, ``>``, ``LIKE``, ``IS NULL``).
* **Sorting:** Using ``ORDER BY`` (ASC/DESC).
* **Aggregation:** Using ``COUNT`` and ``GROUP BY``.

Exercises (F1 Database)
-----------------------
.. note:: 
   Use the ``circuits`` table for the following tasks.

1. **Basic Select:** List all circuit names.
2. **Aliasing:** Output names and locations with German headers (using ``AS``).
3. **Pattern Matching:** Find all circuits starting with the letter 'A'.
4. **Logic:** Find all circuits in Italy that do not start with 'A'.