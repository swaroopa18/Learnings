# PostgreSQL Notes

Quick reference covering databases, tables, constraints, inserting, sorting, filtering, and pagination.

---

## 1. Create and Drop Database

> **Note:** `CREATE DATABASE` makes a new empty database. `DROP DATABASE` deletes it **permanently**, including all its data, so use it carefully. You cannot drop a database you are currently connected to.

```sql
CREATE DATABASE test;   -- create a new database
DROP DATABASE test;     -- delete the database entirely
```

SQL comments:
- `-- comment` is a single-line comment.
- `/* comment */` is a multi-line comment.

---

## 2. Create Table

### 2.1 Without constraints

> **Note:** A table is defined by its column names and data types. Without constraints, the database accepts NULLs and duplicates, so data quality is not enforced.

```sql
CREATE TABLE person (
    id INT,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    gender VARCHAR(7),
    date_of_birth DATE      -- no trailing comma after the last column
);
```

**Common data types**

| Type | Meaning |
|------|---------|
| `INT` | Whole number |
| `BIGSERIAL` | Auto-incrementing big integer (1, 2, 3, ...) |
| `VARCHAR(n)` | Text up to `n` characters |
| `DATE` | Calendar date (`YYYY-MM-DD`) |

> The original version had a trailing comma after `date_of_birth DATE,`. That causes a syntax error, so remove it.

### 2.2 With constraints

> **Note:** Constraints are rules on columns.
> - `NOT NULL`: the value cannot be empty.
> - `PRIMARY KEY`: uniquely identifies each row. It is automatically `NOT NULL` and `UNIQUE`.
> - `BIGSERIAL`: PostgreSQL generates the id automatically, so you don't insert it yourself.

```sql
CREATE TABLE person (
    id BIGSERIAL NOT NULL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    gender VARCHAR(7) NOT NULL,
    date_of_birth DATE NOT NULL,
    email VARCHAR(150)          -- optional column (NULL allowed)
);
```

---

## 3. psql Commands

> **Note:** These are **psql meta-commands** (not SQL). They start with a backslash `\` and don't end with a semicolon.

| Command | Description |
|---------|-------------|
| `\l` | List all databases |
| `\c dbname` | Connect to a database |
| `\d` | Show all tables (relations) |
| `\dt` | Show only tables |
| `\d person` | Describe the `person` table (columns, types, constraints) |
| `\i path_to_sql_file` | Run SQL from a file directly |
| `\q` | Quit psql |

Example:
```
\i /home/user/person.sql
```

---

## 4. Insert Into Table

> **Note:** `INSERT INTO` adds a new row. List the columns first, then supply the values **in the same order**. Skip `id` because `BIGSERIAL` fills it. Strings use single quotes `' '`. A date is written as `DATE 'YYYY-MM-DD'`.

```sql
INSERT INTO person (
    first_name,
    last_name,
    gender,
    date_of_birth,
    email
) VALUES (
    'swaroopa',
    'reddy',
    'female',
    DATE '1990-10-20',
    'swaroopa@gmail.com'
);
```

**Tip:** If you omit an optional column (like `email`), it becomes `NULL`. If you omit a `NOT NULL` column, the insert fails.

---

## 5. ORDER BY and DISTINCT

### ORDER BY

> **Note:** `ORDER BY` sorts the result.
> - `ASC`: ascending (A to Z, 1 to 9). This is the **default**.
> - `DESC`: descending (Z to A, 9 to 1).

```sql
SELECT * FROM persons ORDER BY country_of_birth;        -- ascending (default)
SELECT * FROM persons ORDER BY country_of_birth DESC;   -- descending
SELECT * FROM persons ORDER BY id DESC;                 -- newest id first
```

Sorting by multiple columns:
```sql
SELECT * FROM persons ORDER BY country_of_birth ASC, first_name DESC;
```

### DISTINCT

> **Note:** `DISTINCT` removes duplicate values from the result, so you see each value only once.

```sql
SELECT DISTINCT country_of_birth FROM persons ORDER BY country_of_birth;
```

---

## 6. WHERE

> **Note:** `WHERE` filters rows by a condition. Combine conditions with `AND` and `OR`, and use **parentheses** to control precedence. `AND` is evaluated before `OR`, so parentheses matter.

```sql
-- single condition
SELECT * FROM persons WHERE gender = 'Female';

-- AND: both conditions must be true
SELECT * FROM persons
WHERE gender = 'Female' AND country_of_birth = 'Jordan';

-- AND + OR with parentheses
SELECT * FROM persons
WHERE gender = 'Female'
  AND (country_of_birth = 'Jordan' OR country_of_birth = 'China');
```

| Logical operator | Meaning |
|------------------|---------|
| `AND` | All conditions true |
| `OR` | At least one condition true |
| `NOT` | Negates a condition |

---

## 7. Comparison Operators

> **Note:** These operators compare values in `WHERE`. String values need single quotes. Comparing with `NULL` using `=` does not work. Use `IS NULL` or `IS NOT NULL` instead.

| Operator | Meaning |
|----------|---------|
| `=` | Equal to |
| `<>` | Not equal to |
| `!=` | Not equal to |
| `>` | Greater than |
| `<` | Less than |
| `>=` | Greater than or equal to |
| `<=` | Less than or equal to |

```sql
SELECT * FROM employees WHERE department = 'IT';    -- equal to
SELECT * FROM employees WHERE department <> 'IT';   -- not equal to
SELECT * FROM employees WHERE salary >= 50000;      -- greater than or equal
SELECT * FROM employees WHERE email IS NULL;        -- check for NULL
```

---

## 8. LIMIT, OFFSET and FETCH

> **Note:** These control **how many rows** you get back and **where to start**. They are mainly used for top-N queries and pagination. Always pair them with `ORDER BY`. Without it, row order is not guaranteed, so the rows you get can be inconsistent.

### 8.1 LIMIT

> `LIMIT n` returns at most `n` rows.

```sql
-- first 3 employees
SELECT * FROM employees LIMIT 3;
```

### 8.2 OFFSET

> `OFFSET n` skips the first `n` rows.

```sql
-- skip the first 3 employees
SELECT * FROM employees OFFSET 3;
```

### 8.3 LIMIT + OFFSET (Pagination)

> **Note:** Together they give pagination. Formula: `OFFSET = (page_number - 1) * page_size`.

Example: 100 employees, 10 per page.

```sql
-- Page 1
SELECT * FROM employees ORDER BY emp_id LIMIT 10 OFFSET 0;

