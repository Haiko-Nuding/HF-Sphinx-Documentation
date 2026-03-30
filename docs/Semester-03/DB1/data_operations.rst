Relational Operations & Transactions
====================================

Relational databases store information across multiple tables. To combine them, we use Joins.

Joining Tables
--------------
* **INNER JOIN:** Returns records that have matching values in both tables.
* **LEFT JOIN:** Returns all records from the left table, and matched records from the right.

Data Modification (DML)
-----------------------
.. warning:: 
   Always use a ``WHERE`` clause with ``UPDATE`` and ``DELETE`` to avoid accidental mass-data loss.

* **INSERT:** Adding new records. Be careful with ``AUTO_INCREMENT`` columns.
* **UPDATE:** Modifying existing data.
* **DELETE:** Removing data. Note the **referential integrity**: Delete child records before parent records.

Transactions
------------
To ensure data consistency, multiple steps are grouped into one transaction.

* ``SET AUTOCOMMIT = 0;`` - Disables automatic saving.
* ``COMMIT;`` - Permanently saves changes.
* ``ROLLBACK;`` - Reverts changes if an error occurs.

.. admonition:: Advanced Lab: Transactional Delete
   1. Start Transaction.
   2. Delete dependent records (e.g., ``race_data``).
   3. Delete the main record (e.g., ``race``).
   4. Verify, then ``COMMIT``.