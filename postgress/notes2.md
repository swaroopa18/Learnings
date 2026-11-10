# PostgreSQL Notes - Part 6

Continues from Part 5. Covers deleting rows, `UPDATE`, `ON CONFLICT DO NOTHING`, upsert, foreign keys, joins and adding relationships between tables.

> **Numbering note:** Part 5 ended with a "Quick Summary" numbered 26. Here the topics follow your headings (26 to 31), so renumber if you merge the files.

Sample tables used in the examples:

```sql
CREATE TABLE car (
    id BIGSERIAL PRIMARY KEY,
    make VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    price NUMERIC(19, 2) NOT NULL
);

CREATE TABLE person (
    id BIGSERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    gender VARCHAR(7) NOT NULL,
    date_of_birth DATE NOT NULL,
    email VARCHAR(150) UNIQUE
);
```

---

## 26. Delete Row From Table

> **Note:** The basics of `DELETE` were covered in Part 5 (section 24). This section adds the practical extras. Remember: **`DELETE` without `WHERE` removes every row.**

### 26.1 Quick recap

```sql
DELETE FROM person WHERE id = 1;
DELETE FROM person WHERE gender = 'Female' AND first_name LIKE 'A%';
DELETE FROM person WHERE id IN (3, 5, 7);
```

### 26.2 Delete with a subquery

```sql
-- delete people who have no email
DELETE FROM person
WHERE id IN (SELECT id FROM person WHERE email IS NULL);

-- simpler version of the same thing
DELETE FROM person WHERE email IS NULL;
```

### 26.3 Delete using another table (USING)

> **Note:** `USING` lets you join another table to decide which rows to delete. It is PostgreSQL's version of a join-delete.

```sql
-- delete people whose car costs more than 100000
-- (assumes person.car_id exists, see section 31)
DELETE FROM person
USING car
WHERE person.car_id = car.id
  AND car.price > 100000;
```

### 26.4 Delete only a few rows

> PostgreSQL's `DELETE` has no `LIMIT`. Use a subquery instead.

```sql
DELETE FROM person
WHERE id IN (
    SELECT id FROM person ORDER BY id LIMIT 5
);
```

### 26.5 RETURNING

```sql
DELETE FROM person WHERE id = 2 RETURNING *;
```

### 26.6 Safe deleting with a transaction

> **Note:** Wrap risky deletes in a transaction. If the result looks wrong, `ROLLBACK` undoes it. If it looks right, `COMMIT` saves it.

```sql
BEGIN;
DELETE FROM person WHERE gender = 'Female';
SELECT COUNT(*) FROM person;     -- check the result
ROLLBACK;                        -- undo (or COMMIT; to keep)
```

> **Tip:** Run a `SELECT` with the same `WHERE` first to preview exactly which rows will be removed.

---

## 27. Update Records

> **Note:** `UPDATE` changes values in **existing rows**. Always use `WHERE` to pick the rows. **Without `WHERE`, every row is updated.**

**Syntax**

```sql
UPDATE table_name
SET column1 = value1, column2 = value2
WHERE condition;
```

### 27.1 Update one column

```sql
UPDATE person
SET email = 'new_email@gmail.com'
WHERE id = 5;
```

### 27.2 Update multiple columns

```sql
UPDATE person
SET first_name = 'Swaroopa',
    last_name = 'Reddy',
    gender = 'Female'
WHERE id = 1;
```

### 27.3 Update using expressions

> The new value can be calculated from the current value.

```sql
-- increase every car price by 10%
UPDATE car SET price = price * 1.10;

-- increase price by 5000 for one make
UPDATE car SET price = price + 5000 WHERE make = 'Toyota';

-- round prices to 2 decimals
UPDATE car SET price = ROUND(price, 2);
```

### 27.4 Update to NULL or default

```sql
UPDATE person SET email = NULL WHERE id = 3;
UPDATE person SET gender = DEFAULT WHERE id = 4;
```