-- Page 2
SELECT * FROM employees ORDER BY emp_id LIMIT 10 OFFSET 10;

-- Page 3
SELECT * FROM employees ORDER BY emp_id LIMIT 10 OFFSET 20;
```

### 8.4 FETCH

> **Note:** `FETCH FIRST ... ROWS ONLY` does the same job as `LIMIT` but is the **SQL-standard** syntax, so it is more portable across databases. `ROW` and `ROWS` are interchangeable, and so are `FIRST` and `NEXT`.

```sql
-- top 3 highest-paid employees
SELECT * FROM employees
ORDER BY salary DESC
FETCH FIRST 3 ROWS ONLY;
```

With `OFFSET` (skip 2, then take the next 3):

```sql
SELECT * FROM employees
ORDER BY salary DESC
OFFSET 2 ROWS
FETCH NEXT 3 ROWS ONLY;
```

### LIMIT vs FETCH

| Feature | `LIMIT` | `FETCH FIRST` |
|---------|---------|---------------|
| Standard SQL | No (PostgreSQL/MySQL specific) | Yes |
| Works with `OFFSET` | Yes | Yes |
| Syntax | `LIMIT 3` | `FETCH FIRST 3 ROWS ONLY` |

---

## 9. Clause Order Cheat Sheet

> **Note:** SQL clauses must be written in this order, or you will get a syntax error.

```sql
SELECT DISTINCT column_list
FROM table_name
WHERE condition
ORDER BY column [ASC | DESC]
LIMIT n OFFSET m;          -- or: OFFSET m ROWS FETCH NEXT n ROWS ONLY
```

---

## 10. IN and NOT IN

> **Note:** `IN` checks whether a value matches **any** value in a given list. It is a shorter, cleaner replacement for multiple `OR` conditions. `NOT IN` does the opposite and returns rows whose value is **not** in the list.

### Without IN (long way)

```sql
SELECT * FROM employees
WHERE department = 'IT' OR department = 'HR' OR department = 'Finance';
```

### With IN (short way)

```sql
SELECT * FROM employees
WHERE department IN ('IT', 'HR', 'Finance');
```

### NOT IN

```sql
SELECT * FROM employees
WHERE department NOT IN ('IT', 'HR');
```

### With numbers

```sql
SELECT * FROM employees WHERE emp_id IN (1, 3, 5);
```

### With a subquery

```sql
SELECT * FROM employees
WHERE department IN (SELECT department FROM employees WHERE salary > 80000);
```

> **Watch out:** If the list (or subquery) contains a `NULL`, `NOT IN` returns **no rows** at all, because comparing with `NULL` is unknown. Use `NOT EXISTS` or filter out NULLs in that case.

---

## 11. BETWEEN and NOT BETWEEN

> **Note:** `BETWEEN` checks whether a value lies within a range, and the range is **inclusive**, so both the start and end values are included. `BETWEEN a AND b` is the same as `>= a AND <= b`. Always put the **smaller value first**, otherwise you get no rows.

### Numbers

```sql
SELECT * FROM employees
WHERE salary BETWEEN 30000 AND 60000;

-- equivalent to
SELECT * FROM employees
WHERE salary >= 30000 AND salary <= 60000;
```

### Dates

```sql
SELECT * FROM persons
WHERE date_of_birth BETWEEN DATE '1990-01-01' AND DATE '1995-12-31';
```

### NOT BETWEEN

```sql
SELECT * FROM employees
WHERE salary NOT BETWEEN 30000 AND 60000;
```

> **Watch out:** For timestamps, `BETWEEN '2026-01-01' AND '2026-01-31'` ends at midnight on Jan 31 and misses the rest of that day. For timestamp columns, use `>= start AND < next_day` instead.

---

## 12. LIKE and ILIKE

> **Note:** `LIKE` searches for a **pattern** in text, using wildcards.
> - `%` matches **any number** of characters (including zero).
> - `_` matches **exactly one** character.
>
> `LIKE` is **case-sensitive**. `ILIKE` is the **case-insensitive** version and is PostgreSQL specific. `NOT LIKE` and `NOT ILIKE` negate the match.

| Pattern | Meaning |
|---------|---------|
| `'A%'` | Starts with A |
| `'%a'` | Ends with a |
| `'%an%'` | Contains "an" anywhere |
| `'_a%'` | Second letter is a |
| `'A___'` | Starts with A and is exactly 4 characters long |

### Examples

```sql
-- names starting with 'S'
SELECT * FROM persons WHERE first_name LIKE 'S%';

-- emails ending with gmail.com
SELECT * FROM persons WHERE email LIKE '%@gmail.com';

-- names containing 'an'
SELECT * FROM persons WHERE first_name LIKE '%an%';

-- second letter is 'a'
SELECT * FROM persons WHERE first_name LIKE '_a%';
```

### ILIKE (case-insensitive)

```sql
-- matches 'swaroopa', 'Swaroopa', 'SWAROOPA'
SELECT * FROM persons WHERE first_name ILIKE 'swa%';
```

### NOT LIKE

```sql
SELECT * FROM persons WHERE email NOT LIKE '%@gmail.com';
```

### LIKE vs ILIKE

| Feature | `LIKE` | `ILIKE` |
|---------|--------|---------|
| Case-sensitive | Yes | No |
| Standard SQL | Yes | No (PostgreSQL only) |
| Typical use | Exact-case matching | User search boxes |

> To match a literal `%` or `_`, escape it: `LIKE '50\%'`.

---

## 13. GROUP BY

> **Note:** `GROUP BY` groups rows that share the same value in one or more columns, so you can apply **aggregate functions** to each group. Without it, an aggregate runs over the whole table and returns one row.

**Common aggregate functions**

| Function | Purpose |
|----------|---------|
| `COUNT()` | Number of rows |
| `SUM()` | Total of values |
| `AVG()` | Average |
| `MIN()` | Smallest value |
| `MAX()` | Largest value |

### Count rows per group

```sql
-- how many employees in each department?
SELECT department, COUNT(*) AS total_employees
FROM employees
GROUP BY department;
```

### Other aggregates

```sql
-- average salary per department
SELECT department, AVG(salary) AS avg_salary
FROM employees
GROUP BY department;

