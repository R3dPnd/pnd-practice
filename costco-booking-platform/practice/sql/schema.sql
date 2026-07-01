-- INTERVIEW PRACTICE — SQL Schema + Seed Data
-- Paste this into https://sqliteonline.com and click Run to set up the tables.
-- Then open exercises.sql and write your queries.

DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS departments;

CREATE TABLE departments (
    id        INTEGER PRIMARY KEY,
    dept_name TEXT NOT NULL,
    location  TEXT
);

CREATE TABLE employees (
    id         INTEGER PRIMARY KEY,
    name       TEXT NOT NULL,
    salary     REAL NOT NULL,
    dept_id    INTEGER REFERENCES departments(id),
    hire_date  TEXT,  -- stored as YYYY-MM-DD
    manager_id INTEGER REFERENCES employees(id)
);

CREATE TABLE projects (
    id           INTEGER PRIMARY KEY,
    project_name TEXT NOT NULL,
    dept_id      INTEGER REFERENCES departments(id),
    budget       REAL
);

-- Departments
INSERT INTO departments VALUES (1, 'Engineering',  'Seattle');
INSERT INTO departments VALUES (2, 'Marketing',    'Austin');
INSERT INTO departments VALUES (3, 'Finance',      'Chicago');
INSERT INTO departments VALUES (4, 'HR',           'Seattle');

-- Employees (some with no dept, some with no manager)
INSERT INTO employees VALUES (1,  'Alice Chen',    95000, 1, '2022-03-15', NULL);
INSERT INTO employees VALUES (2,  'Bob Smith',     72000, 1, '2023-07-01', 1);
INSERT INTO employees VALUES (3,  'Carol White',   68000, 1, '2024-01-10', 1);
INSERT INTO employees VALUES (4,  'David Kim',     88000, 2, '2021-11-20', NULL);
INSERT INTO employees VALUES (5,  'Emma Davis',    55000, 2, '2024-06-05', 4);
INSERT INTO employees VALUES (6,  'Frank Lee',     61000, 2, '2023-09-14', 4);
INSERT INTO employees VALUES (7,  'Grace Park',    77000, 3, '2020-04-22', NULL);
INSERT INTO employees VALUES (8,  'Henry Brown',   65000, 3, '2022-08-30', 7);
INSERT INTO employees VALUES (9,  'Iris Nguyen',   59000, 4, '2025-01-03', NULL);
INSERT INTO employees VALUES (10, 'Jack Wilson',   48000, 4, '2025-03-18', 9);
INSERT INTO employees VALUES (11, 'Karen Moore',   51000, NULL, '2024-11-07', NULL); -- no dept

-- Projects
INSERT INTO projects VALUES (1, 'Platform Rewrite',   1, 500000);
INSERT INTO projects VALUES (2, 'Spring Campaign',    2, 120000);
INSERT INTO projects VALUES (3, 'Budget Automation',  3, 80000);
INSERT INTO projects VALUES (4, 'Recruiting Portal',  4, 45000);