### 27.5 Update with multiple conditions

```sql
UPDATE person
SET email = 'unknown@example.com'
WHERE email IS NULL AND gender = 'Male';
```

### 27.6 RETURNING

```sql
UPDATE person
SET first_name = 'Ravi'
WHERE id = 2
RETURNING *;
```

> Shows the **new** values of the updated rows.

### 27.7 Update using another table (FROM)

```sql
-- set each person's email domain from another table
UPDATE person
SET email = n.new_email
FROM new_emails AS n
WHERE person.id = n.person_id;
```

### 27.8 Common UPDATE mistakes

| Mistake | Result |
|---------|--------|
| Forgetting `WHERE` | Every row in the table is changed |
| Wrong condition | Wrong rows updated |
| Violating a constraint | Error (`UNIQUE`, `CHECK`, `NOT NULL`, and so on) |

> **Tip:** Test inside `BEGIN; ... ROLLBACK;` just like with `DELETE`.

---

## 28. ON CONFLICT DO NOTHING

> **Note:** Normally, inserting a row that breaks a `UNIQUE` or primary key rule gives an **error** and stops the statement. `ON CONFLICT DO NOTHING` tells PostgreSQL to **silently skip** that row instead. It requires a unique or primary key constraint to detect the conflict.

### 28.1 The problem

```sql
INSERT INTO person (id, first_name, last_name, gender, date_of_birth)
VALUES (1, 'Ravi', 'Kumar', 'Male', DATE '1992-05-01');
-- ERROR: duplicate key value violates unique constraint "person_pkey"
```

### 28.2 The fix

```sql
INSERT INTO person (id, first_name, last_name, gender, date_of_birth)
VALUES (1, 'Ravi', 'Kumar', 'Male', DATE '1992-05-01')
ON CONFLICT (id) DO NOTHING;
-- INSERT 0 0  (no row inserted, no error)
```

### 28.3 Conflict target options

```sql
-- by column
ON CONFLICT (email) DO NOTHING;

-- by constraint name
ON CONFLICT ON CONSTRAINT person_email_key DO NOTHING;

-- any conflict (no target)
ON CONFLICT DO NOTHING;
```

> **Tip:** `ON CONFLICT DO NOTHING` without a target skips on **any** unique violation. Naming the column is safer, because other errors (such as `NOT NULL` or `CHECK`) are still reported.

### 28.4 With multiple rows

```sql
INSERT INTO person (first_name, last_name, gender, date_of_birth, email)
VALUES
    ('Ravi', 'Kumar', 'Male', DATE '1992-05-01', 'ravi@gmail.com'),
    ('Anita', 'Sharma', 'Female', DATE '1988-03-12', 'anita@gmail.com')
ON CONFLICT (email) DO NOTHING;
```

> Rows that conflict are skipped and the others are inserted.

### 28.5 RETURNING with DO NOTHING

> **Watch out:** `RETURNING` only returns rows that were **actually inserted**. Skipped rows are not returned.

```sql
INSERT INTO person (first_name, last_name, gender, date_of_birth, email)
VALUES ('Ravi', 'Kumar', 'Male', DATE '1992-05-01', 'ravi@gmail.com')
ON CONFLICT (email) DO NOTHING
RETURNING id;
-- returns nothing if the email already existed
```

---

## 29. Upsert

> **Note:** **Upsert = Update + Insert.** If the row doesn't exist, insert it. If it already exists (conflict on a unique column), **update** the existing row instead. In PostgreSQL it is written as `INSERT ... ON CONFLICT ... DO UPDATE`.

### 29.1 Basic upsert

```sql
INSERT INTO person (first_name, last_name, gender, date_of_birth, email)
VALUES ('Ravi', 'Kumar', 'Male', DATE '1992-05-01', 'ravi@gmail.com')
ON CONFLICT (email)
DO UPDATE SET first_name = EXCLUDED.first_name,
              last_name = EXCLUDED.last_name;
```