-- highest and lowest salary per department
SELECT department, MAX(salary) AS highest, MIN(salary) AS lowest
FROM employees
GROUP BY department;
```

### Group by multiple columns

```sql
SELECT department, city, COUNT(*) AS total
FROM employees
GROUP BY department, city;
```

### With WHERE and ORDER BY

```sql
SELECT country_of_birth, COUNT(*) AS total
FROM persons
WHERE gender = 'Female'
GROUP BY country_of_birth
ORDER BY total DESC;
```

> **Rule:** Every column in `SELECT` that is **not** inside an aggregate function must appear in `GROUP BY`. Otherwise PostgreSQL gives an error.

---

## 14. GROUP BY with HAVING

> **Note:** `HAVING` filters **groups** after `GROUP BY` has been applied. `WHERE` filters **individual rows before** grouping, and `HAVING` filters **groups after** grouping. Aggregate functions (like `COUNT()` or `AVG()`) **cannot** be used in `WHERE`, so use `HAVING` for them.

### Example

```sql
-- departments with more than 5 employees
SELECT department, COUNT(*) AS total_employees
FROM employees
GROUP BY department
HAVING COUNT(*) > 5;
```

```sql
-- countries with 10 or more persons
SELECT country_of_birth, COUNT(*) AS total
FROM persons
GROUP BY country_of_birth
HAVING COUNT(*) >= 10
ORDER BY total DESC;
```

### WHERE + GROUP BY + HAVING together

```sql
-- among IT and HR employees, show departments with average salary above 50000
SELECT department, AVG(salary) AS avg_salary
FROM employees
WHERE department IN ('IT', 'HR')      -- filters rows first
GROUP BY department
HAVING AVG(salary) > 50000;           -- filters groups after
```

### WHERE vs HAVING

| Feature | `WHERE` | `HAVING` |
|---------|---------|----------|
| Filters | Individual rows | Groups |
| Runs | Before `GROUP BY` | After `GROUP BY` |
| Can use aggregates | No | Yes |

---

## 15. Execution Order (Why Things Work This Way)

> **Note:** SQL is **written** in one order but **executed** in another. This explains why `WHERE` can't use aggregates and `HAVING` can.

**Written order**

```sql
SELECT ...
FROM ...
WHERE ...
GROUP BY ...
HAVING ...
ORDER BY ...
LIMIT ...;
```

**Execution order**

1. `FROM`: pick the table
2. `WHERE`: filter rows
3. `GROUP BY`: form groups
4. `HAVING`: filter groups
5. `SELECT`: choose columns and compute aggregates
6. `ORDER BY`: sort
7. `LIMIT` / `OFFSET` / `FETCH`: cut the result

---

## 16. MAX, MIN, AVG, SUM, ROUND

> **Note:** Aggregate functions take many rows and return **one value**. They are used on the whole table, or per group when combined with `GROUP BY`. All of them **ignore `NULL` values** (except `COUNT(*)`, which counts rows).

| Function | Purpose |
|----------|---------|
| `MAX(col)` | Largest value |
| `MIN(col)` | Smallest value |
| `AVG(col)` | Average value |
| `SUM(col)` | Total of all values |
| `COUNT(col)` | Number of non-NULL values |
| `COUNT(*)` | Number of rows |
| `ROUND(x, n)` | Rounds `x` to `n` decimal places |

### 16.1 MAX

> Returns the highest value in a column. Works on numbers, text (alphabetical) and dates (latest).

```sql
SELECT MAX(salary) FROM employees;
```

### 16.2 MIN

> Returns the lowest value in a column. Works on numbers, text and dates (earliest).

```sql
SELECT MIN(salary) FROM employees;
```

### 16.3 AVG

> Returns the average (sum divided by the count of non-NULL values).

```sql
SELECT AVG(salary) FROM employees;
```

### 16.4 SUM

> Returns the total of a numeric column.

```sql
SELECT SUM(salary) FROM employees;
```

### 16.5 Using several together

```sql
SELECT
    MIN(salary) AS lowest,
    MAX(salary) AS highest,
    AVG(salary) AS average,
    SUM(salary) AS total
FROM employees;
```

> **Tip:** Use `AS` to give the result column a readable name (an alias).

### 16.6 With GROUP BY

```sql
-- highest salary in each department
SELECT department, MAX(salary) AS highest
FROM employees
GROUP BY department;

