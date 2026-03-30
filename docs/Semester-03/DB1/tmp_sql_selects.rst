DISTINCT: Unique values only
---------------------------------
# Useful to see which continents or directions actually exist in your data
SELECT DISTINCT direction FROM circuit;


GROUP BY with COUNT: Statistics per category
--------------------------------------------------
# Groups circuits by continent and tells you how many are in each
SELECT continent_id, COUNT(*) AS total_circuits 
FROM circuit 
GROUP BY continent_id;


ORDER BY: Sorting (ASC = Smallest first, DESC = Largest first)
----------------------------------------------------------------
# Sort circuits by length, longest first (DESC)
SELECT name, length FROM circuit 
ORDER BY length DESC;


LIKE: Pattern matching (Wildcards)
---------------------------------------
# Find all circuits where the name contains "Circuit" anywhere
SELECT * FROM circuit 
WHERE name LIKE '%Circuit%';


BETWEEN: Range filtering
-----------------------------
# Find circuits between 4 and 6 kilometers long
SELECT name, length FROM circuit 
WHERE length BETWEEN 4 AND 6;


LIMIT: Top results
-----------------------
# Get only the 3 shortest circuits (Uses default ASC)
SELECT name, length FROM circuit 
ORDER BY length ASC 
LIMIT 3;


HAVING: Filtering grouped data (Very Important!)
-----------------------------------------------------
# Only show countries that have MORE than 2 circuits
# Note: Use HAVING for aggregate functions like COUNT, not WHERE
SELECT country_id, COUNT(*) 
FROM circuit 
GROUP BY country_id 
HAVING COUNT(*) > 2;


IS NOT NULL: Filtering out empty data
------------------------------------------
# Show circuits that actually have an old name recorded
SELECT name, previous_names FROM circuit 
WHERE previous_names IS NOT NULL;