> **`EXCLUDED`** is a special table holding the row you **tried to insert**. The plain table name (`person`) refers to the **existing** row.

### 29.2 Updating only some columns

```sql
INSERT INTO person (first_name, last_name, gender, date_of_birth, email)
VALUES ('Ravi', 'K', 'Male', DATE '1992-05-01', 'ravi@gmail.com')
ON CONFLICT (email)
DO UPDATE SET last_name = EXCLUDED.last_name;
-- other columns of the existing row stay unchanged
```

### 29.3 Using the old value (counters)

```sql
-- page_views(page, views) with page as primary key
INSERT INTO page_views (page, views)
VALUES ('home', 1)
ON CONFLICT (page)
DO UPDATE SET views = page_views.views + 1;
```

### 29.4 Conditional update

```sql
-- only update if the new price is lower
INSERT INTO car (id, make, model, price)
VALUES (1, 'Toyota', 'Corolla', 18000)
ON CONFLICT (id)
DO UPDATE SET price = EXCLUDED.price
WHERE EXCLUDED.price < car.price;
```

### 29.5 Upsert rules

| Rule | Explanation |
|------|-------------|
| Needs a unique target | The conflict column must have a `UNIQUE` or primary key constraint (or unique index) |
| One conflict target for `DO UPDATE` | You must specify `ON CONFLICT (column)` or `ON CONSTRAINT name` |
| Duplicates within one statement | Two rows in the same `INSERT` hitting the same key cause: `ON CONFLICT DO UPDATE command cannot affect row a second time` |
| `RETURNING` | Returns both inserted and updated rows |

### 29.6 DO NOTHING vs DO UPDATE

| Feature | `DO NOTHING` | `DO UPDATE` (upsert) |
|---------|--------------|----------------------|
| On conflict | Skip the new row | Update the existing row |
| Existing data | Unchanged | Changed |
| `RETURNING` on conflict | Returns nothing | Returns the updated row |
| Use when | Ignoring duplicates is fine | You want the latest values to win |

---

## 30. Foreign Key and Joins

### 30.1 Foreign key

> **Note:** A **foreign key** is a column that points to the **primary key of another table**. It enforces **referential integrity**: you can't reference a row that doesn't exist, and you can't delete a row that is still referenced (unless you set a rule for it).

- **Parent table**: the table being referenced (`car`).
- **Child table**: the table holding the foreign key (`person`).

### 30.2 Creating a foreign key

> The parent table must be created **first**.

```sql
CREATE TABLE car (
    id BIGSERIAL PRIMARY KEY,
    make VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    price NUMERIC(19, 2) NOT NULL
);

CREATE TABLE person (
    id BIGSERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    gender VARCHAR(7) NOT NULL,
    date_of_birth DATE NOT NULL,
    email VARCHAR(150),
    car_id BIGINT REFERENCES car (id),
    UNIQUE (car_id)
);
```

> `UNIQUE (car_id)` makes this a **one-to-one** relationship (one person has at most one car, and a car belongs to at most one person). Remove it for **one-to-many**.

### 30.3 Foreign key rules in action

```sql
INSERT INTO car (make, model, price) VALUES ('Toyota', 'Corolla', 18000);

-- works: car id 1 exists
INSERT INTO person (first_name, last_name, gender, date_of_birth, car_id)
VALUES ('Ravi', 'Kumar', 'Male', DATE '1992-05-01', 1);

-- fails: car id 99 does not exist
INSERT INTO person (first_name, last_name, gender, date_of_birth, car_id)
VALUES ('Anita', 'Sharma', 'Female', DATE '1988-03-12', 99);
-- ERROR: insert or update on table "person" violates foreign key constraint
```

### 30.4 ON DELETE actions

> **Note:** These decide what happens to child rows when the parent row is deleted.