-- total salary spent per department, biggest first
SELECT department, SUM(salary) AS total_salary
FROM employees
GROUP BY department
ORDER BY total_salary DESC;
```

### 16.7 ROUND

> `ROUND(value, decimals)` rounds a number to the given number of decimal places. With no second argument, it rounds to the nearest whole number. A negative `decimals` rounds to the left of the decimal point (tens, hundreds, and so on).

```sql
SELECT ROUND(10.567);        -- 11
SELECT ROUND(10.567, 1);     -- 10.6
SELECT ROUND(10.567, 2);     -- 10.57
SELECT ROUND(1234.56, -2);   -- 1200
```

`AVG()` usually returns a long decimal, so wrap it in `ROUND`:

```sql
SELECT department, ROUND(AVG(salary), 2) AS avg_salary
FROM employees
GROUP BY department;
```

> **Watch out:** In PostgreSQL, `ROUND(value, n)` with a second argument works on `NUMERIC` values, not `DOUBLE PRECISION`. `AVG()` on an integer column returns `NUMERIC`, so it works directly. If you hit an error, cast first: `ROUND(value::NUMERIC, 2)`.

### 16.8 Finding the row with the max/min value

> **Note:** `MAX()` only returns the value, not the whole row. To get the full row, use `ORDER BY` with `LIMIT`.

```sql
-- employee with the highest salary
SELECT * FROM employees
ORDER BY salary DESC
LIMIT 1;
```

### 16.9 NULL handling

> **Note:** `SUM`, `AVG`, `MAX` and `MIN` skip NULLs, so `AVG` divides only by the non-NULL count. Use `COALESCE(col, 0)` to treat NULL as 0.

```sql
SELECT AVG(COALESCE(salary, 0)) FROM employees;
```

---

## 17. Basics of Arithmetic

> **Note:** PostgreSQL can do math directly in `SELECT`, with or without a table, and you can use arithmetic on columns to create calculated values on the fly. These don't change the stored data.

### 17.1 Arithmetic operators

| Operator | Meaning | Example | Result |
|----------|---------|---------|--------|
| `+` | Addition | `SELECT 10 + 2;` | 12 |
| `-` | Subtraction | `SELECT 10 - 2;` | 8 |
| `*` | Multiplication | `SELECT 10 * 2;` | 20 |
| `/` | Division | `SELECT 10 / 2;` | 5 |
| `%` | Modulo (remainder) | `SELECT 10 % 3;` | 1 |
| `^` | Exponent (power) | `SELECT 2 ^ 3;` | 8 |
| `!` | Factorial (removed in newer versions) | use `factorial(5)` | 120 |

```sql
SELECT 10 + 2;
SELECT 10 ^ 2;     -- 100
SELECT 10 % 3;     -- 1
```

### 17.2 Integer division

> **Watch out:** Dividing two **integers** gives an **integer** (decimals are dropped). To get a decimal result, make at least one value a decimal or cast it.

```sql
SELECT 7 / 2;           -- 3     (integer division)
SELECT 7.0 / 2;         -- 3.5
SELECT 7::NUMERIC / 2;  -- 3.5   (using a cast)
SELECT 7 / 2.0;         -- 3.5
```

### 17.3 Arithmetic on columns

```sql
-- annual salary from monthly salary
SELECT name, salary, salary * 12 AS annual_salary
FROM employees;

-- add a 10% bonus
SELECT name, salary, salary * 0.10 AS bonus
FROM employees;
```

### 17.4 Real example: discounts

```sql
-- 10% discount on car price
SELECT id, make, model, price,
       ROUND(price * 0.10, 2) AS discount,
       ROUND(price - (price * 0.10), 2) AS final_price
FROM car;
```

> **Tip:** Use parentheses to control the order of operations. Normal math rules apply: parentheses first, then `^`, then `*` `/` `%`, then `+` `-`.

```sql
SELECT 2 + 3 * 4;      -- 14
SELECT (2 + 3) * 4;    -- 20
```

### 17.5 Useful math functions

| Function | Purpose | Example | Result |
|----------|---------|---------|--------|
| `ABS(x)` | Absolute value | `ABS(-5)` | 5 |
| `CEIL(x)` | Round **up** to the next whole number | `CEIL(4.1)` | 5 |
| `FLOOR(x)` | Round **down** to the whole number | `FLOOR(4.9)` | 4 |
| `ROUND(x)` | Round to the nearest whole number | `ROUND(4.5)` | 5 |
| `POWER(a, b)` | a raised to the power b | `POWER(2, 3)` | 8 |
| `SQRT(x)` | Square root | `SQRT(16)` | 4 |
| `MOD(a, b)` | Remainder | `MOD(10, 3)` | 1 |

```sql
SELECT ABS(-5), CEIL(4.1), FLOOR(4.9), ROUND(4.5);
```

### 17.6 Arithmetic with NULL

> **Note:** Any arithmetic with `NULL` gives `NULL`. Use `COALESCE` to supply a default.

```sql
SELECT 10 + NULL;                 -- NULL
SELECT 10 + COALESCE(NULL, 0);    -- 10
```

### 17.7 Division by zero

> **Note:** Dividing by zero raises an error. Use `NULLIF(b, 0)` to turn a zero divisor into `NULL`, which makes the result `NULL` instead of an error.

```sql
SELECT 10 / 0;                 -- ERROR: division by zero
SELECT 10 / NULLIF(0, 0);      -- NULL
```

---

## 18. Alias, COALESCE, NULLIF

### 18.1 Alias (AS)

> **Note:** An alias gives a **temporary name** to a column or a table. It exists only for that query and does not change the real name in the database. It makes output readable, especially for calculated columns, and shortens long table names.

#### Column alias

```sql
SELECT first_name AS name, salary * 12 AS annual_salary
FROM employees;
```

The `AS` keyword is optional, but it is clearer to keep it:

```sql
SELECT first_name name FROM employees;   -- works, but less readable
```

#### Alias with spaces or capital letters

> Use **double quotes** `" "`. Without quotes, PostgreSQL converts names to lowercase.

```sql
SELECT salary * 12 AS "Annual Salary" FROM employees;
```

#### Table alias

```sql
SELECT e.name, e.salary
FROM employees AS e
WHERE e.salary > 50000;
```

Table aliases are essential in joins, where the same table may appear twice.

#### Where can you use an alias?

| Clause | Alias usable? |
|--------|---------------|
| `ORDER BY` | Yes |
| `GROUP BY` | Yes (PostgreSQL allows it) |
| `WHERE` | **No** (it runs before `SELECT`) |
| `HAVING` | **No** (repeat the expression instead) |

```sql
-- works
SELECT salary * 12 AS annual FROM employees ORDER BY annual DESC;

-- fails: alias not available in WHERE
SELECT salary * 12 AS annual FROM employees WHERE annual > 600000;

