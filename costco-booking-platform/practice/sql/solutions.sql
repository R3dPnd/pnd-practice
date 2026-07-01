-- SOLUTIONS — Do not open until you have attempted exercises.sql

-- ============================================================
-- Query 1 — Basic JOIN (LEFT JOIN to include no-dept employees)
-- ============================================================
SELECT e.name, d.dept_name
FROM employees e
LEFT JOIN departments d ON e.dept_id = d.id;

-- WHY LEFT JOIN: INNER JOIN drops rows where dept_id IS NULL.
-- Karen Moore has no department and must still appear.


-- ============================================================
-- Query 2 — Aggregation + HAVING
-- ============================================================
SELECT d.dept_name, AVG(e.salary) AS avg_salary
FROM employees e
INNER JOIN departments d ON e.dept_id = d.id
GROUP BY d.dept_name
HAVING AVG(e.salary) > 60000
ORDER BY avg_salary DESC;

-- KEY POINT: You cannot use WHERE avg_salary > 60000 because avg_salary
-- doesn't exist yet at the WHERE stage. HAVING filters AFTER aggregation.
-- WHERE filters individual ROWS. HAVING filters GROUPS.


-- ============================================================
-- Query 3 — Correlated Subquery
-- ============================================================
SELECT e.name, e.salary, e.dept_id
FROM employees e
WHERE e.salary > (
    SELECT AVG(e2.salary)
    FROM employees e2
    WHERE e2.dept_id = e.dept_id
);

-- This is a CORRELATED subquery: it re-executes once per outer row,
-- using the outer row's dept_id. Readable but slower on large tables.

-- JOIN approach (better performance at scale):
SELECT e.name, e.salary, dept_avgs.avg_salary
FROM employees e
INNER JOIN (
    SELECT dept_id, AVG(salary) AS avg_salary
    FROM employees
    GROUP BY dept_id
) dept_avgs ON e.dept_id = dept_avgs.dept_id
WHERE e.salary > dept_avgs.avg_salary;


-- ============================================================
-- Query 4 — Self JOIN
-- ============================================================
SELECT e.name AS employee, m.name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;

-- WHY LEFT JOIN: Employees with no manager (manager_id IS NULL) would
-- be dropped by an INNER JOIN. Alice, David, Grace, Iris have no manager.


-- ============================================================
-- Query 5 — Date Filter (SQLite syntax)
-- ============================================================
SELECT name, hire_date
FROM employees
WHERE hire_date >= DATE('now', '-2 years');

-- SQL Server equivalent: WHERE hire_date >= DATEADD(YEAR, -2, GETDATE())
-- MySQL equivalent:      WHERE hire_date >= DATE_SUB(NOW(), INTERVAL 2 YEAR)
-- PostgreSQL equivalent: WHERE hire_date >= NOW() - INTERVAL '2 years'
-- Always clarify which DB is in use — syntax varies.


-- ============================================================
-- Query 6 — Multi-table JOIN with COUNT
-- ============================================================
SELECT p.project_name, d.dept_name, COUNT(e.id) AS employee_count
FROM projects p
INNER JOIN departments d ON p.dept_id = d.id
LEFT JOIN employees e ON e.dept_id = d.id
GROUP BY p.project_name, d.dept_name;


-- ============================================================
-- Conceptual Answers
-- ============================================================

-- Q1: WHERE vs HAVING
-- WHERE filters individual rows BEFORE aggregation (GROUP BY).
-- HAVING filters groups AFTER aggregation.
-- Use WHERE to filter source rows; use HAVING to filter aggregate results.
-- Example: WHERE salary > 50000 (row-level) vs HAVING COUNT(*) > 3 (group-level)

-- Q2: LEFT JOIN vs INNER JOIN
-- INNER JOIN: only rows with a match on BOTH sides.
-- LEFT JOIN: all rows from the left table; NULLs where no match on right.
-- Use LEFT JOIN when you want to keep rows even if the related record is missing.
-- Example: show all customers even if they have no orders yet.

-- Q3: Index — when it hurts
-- An index speeds up SELECT lookups by creating a sorted lookup structure.
-- It HURTS performance on columns that are frequently updated (INSERT/UPDATE/DELETE)
-- because the index must be rebuilt on every write.
-- Also hurts on small tables where a full table scan is faster than the index overhead.
-- Also: too many indexes on a table slow down all writes.

-- Q4: DELETE vs TRUNCATE vs DROP
-- DELETE: removes rows one at a time, can use WHERE, logs each row, can be rolled back.
-- TRUNCATE: removes all rows at once, no WHERE clause, minimal logging, faster.
-- DROP: removes the entire TABLE structure including all data and indexes. Irreversible.

-- Q5: Subquery vs JOIN
-- Subquery is cleaner when: checking existence (WHERE EXISTS), or when the derived
-- value is only needed for filtering (not selecting).
-- JOIN is better when: you need columns from the related table in the SELECT, or
-- performance matters on large datasets (query optimizer handles JOINs better).