| Action | Behavior |
|--------|----------|
| `NO ACTION` (default) | Error if child rows exist |
| `RESTRICT` | Error immediately if child rows exist |
| `CASCADE` | Delete the child rows too |
| `SET NULL` | Set the foreign key column to NULL |
| `SET DEFAULT` | Set the foreign key column to its default |

```sql
car_id BIGINT REFERENCES car (id) ON DELETE SET NULL
car_id BIGINT REFERENCES car (id) ON DELETE CASCADE
```

> **Watch out:** `CASCADE` can delete a lot of data silently. Use it carefully.

---

### 30.5 Joins

> **Note:** A **join** combines rows from two or more tables based on a related column, usually primary key = foreign key. Tables are matched with `ON`.

| Join type | Returns |
|-----------|---------|
| `INNER JOIN` | Only rows that match in **both** tables |
| `LEFT JOIN` | **All** rows from the left table, plus matches from the right (NULL if none) |
| `RIGHT JOIN` | **All** rows from the right table, plus matches from the left (NULL if none) |
| `FULL JOIN` | All rows from **both** tables (NULL where no match) |
| `CROSS JOIN` | Every row combined with every row (all combinations) |

Sample data used below:

```
person: Ravi (car 1), Anita (car 2), Meena (no car)
car:    1 Toyota Corolla, 2 Honda Civic, 3 Ford Focus (no owner)
```

### 30.6 INNER JOIN

> Only people **who have a car** and cars **that have an owner**.

```sql
SELECT person.first_name, car.make, car.model
FROM person
INNER JOIN car ON person.car_id = car.id;
```

Result: Ravi / Toyota, Anita / Honda. Meena and the Ford are left out.

> `JOIN` alone means `INNER JOIN`.

### 30.7 LEFT JOIN

> **All people**, with car details if they have one, otherwise NULL.

```sql
SELECT person.first_name, car.make, car.model
FROM person
LEFT JOIN car ON person.car_id = car.id;
```

Result: Ravi / Toyota, Anita / Honda, Meena / NULL.

Find people **without** a car:

```sql
SELECT person.first_name
FROM person
LEFT JOIN car ON person.car_id = car.id
WHERE car.id IS NULL;
```

### 30.8 RIGHT JOIN

> **All cars**, with the owner if there is one.

```sql
SELECT person.first_name, car.make, car.model
FROM person
RIGHT JOIN car ON person.car_id = car.id;
```

Result: Ravi / Toyota, Anita / Honda, NULL / Ford.

### 30.9 FULL JOIN

```sql
SELECT person.first_name, car.make, car.model
FROM person
FULL JOIN car ON person.car_id = car.id;
```

Result: all of the above combined, including Meena (no car) and the Ford (no owner).

### 30.10 Table aliases in joins

```sql
SELECT p.first_name, c.make, c.price
FROM person AS p
JOIN car AS c ON p.car_id = c.id
WHERE c.price > 15000
ORDER BY c.price DESC;
```

### 30.11 USING (shortcut when column names match)

```sql
-- orders(id, customer_id, ...) and customer(customer_id, name, ...)
SELECT * FROM orders JOIN customer USING (customer_id);
-- same as: ... JOIN customer ON orders.customer_id = customer.customer_id
```

> `USING (col)` is a shorthand for `ON a.col = b.col` and shows the column only once in the output. It only works when **both tables have a column with the same name**. In our `person` and `car` tables the link columns are named differently (`person.car_id` and `car.id`), and `id` means something different in each table, so use `ON person.car_id = car.id` there.

### 30.12 CROSS JOIN

```sql
SELECT p.first_name, c.make
FROM person p
CROSS JOIN car c;
-- 3 people x 3 cars = 9 rows
```

### 30.13 Joins with aggregates

```sql
-- total value of cars owned, by gender
SELECT p.gender, SUM(c.price) AS total_car_value
FROM person p
JOIN car c ON p.car_id = c.id
GROUP BY p.gender;

-- number of people per car make
SELECT c.make, COUNT(p.id) AS owners
FROM car c
LEFT JOIN person p ON p.car_id = c.id
GROUP BY c.make;
```