-- fix: repeat the expression
SELECT salary * 12 AS annual FROM employees WHERE salary * 12 > 600000;
```

---

### 18.2 COALESCE

> **Note:** `COALESCE` returns the **first non-NULL value** from a list of arguments. It is mainly used to replace `NULL` with a default value, because NULL breaks arithmetic and looks bad in reports.

**Syntax**

```sql
COALESCE(value1, value2, value3, ...)
```

#### Basic examples

```sql
SELECT COALESCE(NULL, 'default');          -- default
SELECT COALESCE(NULL, NULL, 5, 10);        -- 5
SELECT COALESCE(1, 2);                     -- 1
```

#### Replace NULL in a column

```sql
-- show 'Email not provided' if email is NULL
SELECT first_name, COALESCE(email, 'Email not provided') AS email
FROM persons;
```

#### Fix arithmetic with NULL

> `salary + NULL` gives `NULL`. Wrap the nullable column with `COALESCE`.

```sql
SELECT name, salary + COALESCE(bonus, 0) AS total_pay
FROM employees;
```

#### Fallback chain

```sql
-- use mobile, else home phone, else 'N/A'
SELECT COALESCE(mobile, home_phone, 'N/A') AS contact
FROM contacts;
```

> **Tip:** All arguments should be of compatible data types. Mixing a number and text can cause errors.

---

### 18.3 NULLIF

> **Note:** `NULLIF(a, b)` returns `NULL` if `a` equals `b`, otherwise it returns `a`. It is the opposite idea of `COALESCE`: it **creates** NULLs on purpose.

**Syntax**

```sql
NULLIF(value1, value2)
```

```sql
SELECT NULLIF(10, 10);   -- NULL (they are equal)
SELECT NULLIF(10, 5);    -- 10   (not equal, returns the first)
```

#### Use 1: Avoid division by zero

```sql
SELECT 10 / 0;                  -- ERROR: division by zero
SELECT 10 / NULLIF(0, 0);       -- NULL, no error
```

```sql
-- safe average per item
SELECT total_amount / NULLIF(quantity, 0) AS price_per_item
FROM orders;
```

#### Use 2: Turn empty strings into NULL

```sql
SELECT NULLIF(email, '') FROM persons;
```

#### Combine COALESCE + NULLIF

> Division by zero gives NULL (via `NULLIF`), then `COALESCE` replaces that NULL with 0.

```sql
SELECT COALESCE(10 / NULLIF(0, 0), 0);   -- 0
```

#### COALESCE vs NULLIF

| Feature | `COALESCE` | `NULLIF` |
|---------|------------|----------|
| Purpose | Replace NULL with a value | Turn a value into NULL |
| Arguments | Any number | Exactly 2 |
| Returns | First non-NULL value | NULL if both are equal, else the first |

---

## 19. Timestamp and Dates

### 19.1 Date and time data types

> **Note:** PostgreSQL has separate types for dates, times and both together. Choose the smallest type that stores what you need.

| Type | Stores | Example value |
|------|--------|---------------|
| `DATE` | Date only | `2026-11-10` |
| `TIME` | Time only | `12:05:30` |
| `TIMESTAMP` | Date + time (no time zone) | `2026-11-10 12:05:30` |
| `TIMESTAMPTZ` | Date + time **with** time zone | `2026-11-10 12:05:30+05:30` |
| `INTERVAL` | A span of time | `3 days`, `2 hours` |

> **Tip:** Prefer `TIMESTAMPTZ` for events (created at, logged at) so values stay correct across time zones.

#### Date format

PostgreSQL's standard format is `YYYY-MM-DD` (ISO format).

```sql
SELECT DATE '2026-11-10';
```

---

### 19.2 Current date and time

> **Note:** These functions return the current date and time from the database server.

| Function | Returns |
|----------|---------|
| `NOW()` | Current date and time (with time zone) |
| `CURRENT_DATE` | Today's date |
| `CURRENT_TIME` | Current time (with time zone) |
| `CURRENT_TIMESTAMP` | Same as `NOW()` |

```sql
SELECT NOW();
SELECT CURRENT_DATE;
SELECT CURRENT_TIME;
```

#### Extract only the date or time with a cast

> `::` is PostgreSQL's cast operator. It converts one type to another.

```sql
SELECT NOW()::DATE;   -- date only
SELECT NOW()::TIME;   -- time only
```

---

### 19.3 Table with date columns

```sql
CREATE TABLE orders (
    id BIGSERIAL PRIMARY KEY,
    item VARCHAR(50) NOT NULL,
    order_date DATE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

INSERT INTO orders (item, order_date)
VALUES ('Laptop', DATE '2026-11-01');
```

> **Note:** `DEFAULT NOW()` fills the column automatically with the current time if you don't provide a value.

---

### 19.4 Adding and subtracting dates (INTERVAL)

> **Note:** An `INTERVAL` is a span of time. Add or subtract it from a date or timestamp.

```sql
SELECT NOW() + INTERVAL '1 day';
SELECT NOW() - INTERVAL '1 year';
SELECT NOW() - INTERVAL '3 months';
SELECT NOW() + INTERVAL '2 hours 30 minutes';

-- date only result
SELECT (NOW() - INTERVAL '10 days')::DATE;
```

Common interval units: `year`, `month`, `week`, `day`, `hour`, `minute`, `second`.

#### Orders from the last 7 days

```sql
SELECT * FROM orders
WHERE order_date >= CURRENT_DATE - INTERVAL '7 days';
```

#### Subtracting two dates

```sql
-- two DATE values: result is the number of days
SELECT DATE '2026-11-10' - DATE '2026-01-01';   -- 313

-- two TIMESTAMP values: result is an INTERVAL
SELECT NOW() - TIMESTAMP '2026-01-01 00:00:00';
```

---

### 19.5 AGE

> **Note:** `AGE()` returns the difference between two dates as years, months and days. With one argument, it compares against today.

```sql
SELECT AGE(NOW(), DATE '1990-10-20');
-- example output: 36 years 21 days

SELECT first_name, date_of_birth, AGE(NOW(), date_of_birth) AS age
FROM persons;
```

---

### 19.6 EXTRACT (get part of a date)

> **Note:** `EXTRACT(field FROM date)` pulls out one part of a date or timestamp, such as the year or month. `DATE_PART('year', date)` does the same thing.

```sql
SELECT EXTRACT(YEAR FROM NOW());
SELECT EXTRACT(MONTH FROM NOW());
SELECT EXTRACT(DAY FROM NOW());
SELECT EXTRACT(DOW FROM NOW());      -- day of week: 0 = Sunday ... 6 = Saturday
SELECT EXTRACT(HOUR FROM NOW());
```

| Field | Meaning |
|-------|---------|
| `YEAR`, `MONTH`, `DAY` | Date parts |
| `HOUR`, `MINUTE`, `SECOND` | Time parts |
| `DOW` | Day of week (0 = Sunday) |
| `DOY` | Day of year |
| `QUARTER` | Quarter of the year (1 to 4) |

```sql
-- people born in October
SELECT * FROM persons
WHERE EXTRACT(MONTH FROM date_of_birth) = 10;

-- count of persons born per year
SELECT EXTRACT(YEAR FROM date_of_birth) AS birth_year, COUNT(*)
FROM persons
GROUP BY birth_year
ORDER BY birth_year;
```

---

### 19.7 DATE_TRUNC

> **Note:** `DATE_TRUNC('unit', timestamp)` cuts a timestamp down to the start of the given unit. It is very useful for grouping by month, week or day.

```sql
SELECT DATE_TRUNC('month', NOW());   -- first moment of this month
SELECT DATE_TRUNC('year', NOW());    -- first moment of this year
SELECT DATE_TRUNC('day', NOW());     -- today at 00:00:00
```

```sql
-- orders per month
SELECT DATE_TRUNC('month', order_date) AS month, COUNT(*) AS total_orders
FROM orders
GROUP BY month
ORDER BY month;
```

---

### 19.8 TO_CHAR (format dates as text)

> **Note:** `TO_CHAR(date, 'format')` converts a date or timestamp into a formatted string for display.

| Format code | Meaning |
|-------------|---------|
| `YYYY` | 4-digit year |
| `MM` | Month number (01 to 12) |
| `Month` | Full month name |
| `Mon` | Short month name |
| `DD` | Day of month |
| `Day` | Full weekday name |
| `HH24` | Hour (24-hour clock) |
| `MI` | Minutes |
| `SS` | Seconds |

```sql
SELECT TO_CHAR(NOW(), 'DD-MM-YYYY');          -- 10-11-2026
SELECT TO_CHAR(NOW(), 'Month DD, YYYY');      -- November  10, 2026
SELECT TO_CHAR(NOW(), 'YYYY-MM-DD HH24:MI');  -- 2026-11-10 12:05
```

> **Watch out:** `Month` and `Day` are padded with spaces to a fixed width. Use `FMMonth` or `FMDay` to remove the padding.

---

### 19.9 Comparing dates

```sql
SELECT * FROM persons WHERE date_of_birth > DATE '1995-01-01';

SELECT * FROM persons
WHERE date_of_birth BETWEEN DATE '1990-01-01' AND DATE '1995-12-31';

SELECT * FROM orders ORDER BY order_date DESC;   -- newest first
```

> **Watch out:** For timestamp columns, `WHERE created_at = '2026-11-10'` only matches exactly midnight. To match a whole day, use a range or cast:
>
> ```sql
> WHERE created_at >= DATE '2026-11-10' AND created_at < DATE '2026-11-11'
> -- or
> WHERE created_at::DATE = DATE '2026-11-10'
> ```
> The range version is faster because it can use an index.

---

# PostgreSQL Notes - Part 5

Continues from Part 4. Covers primary keys, `ALTER TABLE`, unique and check constraints, deleting rows and adding rows.

> **Numbering note:** Part 4 ended with a "Quick Summary" numbered 20. Here the topics follow your headings (20 to 25), so renumber if you merge the files.

Sample table used in the examples:

```sql
CREATE TABLE person (
    id BIGSERIAL NOT NULL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    gender VARCHAR(7) NOT NULL,
    date_of_birth DATE NOT NULL,
    email VARCHAR(150)
);
```

---

## 20. Primary Keys, Dropping and Adding

> **Note:** A **primary key** uniquely identifies each row in a table. It is automatically `NOT NULL` and `UNIQUE`, and a table can have **only one** primary key (which may span several columns). PostgreSQL creates an index for it automatically.

### 20.1 Why primary keys matter

- Two rows can never share the same key value.
- Other tables can reference it through a **foreign key**.
- Lookups by key are fast.

### 20.2 Checking existing keys

```
\d person
```

Look for the `Indexes:` section. It shows something like:

```
"person_pkey" PRIMARY KEY, btree (id)
```

> PostgreSQL names the key `tablename_pkey` by default. You need this constraint name when dropping it.

### 20.3 Dropping a primary key

```sql
ALTER TABLE person DROP CONSTRAINT person_pkey;
```

> **Note:** After dropping, the `id` column still exists, but duplicate ids are now allowed. It also keeps its `NOT NULL` setting, because dropping the key does not remove `NOT NULL`.

### 20.4 Adding a primary key

```sql
ALTER TABLE person ADD PRIMARY KEY (id);
```

With a custom constraint name:

```sql
ALTER TABLE person ADD CONSTRAINT person_pkey PRIMARY KEY (id);
```

> **Watch out:** Adding a primary key fails if the column already contains **duplicate values** or **NULLs**. Clean the data first.

### 20.5 Composite primary key (more than one column)

```sql
CREATE TABLE enrollment (
    student_id INT,
    course_id INT,
    PRIMARY KEY (student_id, course_id)
);
```

> Each column can repeat on its own, but the **combination** must be unique.

### 20.6 Typical workflow: table created without a key

```sql
-- 1. create table with no primary key
CREATE TABLE person (
    id BIGSERIAL NOT NULL,
    first_name VARCHAR(50) NOT NULL
);

-- 2. add the primary key later
ALTER TABLE person ADD PRIMARY KEY (id);
```

---

## 21. ALTER TABLE

> **Note:** `ALTER TABLE` changes the **structure** of an existing table (columns, constraints, name) without recreating it. Every change starts with `ALTER TABLE table_name`.

| Task | Syntax |
|------|--------|
| Add a column | `ADD COLUMN col type` |
| Drop a column | `DROP COLUMN col` |
| Rename a column | `RENAME COLUMN old TO new` |
| Rename the table | `RENAME TO new_name` |
| Change data type | `ALTER COLUMN col TYPE new_type` |
| Set NOT NULL | `ALTER COLUMN col SET NOT NULL` |
| Remove NOT NULL | `ALTER COLUMN col DROP NOT NULL` |
| Set default | `ALTER COLUMN col SET DEFAULT value` |
| Remove default | `ALTER COLUMN col DROP DEFAULT` |
| Add or drop a constraint | `ADD CONSTRAINT ...` / `DROP CONSTRAINT name` |

### 21.1 Add a column

```sql
ALTER TABLE person ADD COLUMN country VARCHAR(50);

-- with a default and a NOT NULL rule
ALTER TABLE person ADD COLUMN is_active BOOLEAN NOT NULL DEFAULT TRUE;
```

> **Tip:** Adding a `NOT NULL` column to a table that already has rows needs a `DEFAULT`, otherwise the existing rows would be invalid.

### 21.2 Drop a column

```sql
ALTER TABLE person DROP COLUMN country;

-- no error if the column doesn't exist
ALTER TABLE person DROP COLUMN IF EXISTS country;
```

> **Watch out:** Dropping a column permanently deletes its data.

### 21.3 Rename a column

```sql
ALTER TABLE person RENAME COLUMN email TO email_address;
```

### 21.4 Rename the table

```sql
ALTER TABLE person RENAME TO people;
```

### 21.5 Change a column's data type

```sql
ALTER TABLE person ALTER COLUMN first_name TYPE VARCHAR(100);
```

If PostgreSQL can't convert automatically (for example text to integer), use `USING`:

```sql
ALTER TABLE person
ALTER COLUMN zip_code TYPE INT USING zip_code::INT;
```

> **Watch out:** Shrinking a type (for example `VARCHAR(100)` to `VARCHAR(10)`) fails if existing data doesn't fit.

### 21.6 NOT NULL and DEFAULT

```sql
ALTER TABLE person ALTER COLUMN email SET NOT NULL;
ALTER TABLE person ALTER COLUMN email DROP NOT NULL;

ALTER TABLE person ALTER COLUMN gender SET DEFAULT 'Unknown';
ALTER TABLE person ALTER COLUMN gender DROP DEFAULT;
```

### 21.7 Multiple changes in one statement

```sql
ALTER TABLE person
    ADD COLUMN phone VARCHAR(15),
    ADD COLUMN city VARCHAR(50);
```

---

## 22. Unique Constraints

> **Note:** A `UNIQUE` constraint ensures **no two rows have the same value** in a column (or combination of columns). Unlike a primary key, a table can have **many** unique constraints, and the column **may contain NULLs**. Multiple NULLs are allowed, because NULL is not considered equal to NULL.

### 22.1 Define at table creation

```sql
CREATE TABLE person (
    id BIGSERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    email VARCHAR(150) UNIQUE
);
```

### 22.2 Add to an existing table

```sql
-- named constraint (recommended)
ALTER TABLE person ADD CONSTRAINT unique_email UNIQUE (email);

-- unnamed (PostgreSQL names it person_email_key)
ALTER TABLE person ADD UNIQUE (email);
```

### 22.3 Drop a unique constraint

```sql
ALTER TABLE person DROP CONSTRAINT unique_email;
```

### 22.4 Unique across multiple columns

```sql
ALTER TABLE person
ADD CONSTRAINT unique_name_dob UNIQUE (first_name, last_name, date_of_birth);
```

> Each column can repeat on its own, but the **combination** must be unique.

### 22.5 What happens on a duplicate

```sql
INSERT INTO person (first_name, last_name, gender, date_of_birth, email)
VALUES ('Ravi', 'Kumar', 'Male', DATE '1992-05-01', 'swaroopa@gmail.com');
-- ERROR: duplicate key value violates unique constraint "unique_email"
```

### 22.6 Primary key vs Unique

| Feature | `PRIMARY KEY` | `UNIQUE` |
|---------|---------------|----------|
| Per table | Only one | Many |
| NULL allowed | No | Yes (multiple NULLs) |
| Purpose | Identify the row | Prevent duplicate values |
| Can be referenced by foreign key | Yes | Yes |

> **Watch out:** Adding `UNIQUE` fails if duplicate values already exist. Find them first:
>
> ```sql
> SELECT email, COUNT(*) FROM person GROUP BY email HAVING COUNT(*) > 1;
> ```

---

## 23. Check Constraints

> **Note:** A `CHECK` constraint validates data with a **condition**. Every inserted or updated row must satisfy the condition, otherwise PostgreSQL rejects it. It is useful for enforcing business rules, such as allowed values and valid ranges.

### 23.1 Define at table creation

```sql
CREATE TABLE product (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    price NUMERIC(10, 2) CHECK (price > 0),
    quantity INT CHECK (quantity >= 0)
);
```

### 23.2 Add to an existing table

```sql
ALTER TABLE person
ADD CONSTRAINT gender_constraint
CHECK (gender = 'Female' OR gender = 'Male');
```

The same rule written with `IN`:

```sql
ALTER TABLE person
ADD CONSTRAINT gender_constraint
CHECK (gender IN ('Female', 'Male'));
```

### 23.3 What happens when the rule is broken

```sql
INSERT INTO person (first_name, last_name, gender, date_of_birth)
VALUES ('Alex', 'Lee', 'Other', DATE '1995-01-01');
-- ERROR: new row for relation "person" violates check constraint "gender_constraint"
```

### 23.4 Drop a check constraint

```sql
ALTER TABLE person DROP CONSTRAINT gender_constraint;
```

### 23.5 Check across multiple columns

```sql
ALTER TABLE product
ADD CONSTRAINT sale_price_check CHECK (sale_price <= price);
```

### 23.6 More examples

```sql
CHECK (age BETWEEN 18 AND 60)
CHECK (email LIKE '%@%')
CHECK (end_date >= start_date)
CHECK (LENGTH(password) >= 8)
```

> **Watch out:**
> - Adding a check to an existing table fails if any current row violates it.
> - A `CHECK` that evaluates to `NULL` **passes**, so combine with `NOT NULL` if NULLs shouldn't be allowed.
> - If you don't name the constraint, PostgreSQL generates a name like `person_gender_check`. Naming it yourself makes error messages and dropping easier.

---

## 24. Delete Rows From Table

> **Note:** `DELETE FROM` removes **rows** (not the table itself). Always use `WHERE` to choose which rows to remove. **Without `WHERE`, every row is deleted.**

### 24.1 Delete specific rows

```sql
-- delete one row by id
DELETE FROM person WHERE id = 1;

-- delete by condition
DELETE FROM person WHERE gender = 'Female' AND country_of_birth = 'China';

-- delete using IN
DELETE FROM person WHERE id IN (3, 5, 7);
```

### 24.2 Delete all rows

```sql
DELETE FROM person;
```

> **Watch out:** This empties the table. Run `SELECT * FROM person WHERE ...` with the same condition first to preview what will be deleted.

### 24.3 RETURNING (see what was deleted)

```sql
DELETE FROM person WHERE id = 2 RETURNING *;
```

> `RETURNING` shows the deleted rows. It is PostgreSQL specific and handy for confirming the change.

### 24.4 Deleting rows with foreign keys

> **Note:** If other tables reference the row through a foreign key, the delete fails unless the foreign key is defined with `ON DELETE CASCADE` (delete child rows too) or the child rows are removed first.

```sql
-- error example
-- ERROR: update or delete on table "person" violates foreign key constraint ...
```

### 24.5 DELETE vs TRUNCATE vs DROP

| Command | What it removes | Table structure | `WHERE` allowed |
|---------|-----------------|-----------------|-----------------|
| `DELETE FROM t WHERE ...` | Selected rows | Stays | Yes |
| `DELETE FROM t` | All rows | Stays | No |
| `TRUNCATE TABLE t` | All rows (fast) | Stays | No |
| `DROP TABLE t` | Rows **and** the table | Gone | No |

```sql
TRUNCATE TABLE person;                       -- fast, removes all rows
TRUNCATE TABLE person RESTART IDENTITY;      -- also resets the id counter to 1
DROP TABLE person;                           -- removes the table completely
```

> **Tip:** After `DELETE`, a `BIGSERIAL` counter does **not** reset, so new rows continue from the last used number.

---

## 25. Add Row to Table

> **Note:** `INSERT INTO` adds new rows. Basic insert was covered in Part 1 (section 4). Here are the extra forms you will use in practice.

### 25.1 Basic insert (recap)

```sql
INSERT INTO person (first_name, last_name, gender, date_of_birth, email)
VALUES ('swaroopa', 'reddy', 'Female', DATE '1990-10-20', 'swaroopa@gmail.com');
```

### 25.2 Insert multiple rows at once

```sql
INSERT INTO person (first_name, last_name, gender, date_of_birth, email)
VALUES
    ('Ravi', 'Kumar', 'Male', DATE '1992-05-01', 'ravi@gmail.com'),
    ('Anita', 'Sharma', 'Female', DATE '1988-03-12', NULL),
    ('John', 'Smith', 'Male', DATE '1995-07-30', 'john@gmail.com');
```

> This is faster than running separate `INSERT` statements.

### 25.3 Omitting optional columns

```sql
INSERT INTO person (first_name, last_name, gender, date_of_birth)
VALUES ('Meena', 'Rao', 'Female', DATE '1993-09-09');
-- email becomes NULL
```

### 25.4 Using DEFAULT

```sql
INSERT INTO person (id, first_name, last_name, gender, date_of_birth)
VALUES (DEFAULT, 'Kiran', 'Patel', 'Male', DATE '1991-01-15');
```

> **Tip:** Always list column names. Inserting without a column list depends on the exact column order and breaks if the table structure changes.

### 25.5 RETURNING (get the inserted row back)

```sql
INSERT INTO person (first_name, last_name, gender, date_of_birth)
VALUES ('Sara', 'Khan', 'Female', DATE '1994-04-04')
RETURNING id;
```

> Useful to get the auto-generated `id` right after inserting.

### 25.6 ON CONFLICT (handling duplicates)

> **Note:** If an insert would violate a `UNIQUE` or primary key constraint, you can skip it or update the existing row instead of getting an error.

```sql
-- skip the row silently if the email already exists
INSERT INTO person (first_name, last_name, gender, date_of_birth, email)
VALUES ('Ravi', 'Kumar', 'Male', DATE '1992-05-01', 'ravi@gmail.com')
ON CONFLICT (email) DO NOTHING;
```

```sql
-- update the existing row instead (an "upsert")
INSERT INTO person (first_name, last_name, gender, date_of_birth, email)
VALUES ('Ravi', 'Kumar', 'Male', DATE '1992-05-01', 'ravi@gmail.com')
ON CONFLICT (email)
DO UPDATE SET first_name = EXCLUDED.first_name,
              last_name = EXCLUDED.last_name;
```

> `EXCLUDED` refers to the row you tried to insert. `ON CONFLICT (email)` requires a unique constraint or index on `email`, which links back to section 22.

### 25.7 Insert from another table

```sql
INSERT INTO person_backup (first_name, last_name, gender, date_of_birth, email)
SELECT first_name, last_name, gender, date_of_birth, email
FROM person
WHERE gender = 'Female';
```