-- INTERVIEW PRACTICE — SQL Exercises
-- Run schema.sql first to create and populate the tables.
-- Write your answer below each question. Check against solutions.sql when done.

-- ============================================================
-- Query 1 — Basic JOIN (with NULLs)
-- List all employee names and their department name.
-- Include employees who have NO department assigned.
-- Expected: 11 rows — Karen Moore should appear with NULL dept_name
-- ============================================================

-- YOUR ANSWER:
SELECT e.name AS employee_name, d.dept_name
FROM employees e
LEFT JOIN departments d ON e.dept_id = d.dept_id;

-- ============================================================
-- Query 2 — Aggregation + HAVING
-- Show the average salary per department name.
-- Only include departments where the average salary is above 60,000.
-- Order results by average salary descending.
-- Expected: Engineering (~78,333), Finance (~71,000), Marketing (~68,000)
-- ============================================================

-- YOUR ANSWER:
SELECT d.dept_name, AVG(e.salary) AS avg_salary
FROM employees e
JOIN departments d ON e.dept_id = d.id
GROUP BY d.dept_name
HAVING AVG(e.salary) > 60000
ORDER BY avg_salary DESC;

-- ============================================================
-- Query 3 — Correlated Subquery
-- Find employees who earn more than the average salary
-- of their own department.
-- Show: employee name, salary, dept_id
-- ============================================================

-- YOUR ANSWER:
SELECT e.name as employee_name, e.salary as salary, e.dept_id as dept_id
FROM employees e
WHERE e.salary > (SELECT AVG(e2.salary)
    FROM employees e2
    WHERE e2.dept_id = e.dept_id);  


-- ============================================================
-- Query 4 — Self JOIN
-- List each employee's name alongside their manager's name.
-- Employees with no manager should still appear (manager name = NULL).
-- ============================================================
-- YOUR ANSWER:
SELECT e.name AS employee_name, m.name AS manager_name
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;


-- ============================================================
-- Query 5 — Date Filter
-- Find all employees hired in the last 2 years from today (2026-06-17).
-- Show: name, hire_date
-- Note: SQLite uses DATE('now', '-2 years') — no DATEADD() here
-- ============================================================

-- YOUR ANSWER:


-- ============================================================
-- Query 6 — Multi-table JOIN
-- List each project name, the department it belongs to,
-- and the number of employees in that department.
-- ============================================================

-- YOUR ANSWER:


-- ============================================================
-- Conceptual questions — answer in comments below each one:

-- Q1: What is the difference between WHERE and HAVING?


-- Q2: When would you use LEFT JOIN instead of INNER JOIN?


-- Q3: What is an index? Give an example of when adding one HURTS performance.


-- Q4: What is the difference between DELETE, TRUNCATE, and DROP?


-- Q5: When is a subquery better than a JOIN?