### 30.14 Ambiguous column error

> If both tables have a column with the same name, prefix it with the table name or alias.

```sql
SELECT id FROM person JOIN car ON person.car_id = car.id;
-- ERROR: column reference "id" is ambiguous

SELECT person.id, car.id FROM person JOIN car ON person.car_id = car.id;
```

---

## 31. Adding Relationships Between Tables

> **Note:** If the tables already exist without a link, use `ALTER TABLE` to add a foreign key column afterwards, then fill it with `UPDATE`. This is the usual workflow on a database that is already in use.

### 31.1 Tables with no relationship yet

```sql
CREATE TABLE car (
    id BIGSERIAL PRIMARY KEY,
    make VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    price NUMERIC(19, 2) NOT NULL
);

CREATE TABLE person (
    id BIGSERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL
);
```

### 31.2 Step 1: Add the foreign key column

```sql
ALTER TABLE person ADD COLUMN car_id BIGINT REFERENCES car (id);
```

Or, as a named constraint:

```sql
ALTER TABLE person ADD COLUMN car_id BIGINT;

ALTER TABLE person
ADD CONSTRAINT fk_person_car
FOREIGN KEY (car_id) REFERENCES car (id);
```

### 31.3 Step 2: Make it one-to-one (optional)

```sql
ALTER TABLE person ADD CONSTRAINT unique_car_id UNIQUE (car_id);
```

### 31.4 Step 3: Link the existing rows

```sql
UPDATE person SET car_id = 2 WHERE id = 1;
UPDATE person SET car_id = 1 WHERE id = 2;
```

### 31.5 Step 4: Check the relationship

```sql
SELECT p.first_name, c.make, c.model
FROM person p
LEFT JOIN car c ON p.car_id = c.id;
```

### 31.6 Dropping a relationship

```sql
ALTER TABLE person DROP CONSTRAINT fk_person_car;
-- or drop the column entirely
ALTER TABLE person DROP COLUMN car_id;
```

> Use `\d person` to see the actual constraint name (for an unnamed one it is usually `person_car_id_fkey`).

### 31.7 Relationship types

| Type | How to build it | Example |
|------|-----------------|---------|
| **One-to-one** | Foreign key + `UNIQUE` on it | Person and passport |
| **One-to-many** | Foreign key on the "many" side (no `UNIQUE`) | One customer, many orders |
| **Many-to-many** | A third **junction table** with two foreign keys | Students and courses |

#### One-to-many example

```sql
CREATE TABLE customer (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE orders (
    id BIGSERIAL PRIMARY KEY,
    order_date DATE NOT NULL,
    customer_id BIGINT NOT NULL REFERENCES customer (id)
);
-- one customer can have many orders
```

#### Many-to-many example

```sql
CREATE TABLE student (id BIGSERIAL PRIMARY KEY, name VARCHAR(50) NOT NULL);
CREATE TABLE course  (id BIGSERIAL PRIMARY KEY, title VARCHAR(50) NOT NULL);

CREATE TABLE enrollment (
    student_id BIGINT REFERENCES student (id),
    course_id BIGINT REFERENCES course (id),
    PRIMARY KEY (student_id, course_id)
);
```

### 31.8 Common problems

| Problem | Cause and fix |
|---------|---------------|
| `violates foreign key constraint` when adding the constraint | Existing rows reference ids that don't exist. Fix or NULL them first |
| Can't drop the parent table | Child tables still depend on it. Drop the child first, or use `DROP TABLE ... CASCADE` |
| Can't delete a parent row | Child rows reference it. Delete the children, or use `ON DELETE CASCADE` / `SET NULL` |
| Type mismatch error | The foreign key type must match the referenced key (`BIGSERIAL` pairs with `BIGINT`) |

---

## Sample Data

Every result below is based on this data, so you can run it and compare.

```sql
CREATE TABLE car (
    id BIGSERIAL PRIMARY KEY,
    make VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    price NUMERIC(19, 2) NOT NULL
);

CREATE TABLE person (
    id BIGSERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    car_id BIGINT REFERENCES car (id),
    UNIQUE (car_id)
);

INSERT INTO car (make, model, price) VALUES
    ('Toyota', 'Corolla', 18000),
    ('Honda',  'Civic',   20000),
    ('Ford',   'Focus',   17000);

INSERT INTO person (first_name, last_name, car_id) VALUES
    ('Ravi',  'Kumar',  1),
    ('Anita', 'Sharma', 2),
    ('Meena', 'Rao',    NULL),
    ('John',  'Smith',  NULL);
```

**person**

| id | first_name | last_name | car_id |
|----|------------|-----------|--------|
| 1 | Ravi | Kumar | 1 |
| 2 | Anita | Sharma | 2 |
| 3 | Meena | Rao | NULL |
| 4 | John | Smith | NULL |

**car**

| id | make | model | price |
|----|------|-------|-------|
| 1 | Toyota | Corolla | 18000 |
| 2 | Honda | Civic | 20000 |
| 3 | Ford | Focus | 17000 |

> Meena and John have **no car**. The Ford Focus has **no owner**. These unmatched rows are what make the two joins behave differently.

---

## 32. Inner Joins

> **Note:** An `INNER JOIN` returns only the rows that have a **match in both tables**. If a row in either table has no partner, it is left out of the result. `JOIN` on its own means `INNER JOIN`.

### 32.1 Syntax

```sql
SELECT columns
FROM table_a
INNER JOIN table_b ON table_a.column = table_b.column;
```

### 32.2 Basic example

```sql
SELECT person.first_name, car.make, car.model
FROM person
INNER JOIN car ON person.car_id = car.id;
```

| first_name | make | model |
|------------|------|-------|
| Ravi | Toyota | Corolla |
| Anita | Honda | Civic |

> Meena and John are missing (no car), and so is the Ford (no owner).

### 32.3 How the match works

```
person.car_id  =  car.id
     1         =    1   -> match: Ravi + Toyota
     2         =    2   -> match: Anita + Honda
   NULL        =    ?   -> no match (NULL never equals anything)
                   3    -> no person points to it, no match
```

> **Note:** `NULL = anything` is never true, so rows with a NULL foreign key never match in an inner join.

### 32.4 Selecting all columns

```sql
SELECT * FROM person JOIN car ON person.car_id = car.id;
```

> Returns the columns of **both** tables side by side. Both have an `id` column, so you will see two `id` columns. Prefer naming the columns you need.

### 32.5 Table aliases

```sql
SELECT p.first_name, c.make, c.price
FROM person AS p
JOIN car AS c ON p.car_id = c.id;
```

> Aliases (`p`, `c`) keep queries short and remove ambiguity when both tables share a column name such as `id`.

### 32.6 Filtering with WHERE

```sql
SELECT p.first_name, c.make, c.price
FROM person p
JOIN car c ON p.car_id = c.id
WHERE c.price > 18000;
```

| first_name | make | price |
|------------|------|-------|
| Anita | Honda | 20000.00 |

> For an inner join, a condition in `WHERE` or in `ON` gives the **same result**. This changes for left joins (see 33.6).

### 32.7 Sorting, limiting and expressions

```sql
SELECT p.first_name || ' ' || p.last_name AS owner,
       c.make || ' ' || c.model AS car,
       ROUND(c.price * 0.9, 2) AS discounted_price
FROM person p
JOIN car c ON p.car_id = c.id
ORDER BY c.price DESC
LIMIT 5;
```

> `||` joins text together (concatenation).

### 32.8 Joining more than three tables

> **Note:** Chain joins one after another. Each `JOIN` adds one more table.

```sql
CREATE TABLE insurance (
    id BIGSERIAL PRIMARY KEY,
    provider VARCHAR(50) NOT NULL,
    person_id BIGINT NOT NULL REFERENCES person (id)
);

INSERT INTO insurance (provider, person_id) VALUES ('LIC', 1);
```

```sql
SELECT p.first_name, c.make, i.provider
FROM person p
JOIN car c ON p.car_id = c.id
JOIN insurance i ON i.person_id = p.id;
```

| first_name | make | provider |
|------------|------|----------|
| Ravi | Toyota | LIC |

> A row survives only if it matches in **every** join. Anita has a car but no insurance, so she is dropped.

### 32.9 Inner join with GROUP BY

```sql
-- total value of cars owned
SELECT SUM(c.price) AS total_value
FROM person p
JOIN car c ON p.car_id = c.id;
-- 38000.00

-- number of owners per make
SELECT c.make, COUNT(*) AS owners
FROM person p
JOIN car c ON p.car_id = c.id
GROUP BY c.make;
```

### 32.10 JOIN ... USING

> **Note:** When both tables have a column with the **same name**, `USING` is a shorthand for `ON`, and the column appears only once in the output.

```sql
-- orders(id, customer_id, ...) and customer(customer_id, name, ...)
SELECT * FROM orders JOIN customer USING (customer_id);
-- same as: ... JOIN customer ON orders.customer_id = customer.customer_id
```

> In `person` and `car`, the link columns are named differently (`car_id` vs `id`), so `USING` doesn't apply there.

### 32.11 Inner join order doesn't matter

```sql
FROM person p JOIN car c ON p.car_id = c.id
-- gives the same rows as
FROM car c JOIN person p ON p.car_id = c.id
```

> Row order in the output may differ, and without `ORDER BY` it is never guaranteed.

### 32.12 Common mistakes

| Mistake | Result |
|---------|--------|
| Forgetting `ON` | Error (or, with a comma join, a cross join with every combination) |
| Wrong columns in `ON` | Wrong or empty results |
| Using `SELECT id` when both tables have `id` | `ERROR: column reference "id" is ambiguous` |
| Expecting unmatched rows to appear | Inner join drops them. Use a left join instead |

---

## 33. Left Joins

> **Note:** A `LEFT JOIN` (also written `LEFT OUTER JOIN`) returns **all rows from the left table**, plus the matching rows from the right table. Where there is no match, the right-side columns are filled with `NULL`. The "left" table is the one written **before** the `JOIN` keyword.

### 33.1 Syntax

```sql
SELECT columns
FROM left_table
LEFT JOIN right_table ON left_table.column = right_table.column;
```

### 33.2 Basic example

```sql
SELECT p.first_name, c.make, c.model
FROM person p
LEFT JOIN car c ON p.car_id = c.id;
```

| first_name | make | model |
|------------|------|-------|
| Ravi | Toyota | Corolla |
| Anita | Honda | Civic |
| Meena | NULL | NULL |
| John | NULL | NULL |

> Everyone from `person` appears. Meena and John have no car, so their car columns are NULL. The unowned Ford is not shown, because `car` is the **right** table here.

### 33.3 Inner vs Left (side by side)

| | `INNER JOIN` | `LEFT JOIN` |
|---|--------------|-------------|
| Rows from the left table | Only matched | **All** |
| Rows from the right table | Only matched | Only matched |
| No match on the right | Row dropped | Row kept, right columns are NULL |
| Rows in this example | 2 | 4 |

### 33.4 Finding rows with no match (anti-join)

> **Note:** A very common pattern: left join, then keep only rows where the right side is NULL. This finds "rows in A that have nothing in B".

```sql
-- people without a car
SELECT p.first_name
FROM person p
LEFT JOIN car c ON p.car_id = c.id
WHERE c.id IS NULL;
```

| first_name |
|------------|
| Meena |
| John |

```sql
-- cars without an owner (swap the tables)
SELECT c.make, c.model
FROM car c
LEFT JOIN person p ON p.car_id = c.id
WHERE p.id IS NULL;
```

| make | model |
|------|-------|
| Ford | Focus |

> Check `IS NULL` on a column that is **never NULL in real data**, such as the primary key (`c.id`). Checking a column that can legitimately be NULL gives false results.

### 33.5 Replacing NULLs in the output

```sql
SELECT p.first_name,
       COALESCE(c.make, 'No car') AS make,
       COALESCE(c.price, 0) AS price
FROM person p
LEFT JOIN car c ON p.car_id = c.id;
```

| first_name | make | price |
|------------|------|-------|
| Ravi | Toyota | 18000.00 |
| Anita | Honda | 20000.00 |
| Meena | No car | 0 |
| John | No car | 0 |

### 33.6 WHERE vs ON in a left join (important)

> **Watch out:** In a left join, **where you put a condition on the right table changes the result.**

**Condition in `WHERE`**: filters **after** the join, so the NULL rows are removed and the left join behaves like an inner join.

```sql
SELECT p.first_name, c.make, c.price
FROM person p
LEFT JOIN car c ON p.car_id = c.id
WHERE c.price > 18000;
```

| first_name | make | price |
|------------|------|-------|
| Anita | Honda | 20000.00 |

**Condition in `ON`**: filters **which right-side rows can match**, and all left rows are still kept.

```sql
SELECT p.first_name, c.make, c.price
FROM person p
LEFT JOIN car c ON p.car_id = c.id AND c.price > 18000;
```

| first_name | make | price |
|------------|------|-------|
| Ravi | NULL | NULL |
| Anita | Honda | 20000.00 |
| Meena | NULL | NULL |
| John | NULL | NULL |

> Rule of thumb: conditions on the **left** table go in `WHERE`. Conditions on the **right** table that shouldn't remove left rows go in `ON`.

### 33.7 Left join with aggregates

```sql
-- how many people drive each car make (including makes with 0 owners)
SELECT c.make, COUNT(p.id) AS owners
FROM car c
LEFT JOIN person p ON p.car_id = c.id
GROUP BY c.make
ORDER BY owners DESC;
```

| make | owners |
|------|--------|
| Toyota | 1 |
| Honda | 1 |
| Ford | 0 |

> **Watch out:** Use `COUNT(p.id)` (a column from the right table), not `COUNT(*)`. `COUNT(*)` counts the row itself, so Ford would wrongly show 1. `COUNT(column)` ignores NULLs.

### 33.8 Chaining left joins

```sql
SELECT p.first_name, c.make, i.provider
FROM person p
LEFT JOIN car c ON p.car_id = c.id
LEFT JOIN insurance i ON i.person_id = p.id;
```

| first_name | make | provider |
|------------|------|----------|
| Ravi | Toyota | LIC |
| Anita | Honda | NULL |
| Meena | NULL | NULL |
| John | NULL | NULL |

> All four people are kept, and each missing piece shows NULL. Compare with the inner join in 32.8, which returned just Ravi.

### 33.9 LEFT JOIN vs RIGHT JOIN

> **Note:** A `RIGHT JOIN` is a left join with the tables swapped. Most people use only `LEFT JOIN` and reorder the tables, for readability.

```sql
-- these two return the same rows
FROM person p LEFT JOIN car c ON p.car_id = c.id
FROM car c RIGHT JOIN person p ON p.car_id = c.id
```

### 33.10 When to use which

| You want... | Use |
|-------------|-----|
| Only records that exist in both tables | `INNER JOIN` |
| All records from one table, with extra info if available | `LEFT JOIN` |
| Records in A with no match in B | `LEFT JOIN ... WHERE b.id IS NULL` |
| Counts that include zeros | `LEFT JOIN` + `COUNT(right_column)` |

---

## 34. deleting records with foriegn keys
## 35. serial and sequences
## 36. extensions