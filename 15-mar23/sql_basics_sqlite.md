# 🐾 SQL Basics with Python & SQLite
### A Hands-On Guide with Animal Data

---

## Table of Contents

1. [Setup & Imports](#1-setup--imports)
2. [Creating a Database](#2-creating-a-database)
3. [Creating Tables](#3-creating-tables)
4. [Primary Keys](#4-primary-keys)
5. [Inserting Data — Our 20 Animals](#5-inserting-data--our-20-animals)
6. [Reading Data — SELECT (The R in CRUD)](#6-reading-data--select-the-r-in-crud)
7. [Updating Data — UPDATE (The U in CRUD)](#7-updating-data--update-the-u-in-crud)
8. [Deleting Data — DELETE (The D in CRUD)](#8-deleting-data--delete-the-d-in-crud)
9. [Foreign Keys & Related Tables](#9-foreign-keys--related-tables)
10. [Renaming Tables and Columns](#10-renaming-tables-and-columns)
11. [Putting It All Together](#11-putting-it-all-together)

---

## 1. Setup & Imports

SQLite comes built into Python — no installation required. All you need is the `sqlite3` module from the standard library.

```python
import sqlite3
```

That's it. No `pip install`, no server to start, no configuration files. SQLite stores everything in a single `.db` file on your disk, or optionally entirely in memory.

### Connecting to a Database

The entry point to working with SQLite is `sqlite3.connect()`. It returns a **connection** object, which represents your session with the database.

```python
import sqlite3

# Connect to a file-based database (created automatically if it doesn't exist)
connection = sqlite3.connect("zoo.db")

# Or connect to an in-memory database (great for testing — gone when the script ends)
connection = sqlite3.connect(":memory:")
```

### The Cursor

To execute SQL statements, you need a **cursor** — think of it as the "pen" you use to write SQL against the database.

```python
cursor = connection.cursor()
```

### Committing and Closing

- `connection.commit()` — saves all pending changes to the database permanently.
- `connection.close()` — closes the connection when you're done.

```python
connection.commit()
connection.close()
```

### A Clean Helper Pattern

To avoid repeating boilerplate, most Python projects use a **context manager** pattern with `with` blocks. We'll use both styles throughout this guide so you get familiar with them.

```python
import sqlite3

# Using a context manager — connection closes automatically
with sqlite3.connect("zoo.db") as connection:
    cursor = connection.cursor()
    cursor.execute("SELECT 1")   # Just a test query
    print(cursor.fetchone())     # (1,)
# Connection is automatically closed when the with block ends
```

---

## 2. Creating a Database

Creating a database in SQLite is as simple as connecting to it. If the file `zoo.db` doesn't exist, SQLite creates it. If it does exist, SQLite opens it.

```python
import sqlite3

# This single line creates the database file if it doesn't already exist
connection = sqlite3.connect("zoo.db")
print("Database created and connected successfully!")

connection.close()
```

After running this, you'll see a `zoo.db` file appear in your working directory. That file **is** the entire database — tables, data, indexes, and all.

### Checking the SQLite Version

```python
import sqlite3

connection = sqlite3.connect("zoo.db")
cursor = connection.cursor()

cursor.execute("SELECT sqlite_version()")
version = cursor.fetchone()
print(f"SQLite version: {version[0]}")

connection.close()
```

---

### 🏋️ Exercises — Section 2

**Exercise 2.1 — Create your first database**
Write a script that creates a new database called `my_first.db`, prints a confirmation message, and then closes the connection.

```python
# Your solution here
import sqlite3

connection = sqlite3.connect("my_first.db")
print("my_first.db created successfully!")
connection.close()
```

---

**Exercise 2.2 — Connect and print the SQLite version**
Connect to a database called `practice.db` and print the SQLite version using `SELECT sqlite_version()`.

```python
# Your solution here
import sqlite3

connection = sqlite3.connect("practice.db")
cursor = connection.cursor()
cursor.execute("SELECT sqlite_version()")
print("SQLite version:", cursor.fetchone()[0])
connection.close()
```

---

**Exercise 2.3 — Use a context manager**
Rewrite Exercise 2.1 using a `with` block (context manager) instead of manually calling `connection.close()`.

```python
# Your solution here
import sqlite3

with sqlite3.connect("my_first.db") as connection:
    print("Connected using a context manager!")
    print("Connection will close automatically.")
```

---

## 3. Creating Tables

A **table** is the core structure of a relational database. It stores data in rows and columns — like a spreadsheet with strict rules about what each column can contain.

### The CREATE TABLE Statement

```sql
CREATE TABLE table_name (
    column_name  DATA_TYPE  CONSTRAINTS,
    column_name  DATA_TYPE  CONSTRAINTS,
    ...
);
```

### SQLite Data Types

SQLite uses a flexible type system. The most common types you'll use are:

| Type | Description | Example Values |
|---|---|---|
| `INTEGER` | Whole numbers | `1`, `42`, `-7` |
| `REAL` | Decimal numbers | `3.14`, `9.99` |
| `TEXT` | String / text | `"Alice"`, `"Lion"` |
| `BLOB` | Binary data (files, images) | raw bytes |
| `NULL` | No value / missing | `NULL` |

### Common Column Constraints

| Constraint | Meaning |
|---|---|
| `NOT NULL` | This column must always have a value |
| `UNIQUE` | No two rows can have the same value in this column |
| `DEFAULT value` | Use this value if none is provided |
| `CHECK(condition)` | Only allow values that satisfy the condition |

### Creating the Animals Table

```python
import sqlite3

connection = sqlite3.connect("zoo.db")
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS animals (
        id        INTEGER  PRIMARY KEY AUTOINCREMENT,
        name      TEXT     NOT NULL,
        age       INTEGER  NOT NULL CHECK(age >= 0),
        kind      TEXT     NOT NULL
    )
""")

connection.commit()
print("Table 'animals' created successfully!")
connection.close()
```

A few things to note:
- `IF NOT EXISTS` prevents an error if the table already exists — always a good habit.
- `PRIMARY KEY AUTOINCREMENT` means SQLite will automatically assign a unique ID to each new row.
- `CHECK(age >= 0)` ensures no animal can have a negative age.

### Viewing Existing Tables

You can query the special `sqlite_master` table to see what tables exist in your database:

```python
import sqlite3

connection = sqlite3.connect("zoo.db")
cursor = connection.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Tables in zoo.db:", tables)

connection.close()
```

### Viewing a Table's Structure

```python
cursor.execute("PRAGMA table_info(animals)")
columns = cursor.fetchall()
for column in columns:
    print(column)
# Each row: (cid, name, type, notnull, default_value, is_primary_key)
```

---

### 🏋️ Exercises — Section 3

**Exercise 3.1 — Create a `habitats` table**
Create a table called `habitats` with columns for `id` (integer, primary key, autoincrement), `name` (text, not null), and `climate` (text). Use `IF NOT EXISTS`.

```python
# Your solution here
import sqlite3

with sqlite3.connect("zoo.db") as connection:
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS habitats (
            id      INTEGER  PRIMARY KEY AUTOINCREMENT,
            name    TEXT     NOT NULL,
            climate TEXT
        )
    """)
    print("Table 'habitats' created!")
```

---

**Exercise 3.2 — Inspect the animals table**
Write a script that connects to `zoo.db` and prints the column information for the `animals` table using `PRAGMA table_info`.

```python
# Your solution here
import sqlite3

with sqlite3.connect("zoo.db") as connection:
    cursor = connection.cursor()
    cursor.execute("PRAGMA table_info(animals)")
    columns = cursor.fetchall()
    print("Columns in 'animals':")
    for col in columns:
        print(f"  Column: {col[1]}, Type: {col[2]}, Not Null: {bool(col[3])}")
```

---

**Exercise 3.3 — Create a `keepers` table**
Create a table called `keepers` with: `id` (integer, primary key, autoincrement), `name` (text, not null, unique), `years_experience` (integer, default 0, check it's >= 0).

```python
# Your solution here
import sqlite3

with sqlite3.connect("zoo.db") as connection:
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS keepers (
            id                INTEGER  PRIMARY KEY AUTOINCREMENT,
            name              TEXT     NOT NULL UNIQUE,
            years_experience  INTEGER  DEFAULT 0 CHECK(years_experience >= 0)
        )
    """)
    print("Table 'keepers' created!")
```

---

## 4. Primary Keys

A **primary key** is a column (or combination of columns) that uniquely identifies every row in a table. Think of it as each row's unique ID badge — no two rows can ever have the same primary key value, and it can never be `NULL`.

### Why Primary Keys Matter

Without a primary key, you have no guaranteed way to refer to a specific row. If you have two animals both named "Leo" who are both lions, how do you update or delete just one of them? The primary key (`id`) gives each record an unambiguous identity.

```
Without primary key:
  name="Leo", age=5, kind="Lion"    ← which Leo do you mean?
  name="Leo", age=5, kind="Lion"

With primary key:
  id=1, name="Leo", age=5, kind="Lion"   ← id=1 specifically
  id=2, name="Leo", age=5, kind="Lion"   ← id=2 specifically
```

### AUTOINCREMENT in SQLite

When you mark a column as `INTEGER PRIMARY KEY AUTOINCREMENT`, SQLite automatically assigns the next available integer each time you insert a row. You never have to supply the `id` yourself.

```python
import sqlite3

with sqlite3.connect("zoo.db") as connection:
    cursor = connection.cursor()

    # Create a simple demo table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS demo (
            id    INTEGER  PRIMARY KEY AUTOINCREMENT,
            label TEXT     NOT NULL
        )
    """)

    # Insert rows WITHOUT specifying an id
    cursor.execute("INSERT INTO demo (label) VALUES ('first')")
    cursor.execute("INSERT INTO demo (label) VALUES ('second')")
    cursor.execute("INSERT INTO demo (label) VALUES ('third')")

    # Query to see the auto-assigned ids
    cursor.execute("SELECT * FROM demo")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    # (1, 'first')
    # (2, 'second')
    # (3, 'third')
```

### Getting the Last Inserted ID

After an `INSERT`, you can find out what ID was assigned to the new row:

```python
cursor.execute("INSERT INTO animals (name, age, kind) VALUES (?, ?, ?)", ("Leo", 5, "Lion"))
last_id = cursor.lastrowid
print(f"Inserted animal with id: {last_id}")
```

### Natural vs Surrogate Keys

- A **surrogate key** is a system-generated ID like `AUTOINCREMENT` — it has no real-world meaning, just uniqueness.
- A **natural key** is a real-world attribute that is naturally unique, like an email address or a national ID number.

For most tables, surrogate keys (`id INTEGER PRIMARY KEY AUTOINCREMENT`) are the safest and most common choice.

---

### 🏋️ Exercises — Section 4

**Exercise 4.1 — Observe AUTOINCREMENT in action**
Insert three animals into the `animals` table without specifying an `id`, then SELECT all rows and print them to confirm the IDs were assigned automatically.

```python
# Your solution here
import sqlite3

with sqlite3.connect("zoo.db") as connection:
    cursor = connection.cursor()
    cursor.execute("INSERT INTO animals (name, age, kind) VALUES (?, ?, ?)", ("Bubbles", 2, "Goldfish"))
    cursor.execute("INSERT INTO animals (name, age, kind) VALUES (?, ?, ?)", ("Spike", 6, "Hedgehog"))
    cursor.execute("INSERT INTO animals (name, age, kind) VALUES (?, ?, ?)", ("Bella", 4, "Parrot"))

    cursor.execute("SELECT * FROM animals")
    for row in cursor.fetchall():
        print(row)
```

---

**Exercise 4.2 — Capture the last inserted ID**
Insert one animal and use `cursor.lastrowid` to print the ID that was assigned to it.

```python
# Your solution here
import sqlite3

with sqlite3.connect("zoo.db") as connection:
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO animals (name, age, kind) VALUES (?, ?, ?)",
        ("Max", 3, "Penguin")
    )
    print(f"Max was inserted with id: {cursor.lastrowid}")
```

---

**Exercise 4.3 — Try to violate the primary key**
Try to insert a row with a duplicate `id` and observe the error SQLite raises. Wrap the insert in a try/except block and print the error message.

```python
# Your solution here
import sqlite3

with sqlite3.connect("zoo.db") as connection:
    cursor = connection.cursor()
    # First, insert with a specific id
    cursor.execute("INSERT INTO animals (id, name, age, kind) VALUES (?, ?, ?, ?)", (999, "Test", 1, "Cat"))

    try:
        # Try to insert another row with the same id
        cursor.execute("INSERT INTO animals (id, name, age, kind) VALUES (?, ?, ?, ?)", (999, "Duplicate", 1, "Dog"))
    except sqlite3.IntegrityError as e:
        print(f"Error caught: {e}")
    # Error caught: UNIQUE constraint failed: animals.id
```

---

## 5. Inserting Data — Our 20 Animals

Now let's populate the `animals` table with real data. The INSERT statement adds new rows to a table.

### Single Row Insert

```sql
INSERT INTO table_name (column1, column2, ...) VALUES (value1, value2, ...);
```

**Always use parameterized queries** — pass `?` as a placeholder and supply the values separately. This prevents SQL injection and handles special characters automatically.

```python
# Safe — parameterized query
cursor.execute("INSERT INTO animals (name, age, kind) VALUES (?, ?, ?)", ("Leo", 5, "Lion"))

# NEVER do this — vulnerable to SQL injection
name = "Leo"
cursor.execute(f"INSERT INTO animals (name, age, kind) VALUES ('{name}', 5, 'Lion')")  # BAD
```

### Bulk Insert with executemany()

For inserting many rows at once, `executemany()` is far more efficient than calling `execute()` in a loop. It takes a list of tuples and inserts them all in a single operation.

```python
cursor.executemany(
    "INSERT INTO animals (name, age, kind) VALUES (?, ?, ?)",
    list_of_tuples
)
```

### Our 20 Animals Dataset

```python
import sqlite3

# The complete dataset: (name, age, kind)
animals_data = [
    ("Simba",     8,  "Lion"),
    ("Nala",      6,  "Lion"),
    ("Dumbo",     12, "Elephant"),
    ("Ellie",     9,  "Elephant"),
    ("Speedy",    3,  "Cheetah"),
    ("Bubbles",   1,  "Dolphin"),
    ("Splash",    4,  "Dolphin"),
    ("Koko",      15, "Gorilla"),
    ("Zara",      7,  "Zebra"),
    ("Stripes",   5,  "Zebra"),
    ("Frostbite", 2,  "Arctic Fox"),
    ("Giraffy",   10, "Giraffe"),
    ("Tallulah",  8,  "Giraffe"),
    ("Tango",     6,  "Flamingo"),
    ("Rosie",     3,  "Flamingo"),
    ("Bandit",    4,  "Meerkat"),
    ("Ozzy",      11, "Orangutan"),
    ("Pepper",    2,  "Penguin"),
    ("Rocky",     5,  "Snow Leopard"),
    ("Willow",    7,  "Red Panda"),
]

with sqlite3.connect("zoo.db") as connection:
    cursor = connection.cursor()

    # Make sure we start fresh for this guide
    cursor.execute("DELETE FROM animals")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='animals'")

    # Insert all 20 animals in one shot
    cursor.executemany(
        "INSERT INTO animals (name, age, kind) VALUES (?, ?, ?)",
        animals_data
    )

    print(f"Inserted {cursor.rowcount} animals successfully!")

    # Verify
    cursor.execute("SELECT COUNT(*) FROM animals")
    count = cursor.fetchone()[0]
    print(f"Total animals in database: {count}")
```

### Viewing All Inserted Animals

```python
import sqlite3

with sqlite3.connect("zoo.db") as connection:
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM animals ORDER BY id")
    rows = cursor.fetchall()

    print(f"{'ID':<5} {'Name':<12} {'Age':<6} {'Kind':<15}")
    print("-" * 40)
    for row in rows:
        print(f"{row[0]:<5} {row[1]:<12} {row[2]:<6} {row[3]:<15}")
```

**Expected output:**
```
ID    Name         Age    Kind
----------------------------------------
1     Simba        8      Lion
2     Nala         6      Lion
3     Dumbo        12     Elephant
4     Ellie        9      Elephant
5     Speedy       3      Cheetah
6     Bubbles      1      Dolphin
7     Splash       4      Dolphin
8     Koko         15     Gorilla
9     Zara         7      Zebra
10    Stripes      5      Zebra
11    Frostbite    2      Arctic Fox
12    Giraffy      10     Giraffe
13    Tallulah     8      Giraffe
14    Tango        6      Flamingo
15    Rosie        3      Flamingo
16    Bandit       4      Meerkat
17    Ozzy         11     Orangutan
18    Pepper       2      Penguin
19    Rocky        5      Snow Leopard
20    Willow       7      Red Panda
```

---

### 🏋️ Exercises — Section 5

**Exercise 5.1 — Insert a single new animal**
Insert a new animal of your choice using a parameterized `execute()` call and print its assigned ID using `cursor.lastrowid`.

```python
# Your solution here
import sqlite3

with sqlite3.connect("zoo.db") as connection:
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO animals (name, age, kind) VALUES (?, ?, ?)",
        ("Raja", 9, "Bengal Tiger")
    )
    print(f"Inserted Raja the Bengal Tiger with ID: {cursor.lastrowid}")
```

---

**Exercise 5.2 — Insert three animals using executemany()**
Use `executemany()` to insert three animals at once and print the total number of rows in the table afterward.

```python
# Your solution here
import sqlite3

new_animals = [
    ("Luna",  2, "Arctic Wolf"),
    ("Biscuit", 5, "Wombat"),
    ("Cleo",  8, "Komodo Dragon"),
]

with sqlite3.connect("zoo.db") as connection:
    cursor = connection.cursor()
    cursor.executemany(
        "INSERT INTO animals (name, age, kind) VALUES (?, ?, ?)",
        new_animals
    )
    cursor.execute("SELECT COUNT(*) FROM animals")
    total = cursor.fetchone()[0]
    print(f"3 animals added. Total now: {total}")
```

---

**Exercise 5.3 — Print a formatted animal list**
Query all animals and print them in a formatted table showing `id`, `name`, `age`, and `kind`. Use Python's f-string formatting to align the columns neatly.

```python
# Your solution here
import sqlite3

with sqlite3.connect("zoo.db") as connection:
    cursor = connection.cursor()
    cursor.execute("SELECT id, name, age, kind FROM animals ORDER BY kind, name")
    rows = cursor.fetchall()

    print(f"{'ID':<5} {'Name':<12} {'Age':<5} {'Kind':<20}")
    print("=" * 44)
    for row in rows:
        print(f"{row[0]:<5} {row[1]:<12} {row[2]:<5} {row[3]:<20}")
```

---

## 6. Reading Data — SELECT (The R in CRUD)

`SELECT` is the most commonly used SQL command. It retrieves data from the database without modifying anything. This is the **R** in **CRUD** (Create, Read, Update, Delete).

### Basic SELECT Syntax

```sql
SELECT column1, column2 FROM table_name;
SELECT * FROM table_name;              -- * means "all columns"
```

### Fetching Results in Python

After executing a `SELECT`, you retrieve the results with one of three methods:

| Method | Returns | Best when |
|---|---|---|
| `fetchone()` | A single row (or `None`) | You expect exactly one result |
| `fetchmany(n)` | Up to `n` rows | You want batches |
| `fetchall()` | All remaining rows as a list | You want everything |

```python
import sqlite3

with sqlite3.connect("zoo.db") as connection:
    cursor = connection.cursor()

    # --- SELECT all columns ---
    cursor.execute("SELECT * FROM animals")
    all_animals = cursor.fetchall()
    print(f"All animals: {len(all_animals)} rows")

    # --- SELECT specific columns ---
    cursor.execute("SELECT name, kind FROM animals")
    names_and_kinds = cursor.fetchall()
    for row in names_and_kinds[:3]:
        print(row)  # ('Simba', 'Lion')

    # --- fetchone: get a single result ---
    cursor.execute("SELECT * FROM animals WHERE id = 1")
    first = cursor.fetchone()
    print("First animal:", first)
```

### WHERE — Filtering Rows

The `WHERE` clause filters which rows are returned.

```python
import sqlite3

with sqlite3.connect("zoo.db") as connection:
    cursor = connection.cursor()

    # Animals that are lions
    cursor.execute("SELECT * FROM animals WHERE kind = ?", ("Lion",))
    lions = cursor.fetchall()
    print("Lions:", lions)

    # Animals older than 7
    cursor.execute("SELECT name, age FROM animals WHERE age > ?", (7,))
    older = cursor.fetchall()
    print("Older than 7:", older)

    # Animals whose name starts with 'S'
    cursor.execute("SELECT name, kind FROM animals WHERE name LIKE ?", ("S%",))
    s_names = cursor.fetchall()
    print("Names starting with S:", s_names)

    # Animals that are young AND a specific kind
    cursor.execute(
        "SELECT * FROM animals WHERE age < ? AND kind = ?",
        (5, "Zebra")
    )
    young_zebras = cursor.fetchall()
    print("Young zebras:", young_zebras)
```

### ORDER BY — Sorting Results

```python
cursor.execute("SELECT name, age FROM animals ORDER BY age ASC")   # youngest first
cursor.execute("SELECT name, age FROM animals ORDER BY age DESC")  # oldest first
cursor.execute("SELECT * FROM animals ORDER BY kind ASC, age DESC") # sort by multiple columns
```

### LIMIT — Controlling How Many Rows Come Back

```python
cursor.execute("SELECT * FROM animals ORDER BY age DESC LIMIT 5")  # top 5 oldest
cursor.execute("SELECT * FROM animals LIMIT 5 OFFSET 10")          # rows 11–15 (pagination)
```

### Aggregate Functions — Summarizing Data

```python
import sqlite3

with sqlite3.connect("zoo.db") as connection:
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM animals")
    print("Total animals:", cursor.fetchone()[0])

    cursor.execute("SELECT AVG(age) FROM animals")
    print("Average age:", round(cursor.fetchone()[0], 1))

    cursor.execute("SELECT MAX(age) FROM animals")
    print("Oldest age:", cursor.fetchone()[0])

    cursor.execute("SELECT MIN(age) FROM animals")
    print("Youngest age:", cursor.fetchone()[0])

    # GROUP BY: count animals per kind
    cursor.execute("""
        SELECT kind, COUNT(*) AS count
        FROM animals
        GROUP BY kind
        ORDER BY count DESC
    """)
    print("\nAnimals by kind:")
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]}")
```

### Using Row Factories for Cleaner Access

By default, rows come back as plain tuples. Setting `connection.row_factory = sqlite3.Row` lets you access columns by name:

```python
import sqlite3

with sqlite3.connect("zoo.db") as connection:
    connection.row_factory = sqlite3.Row   # Enable named column access
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM animals WHERE kind = ?", ("Flamingo",))
    flamingos = cursor.fetchall()

    for animal in flamingos:
        # Access by column name instead of index
        print(f"{animal['name']} is a {animal['kind']} aged {animal['age']}")
```

---

### 🏋️ Exercises — Section 6

**Exercise 6.1 — Find all animals over age 8**
Write a query that selects the `name`, `age`, and `kind` of every animal older than 8, ordered from oldest to youngest.

```python
# Your solution here
import sqlite3

with sqlite3.connect("zoo.db") as connection:
    cursor = connection.cursor()
    cursor.execute("""
        SELECT name, age, kind
        FROM animals
        WHERE age > ?
        ORDER BY age DESC
    """, (8,))
    rows = cursor.fetchall()
    print("Animals older than 8:")
    for row in rows:
        print(f"  {row[0]}, {row[1]} years old, {row[2]}")
```

---

**Exercise 6.2 — Count animals per kind**
Write a query that groups animals by `kind` and shows the count for each, ordered by count descending. Use the `GROUP BY` clause.

```python
# Your solution here
import sqlite3

with sqlite3.connect("zoo.db") as connection:
    cursor = connection.cursor()
    cursor.execute("""
        SELECT kind, COUNT(*) AS total
        FROM animals
        GROUP BY kind
        ORDER BY total DESC
    """)
    print(f"{'Kind':<20} {'Count':<6}")
    print("-" * 26)
    for row in cursor.fetchall():
        print(f"{row[0]:<20} {row[1]:<6}")
```

---

**Exercise 6.3 — Find the oldest animal per kind**
Write a query that finds the oldest animal in each `kind` group, showing `kind` and `max_age`, ordered alphabetically by kind.

```python
# Your solution here
import sqlite3

with sqlite3.connect("zoo.db") as connection:
    cursor = connection.cursor()
    cursor.execute("""
        SELECT kind, MAX(age) AS max_age, name
        FROM animals
        GROUP BY kind
        ORDER BY kind ASC
    """)
    print(f"{'Kind':<20} {'Oldest':<8} {'Name':<12}")
    print("-" * 40)
    for row in cursor.fetchall():
        print(f"{row[0]:<20} {row[1]:<8} {row[2]:<12}")
```

---

## 7. Updating Data — UPDATE (The U in CRUD)

The `UPDATE` statement modifies existing rows in a table. This is the **U** in **CRUD**.

### Basic UPDATE Syntax

```sql
UPDATE table_name
SET    column1 = value1, column2 = value2
WHERE  condition;
```

> **Critical rule:** Always include a `WHERE` clause. Without it, `UPDATE` will modify **every single row** in the table.

```python
import sqlite3

with sqlite3.connect("zoo.db") as connection:
    cursor = connection.cursor()

    # --- Update one column for a specific animal ---
    cursor.execute(
        "UPDATE animals SET age = ? WHERE id = ?",
        (9, 1)   # Simba just had a birthday!
    )
    print(f"Rows updated: {cursor.rowcount}")

    # Verify
    cursor.execute("SELECT * FROM animals WHERE id = 1")
    print("Updated Simba:", cursor.fetchone())
```

### Updating Multiple Columns at Once

```python
with sqlite3.connect("zoo.db") as connection:
    cursor = connection.cursor()

    # Update both name and age at the same time
    cursor.execute(
        "UPDATE animals SET name = ?, age = ? WHERE id = ?",
        ("Simba Jr.", 9, 1)
    )
    print(f"Updated {cursor.rowcount} row(s)")
```

### Updating Multiple Rows with One Statement

```python
with sqlite3.connect("zoo.db") as connection:
    cursor = connection.cursor()

    # Add 1 year to the age of every dolphin (they all had birthdays today)
    cursor.execute(
        "UPDATE animals SET age = age + 1 WHERE kind = ?",
        ("Dolphin",)
    )
    print(f"Updated {cursor.rowcount} dolphins")

    # Verify
    cursor.execute("SELECT * FROM animals WHERE kind = ?", ("Dolphin",))
    print(cursor.fetchall())
```

### Checking How Many Rows Were Affected

`cursor.rowcount` tells you how many rows the last `UPDATE` (or `DELETE`) affected. This is useful for confirming your query worked as expected.

```python
with sqlite3.connect("zoo.db") as connection:
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE animals SET age = age + 1 WHERE kind = ?",
        ("Dragon",)   # No dragons in our zoo!
    )
    if cursor.rowcount == 0:
        print("No rows updated — no animals matched that condition.")
    else:
        print(f"{cursor.rowcount} row(s) updated.")
```

---

### 🏋️ Exercises — Section 7

**Exercise 7.1 — Give Koko a birthday**
Koko the Gorilla just turned one year older. Update her age by 1 using her `id` (id=8), then SELECT her record to confirm the change.

```python
# Your solution here
import sqlite3

with sqlite3.connect("zoo.db") as connection:
    cursor = connection.cursor()

    cursor.execute("UPDATE animals SET age = age + 1 WHERE id = ?", (8,))
    print(f"Updated {cursor.rowcount} row(s)")

    cursor.execute("SELECT * FROM animals WHERE id = ?", (8,))
    print("Koko after update:", cursor.fetchone())
```

---

**Exercise 7.2 — Rename all Zebras to 'Plains Zebra'**
The zoo's records need to be more specific. Update the `kind` of every Zebra from `"Zebra"` to `"Plains Zebra"`. Print how many rows were updated.

```python
# Your solution here
import sqlite3

with sqlite3.connect("zoo.db") as connection:
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE animals SET kind = ? WHERE kind = ?",
        ("Plains Zebra", "Zebra")
    )
    print(f"Updated {cursor.rowcount} zebra(s) to 'Plains Zebra'")

    cursor.execute("SELECT * FROM animals WHERE kind = 'Plains Zebra'")
    for row in cursor.fetchall():
        print(row)
```

---

**Exercise 7.3 — Correct an age using a WHERE with AND**
The flamingo named "Tango" (id=14) was miscatalogued — her age should be 4, not 6. Also update her name to "Tangerine". Use a single `UPDATE` statement with both changes.

```python
# Your solution here
import sqlite3

with sqlite3.connect("zoo.db") as connection:
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE animals SET name = ?, age = ? WHERE id = ?",
        ("Tangerine", 4, 14)
    )
    print(f"Updated {cursor.rowcount} row(s)")

    cursor.execute("SELECT * FROM animals WHERE id = 14")
    print("Updated flamingo:", cursor.fetchone())
```

---

## 8. Deleting Data — DELETE (The D in CRUD)

The `DELETE` statement removes rows from a table. This is the **D** in **CRUD**.

### Basic DELETE Syntax

```sql
DELETE FROM table_name WHERE condition;
```

> **Critical rule:** Just like `UPDATE`, always use a `WHERE` clause. `DELETE FROM animals` without a `WHERE` will delete every animal in the table instantly.

```python
import sqlite3

with sqlite3.connect("zoo.db") as connection:
    cursor = connection.cursor()

    # Delete a specific animal by id (safest — id is unique)
    cursor.execute("DELETE FROM animals WHERE id = ?", (21,))
    print(f"Deleted {cursor.rowcount} row(s)")
```

### Deleting Multiple Rows

```python
with sqlite3.connect("zoo.db") as connection:
    cursor = connection.cursor()

    # Delete all animals younger than 2
    cursor.execute("DELETE FROM animals WHERE age < ?", (2,))
    print(f"Removed {cursor.rowcount} very young animal(s)")
```

### Safe Delete Pattern — Check First

A good habit is to `SELECT` before you `DELETE` — see what you're about to delete before you delete it.

```python
import sqlite3

with sqlite3.connect("zoo.db") as connection:
    cursor = connection.cursor()

    target_kind = "Arctic Fox"

    # Step 1: preview what will be deleted
    cursor.execute("SELECT * FROM animals WHERE kind = ?", (target_kind,))
    to_delete = cursor.fetchall()
    print(f"About to delete {len(to_delete)} animal(s): {to_delete}")

    # Step 2: confirm and delete
    if to_delete:
        cursor.execute("DELETE FROM animals WHERE kind = ?", (target_kind,))
        print(f"Deleted {cursor.rowcount} Arctic Fox(es).")
```

### DELETE vs TRUNCATE

- `DELETE FROM table_name` removes rows but keeps the table structure. Works row by row and fires triggers. Supports `WHERE`.
- In SQLite, you can clear all rows quickly using `DELETE FROM table_name` without a WHERE (since SQLite doesn't support `TRUNCATE`). To also reset the auto-increment counter:

```python
cursor.execute("DELETE FROM animals")
cursor.execute("DELETE FROM sqlite_sequence WHERE name='animals'")
# Now the next inserted animal will get id=1 again
```

---

### 🏋️ Exercises — Section 8

**Exercise 8.1 — Delete one animal by ID**
Delete the animal with `id=20` (Willow the Red Panda), then SELECT all remaining animals to verify the deletion.

```python
# Your solution here
import sqlite3

with sqlite3.connect("zoo.db") as connection:
    cursor = connection.cursor()

    cursor.execute("DELETE FROM animals WHERE id = ?", (20,))
    print(f"Deleted {cursor.rowcount} animal(s)")

    cursor.execute("SELECT COUNT(*) FROM animals")
    print(f"Remaining animals: {cursor.fetchone()[0]}")
```

---

**Exercise 8.2 — Preview before deleting**
Write a safe delete script that first SELECTs and prints all animals with `age <= 3`, then asks the user to confirm before deleting them (use `input()`).

```python
# Your solution here
import sqlite3

with sqlite3.connect("zoo.db") as connection:
    cursor = connection.cursor()

    cursor.execute("SELECT id, name, age, kind FROM animals WHERE age <= ?", (3,))
    young_ones = cursor.fetchall()

    if not young_ones:
        print("No animals with age <= 3 found.")
    else:
        print(f"These {len(young_ones)} animal(s) will be deleted:")
        for animal in young_ones:
            print(f"  ID={animal[0]} | {animal[1]} | {animal[2]} yrs | {animal[3]}")

        confirm = input("\nType 'yes' to confirm deletion: ")
        if confirm.lower() == "yes":
            cursor.execute("DELETE FROM animals WHERE age <= ?", (3,))
            print(f"Deleted {cursor.rowcount} animal(s).")
        else:
            print("Deletion cancelled.")
```

---

**Exercise 8.3 — Delete all and reset**
Clear the entire `animals` table and reset the auto-increment counter using `DELETE FROM animals` and the `sqlite_sequence` trick. Then re-insert just three animals and confirm their IDs start at 1 again.

```python
# Your solution here
import sqlite3

with sqlite3.connect("zoo.db") as connection:
    cursor = connection.cursor()

    cursor.execute("DELETE FROM animals")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='animals'")
    print("Table cleared and counter reset.")

    fresh_data = [
        ("Alpha", 5, "Wolf"),
        ("Beta",  3, "Bear"),
        ("Gamma", 7, "Eagle"),
    ]
    cursor.executemany("INSERT INTO animals (name, age, kind) VALUES (?, ?, ?)", fresh_data)

    cursor.execute("SELECT * FROM animals")
    for row in cursor.fetchall():
        print(row)
    # IDs should be 1, 2, 3
```

---

## 9. Foreign Keys & Related Tables

A **foreign key** is a column in one table that references the **primary key** of another table. It creates a link between two tables and enforces **referential integrity** — you can't reference a row that doesn't exist.

### Why Foreign Keys?

Suppose each animal in our zoo belongs to a habitat (Savanna, Ocean, Arctic, etc.). Instead of repeating "Savanna" in every lion and zebra row, we store habitat information in a separate `habitats` table and just reference its ID in the `animals` table. This is called **normalization**.

```
Without foreign keys (data duplication):
  animals: id=1, name="Simba",  habitat_name="Savanna", habitat_climate="Hot and Dry"
  animals: id=2, name="Nala",   habitat_name="Savanna", habitat_climate="Hot and Dry"
  animals: id=9, name="Zara",   habitat_name="Savanna", habitat_climate="Hot and Dry"
  ← "Savanna" data is repeated everywhere

With foreign keys (normalized):
  habitats: id=1, name="Savanna",  climate="Hot and Dry"
  animals:  id=1, name="Simba",    habitat_id=1
  animals:  id=2, name="Nala",     habitat_id=1
  animals:  id=9, name="Zara",     habitat_id=1
  ← habitat data lives in one place; animals just reference it
```

### Enabling Foreign Keys in SQLite

**Important:** SQLite does not enforce foreign keys by default. You must turn this on each time you open a connection:

```python
cursor.execute("PRAGMA foreign_keys = ON")
```

### Setting Up Two Related Tables

```python
import sqlite3

with sqlite3.connect("zoo.db") as connection:
    cursor = connection.cursor()

    # Enable foreign key enforcement
    cursor.execute("PRAGMA foreign_keys = ON")

    # Parent table: habitats
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS habitats (
            id      INTEGER  PRIMARY KEY AUTOINCREMENT,
            name    TEXT     NOT NULL UNIQUE,
            climate TEXT     NOT NULL
        )
    """)

    # Insert habitat data
    habitats_data = [
        ("Savanna",      "Hot and Dry"),
        ("Ocean",        "Temperate"),
        ("Arctic",       "Freezing"),
        ("Rainforest",   "Hot and Humid"),
        ("Grassland",    "Mild"),
        ("Mountain",     "Cold"),
        ("Wetlands",     "Humid"),
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO habitats (name, climate) VALUES (?, ?)",
        habitats_data
    )

    # Child table: animals_v2 (with habitat_id foreign key)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS animals_v2 (
            id          INTEGER  PRIMARY KEY AUTOINCREMENT,
            name        TEXT     NOT NULL,
            age         INTEGER  NOT NULL CHECK(age >= 0),
            kind        TEXT     NOT NULL,
            habitat_id  INTEGER  REFERENCES habitats(id) ON DELETE SET NULL
        )
    """)

    # Insert animals with habitat references
    animals_with_habitats = [
        ("Simba",     8,  "Lion",         1),  # Savanna
        ("Nala",      6,  "Lion",         1),  # Savanna
        ("Dumbo",     12, "Elephant",     1),  # Savanna
        ("Ellie",     9,  "Elephant",     1),  # Savanna
        ("Speedy",    3,  "Cheetah",      1),  # Savanna
        ("Bubbles",   1,  "Dolphin",      2),  # Ocean
        ("Splash",    4,  "Dolphin",      2),  # Ocean
        ("Koko",      15, "Gorilla",      4),  # Rainforest
        ("Zara",      7,  "Zebra",        5),  # Grassland
        ("Stripes",   5,  "Zebra",        5),  # Grassland
        ("Frostbite", 2,  "Arctic Fox",   3),  # Arctic
        ("Giraffy",   10, "Giraffe",      1),  # Savanna
        ("Tallulah",  8,  "Giraffe",      1),  # Savanna
        ("Tango",     6,  "Flamingo",     7),  # Wetlands
        ("Rosie",     3,  "Flamingo",     7),  # Wetlands
        ("Bandit",    4,  "Meerkat",      1),  # Savanna
        ("Ozzy",      11, "Orangutan",    4),  # Rainforest
        ("Pepper",    2,  "Penguin",      3),  # Arctic
        ("Rocky",     5,  "Snow Leopard", 6),  # Mountain
        ("Willow",    7,  "Red Panda",    6),  # Mountain
    ]

    cursor.executemany(
        "INSERT INTO animals_v2 (name, age, kind, habitat_id) VALUES (?, ?, ?, ?)",
        animals_with_habitats
    )

    print("Habitats and animals_v2 created and populated!")
```

### Querying with JOIN

A `JOIN` combines rows from two tables based on a matching column — in this case, `animals_v2.habitat_id = habitats.id`.

```python
import sqlite3

with sqlite3.connect("zoo.db") as connection:
    cursor = connection.cursor()

    # INNER JOIN: get animal name + habitat name + climate
    cursor.execute("""
        SELECT a.name, a.kind, h.name AS habitat, h.climate
        FROM   animals_v2 a
        JOIN   habitats h ON a.habitat_id = h.id
        ORDER  BY h.name, a.name
    """)

    print(f"{'Animal':<12} {'Kind':<15} {'Habitat':<14} {'Climate':<20}")
    print("-" * 62)
    for row in cursor.fetchall():
        print(f"{row[0]:<12} {row[1]:<15} {row[2]:<14} {row[3]:<20}")
```

### The ON DELETE Behavior

When a parent row (habitat) is deleted, what happens to the child rows (animals)? You control this with `ON DELETE`:

| Option | Behavior |
|---|---|
| `ON DELETE CASCADE` | Child rows are automatically deleted too |
| `ON DELETE SET NULL` | Child's foreign key column is set to `NULL` |
| `ON DELETE RESTRICT` | Deletion is prevented if children exist (raises an error) |
| `ON DELETE NO ACTION` | Default — similar to RESTRICT in most databases |

```python
# Demonstrating ON DELETE SET NULL
with sqlite3.connect("zoo.db") as connection:
    cursor = connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")

    # Delete the Arctic habitat (id=3)
    cursor.execute("DELETE FROM habitats WHERE id = ?", (3,))

    # Animals that were in the Arctic should now have NULL habitat_id
    cursor.execute("SELECT name, kind, habitat_id FROM animals_v2 WHERE habitat_id IS NULL")
    print("Animals with no habitat (was Arctic):", cursor.fetchall())
```

---

### 🏋️ Exercises — Section 9

**Exercise 9.1 — List animals by habitat**
Write a JOIN query that lists every animal alongside its habitat name, ordered by habitat name and then animal name alphabetically.

```python
# Your solution here
import sqlite3

with sqlite3.connect("zoo.db") as connection:
    cursor = connection.cursor()
    cursor.execute("""
        SELECT h.name AS habitat, a.name AS animal, a.kind
        FROM animals_v2 a
        JOIN habitats h ON a.habitat_id = h.id
        ORDER BY h.name ASC, a.name ASC
    """)
    print(f"{'Habitat':<15} {'Animal':<12} {'Kind':<20}")
    print("-" * 48)
    for row in cursor.fetchall():
        print(f"{row[0]:<15} {row[1]:<12} {row[2]:<20}")
```

---

**Exercise 9.2 — Count animals per habitat**
Write a query that joins `animals_v2` and `habitats`, groups by habitat name, and counts how many animals live in each habitat. Order by count descending.

```python
# Your solution here
import sqlite3

with sqlite3.connect("zoo.db") as connection:
    cursor = connection.cursor()
    cursor.execute("""
        SELECT h.name AS habitat, COUNT(a.id) AS animal_count
        FROM habitats h
        LEFT JOIN animals_v2 a ON a.habitat_id = h.id
        GROUP BY h.name
        ORDER BY animal_count DESC
    """)
    print(f"{'Habitat':<15} {'Animals':<10}")
    print("-" * 25)
    for row in cursor.fetchall():
        print(f"{row[0]:<15} {row[1]:<10}")
```

---

**Exercise 9.3 — Try to violate referential integrity**
Try to insert an animal with a `habitat_id` that doesn't exist (e.g., `habitat_id=99`) and observe the foreign key error. Remember to enable `PRAGMA foreign_keys = ON`.

```python
# Your solution here
import sqlite3

with sqlite3.connect("zoo.db") as connection:
    cursor = connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")

    try:
        cursor.execute(
            "INSERT INTO animals_v2 (name, age, kind, habitat_id) VALUES (?, ?, ?, ?)",
            ("Ghost", 1, "Unicorn", 99)   # habitat_id=99 does not exist
        )
    except sqlite3.IntegrityError as e:
        print(f"Foreign key error caught: {e}")
    # FOREIGN KEY constraint failed
```

---

## 10. Renaming Tables and Columns

Sometimes you need to restructure your database — renaming a table for clarity, or renaming a column to better reflect its purpose. SQLite supports this through the `ALTER TABLE` statement.

### Renaming a Table

```sql
ALTER TABLE old_name RENAME TO new_name;
```

```python
import sqlite3

with sqlite3.connect("zoo.db") as connection:
    cursor = connection.cursor()

    # Rename 'animals' to 'zoo_animals'
    cursor.execute("ALTER TABLE animals RENAME TO zoo_animals")
    print("Table renamed successfully!")

    # Verify: list all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    print("Tables now:", cursor.fetchall())

    # Rename it back for the rest of the guide
    cursor.execute("ALTER TABLE zoo_animals RENAME TO animals")
    print("Table renamed back to 'animals'")
```

### Renaming a Column

Renaming columns in SQLite requires version 3.25.0 or newer (released 2018). Check your version first if you're on an older system.

```sql
ALTER TABLE table_name RENAME COLUMN old_column_name TO new_column_name;
```

```python
import sqlite3

with sqlite3.connect("zoo.db") as connection:
    cursor = connection.cursor()

    # Rename the 'kind' column to 'species'
    cursor.execute("ALTER TABLE animals RENAME COLUMN kind TO species")
    print("Column renamed: 'kind' → 'species'")

    # Verify the new structure
    cursor.execute("PRAGMA table_info(animals)")
    for col in cursor.fetchall():
        print(f"  {col[1]} ({col[2]})")

    # Rename it back
    cursor.execute("ALTER TABLE animals RENAME COLUMN species TO kind")
    print("Column renamed back to 'kind'")
```

### Adding a New Column

You can also add new columns to an existing table without recreating it:

```sql
ALTER TABLE table_name ADD COLUMN column_name DATA_TYPE CONSTRAINTS;
```

```python
import sqlite3

with sqlite3.connect("zoo.db") as connection:
    cursor = connection.cursor()

    # Add a 'is_nocturnal' column with a default value
    cursor.execute("""
        ALTER TABLE animals
        ADD COLUMN is_nocturnal INTEGER DEFAULT 0
    """)
    print("Column 'is_nocturnal' added!")

    # Update some animals to be nocturnal
    nocturnal_ids = [11, 16]  # Frostbite (Arctic Fox), Bandit (Meerkat)
    for animal_id in nocturnal_ids:
        cursor.execute(
            "UPDATE animals SET is_nocturnal = 1 WHERE id = ?",
            (animal_id,)
        )

    cursor.execute("SELECT name, kind, is_nocturnal FROM animals WHERE is_nocturnal = 1")
    print("Nocturnal animals:", cursor.fetchall())
```

> **Note:** SQLite's `ALTER TABLE` is more limited than other databases like PostgreSQL or MySQL. You cannot drop columns, change a column's data type, or add constraints to existing columns using `ALTER TABLE` in older SQLite versions. For complex schema changes, the workaround is: (1) create a new table with the desired schema, (2) copy data over, (3) drop the old table, (4) rename the new table.

---

### 🏋️ Exercises — Section 10

**Exercise 10.1 — Rename a table and query it**
Rename the `habitats` table to `zoo_habitats`, run a SELECT query on it, then rename it back to `habitats`.

```python
# Your solution here
import sqlite3

with sqlite3.connect("zoo.db") as connection:
    cursor = connection.cursor()

    cursor.execute("ALTER TABLE habitats RENAME TO zoo_habitats")
    print("Table renamed to 'zoo_habitats'")

    cursor.execute("SELECT * FROM zoo_habitats")
    for row in cursor.fetchall():
        print(row)

    cursor.execute("ALTER TABLE zoo_habitats RENAME TO habitats")
    print("Table renamed back to 'habitats'")
```

---

**Exercise 10.2 — Rename a column**
Rename the `name` column in the `animals` table to `animal_name`, verify the structure with `PRAGMA table_info`, then rename it back.

```python
# Your solution here
import sqlite3

with sqlite3.connect("zoo.db") as connection:
    cursor = connection.cursor()

    cursor.execute("ALTER TABLE animals RENAME COLUMN name TO animal_name")
    print("Column renamed to 'animal_name'")

    cursor.execute("PRAGMA table_info(animals)")
    print("New structure:")
    for col in cursor.fetchall():
        print(f"  {col[1]} ({col[2]})")

    cursor.execute("ALTER TABLE animals RENAME COLUMN animal_name TO name")
    print("Column renamed back to 'name'")
```

---

**Exercise 10.3 — Add a new column**
Add a `weight_kg` column (type `REAL`, default `NULL`) to the `animals` table. Then update three animals of your choice with realistic weights, and SELECT those three animals to verify.

```python
# Your solution here
import sqlite3

with sqlite3.connect("zoo.db") as connection:
    cursor = connection.cursor()

    cursor.execute("ALTER TABLE animals ADD COLUMN weight_kg REAL DEFAULT NULL")
    print("Column 'weight_kg' added!")

    weights = [
        (190.0, 1),   # Simba the Lion: ~190 kg
        (4200.0, 3),  # Dumbo the Elephant: ~4200 kg
        (0.5, 18),    # Pepper the Penguin: ~0.5 kg
    ]
    cursor.executemany(
        "UPDATE animals SET weight_kg = ? WHERE id = ?",
        weights
    )
    print(f"Updated weights for {cursor.rowcount} animal(s)")

    cursor.execute("SELECT name, kind, weight_kg FROM animals WHERE weight_kg IS NOT NULL")
    print("\nAnimals with weights:")
    for row in cursor.fetchall():
        print(f"  {row[0]} ({row[1]}): {row[2]} kg")
```

---

## 11. Putting It All Together

Let's build a complete mini-application that demonstrates all the concepts from this guide in one cohesive script.

```python
"""
zoo_manager.py
A complete SQLite demo covering:
  - Database & table creation (DDL)
  - Primary keys and foreign keys
  - Full CRUD operations (INSERT, SELECT, UPDATE, DELETE)
  - ALTER TABLE (rename table, rename column, add column)
  - JOIN queries
"""

import sqlite3


def get_connection(db_name="zoo_complete.db"):
    """Create a connection and enable foreign keys."""
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row       # Access columns by name
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def setup_schema(conn):
    """DDL: Create all tables."""
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS habitats (
            id      INTEGER  PRIMARY KEY AUTOINCREMENT,
            name    TEXT     NOT NULL UNIQUE,
            climate TEXT     NOT NULL
        );

        CREATE TABLE IF NOT EXISTS animals (
            id          INTEGER  PRIMARY KEY AUTOINCREMENT,
            name        TEXT     NOT NULL,
            age         INTEGER  NOT NULL CHECK(age >= 0),
            kind        TEXT     NOT NULL,
            weight_kg   REAL     DEFAULT NULL,
            is_nocturnal INTEGER DEFAULT 0,
            habitat_id  INTEGER  REFERENCES habitats(id) ON DELETE SET NULL
        );
    """)
    conn.commit()
    print("✔ Schema created")


def seed_data(conn):
    """DML: Insert all seed data."""
    habitats = [
        ("Savanna",    "Hot and Dry"),
        ("Ocean",      "Temperate"),
        ("Arctic",     "Freezing"),
        ("Rainforest", "Hot and Humid"),
        ("Grassland",  "Mild"),
        ("Mountain",   "Cold"),
        ("Wetlands",   "Humid"),
    ]
    conn.executemany(
        "INSERT OR IGNORE INTO habitats (name, climate) VALUES (?, ?)",
        habitats
    )

    animals = [
        ("Simba",     8,  "Lion",         190.0,  0, 1),
        ("Nala",      6,  "Lion",         130.0,  0, 1),
        ("Dumbo",     12, "Elephant",     4200.0, 0, 1),
        ("Ellie",     9,  "Elephant",     3800.0, 0, 1),
        ("Speedy",    3,  "Cheetah",      55.0,   0, 1),
        ("Bubbles",   1,  "Dolphin",      150.0,  0, 2),
        ("Splash",    4,  "Dolphin",      160.0,  0, 2),
        ("Koko",      15, "Gorilla",      180.0,  0, 4),
        ("Zara",      7,  "Zebra",        350.0,  0, 5),
        ("Stripes",   5,  "Zebra",        320.0,  0, 5),
        ("Frostbite", 2,  "Arctic Fox",   6.0,    1, 3),
        ("Giraffy",   10, "Giraffe",      900.0,  0, 1),
        ("Tallulah",  8,  "Giraffe",      830.0,  0, 1),
        ("Tango",     6,  "Flamingo",     3.5,    0, 7),
        ("Rosie",     3,  "Flamingo",     3.2,    0, 7),
        ("Bandit",    4,  "Meerkat",      0.75,   1, 1),
        ("Ozzy",      11, "Orangutan",    75.0,   0, 4),
        ("Pepper",    2,  "Penguin",      0.5,    0, 3),
        ("Rocky",     5,  "Snow Leopard", 50.0,   1, 6),
        ("Willow",    7,  "Red Panda",    6.2,    1, 6),
    ]
    conn.executemany(
        """INSERT INTO animals (name, age, kind, weight_kg, is_nocturnal, habitat_id)
           VALUES (?, ?, ?, ?, ?, ?)""",
        animals
    )
    conn.commit()
    print(f"✔ Seeded {len(habitats)} habitats and {len(animals)} animals")


def read_all_animals(conn):
    """DQL: SELECT with JOIN."""
    cursor = conn.execute("""
        SELECT a.id, a.name, a.age, a.kind, a.weight_kg,
               CASE WHEN a.is_nocturnal = 1 THEN 'Yes' ELSE 'No' END AS nocturnal,
               COALESCE(h.name, 'Unknown') AS habitat
        FROM   animals a
        LEFT JOIN habitats h ON a.habitat_id = h.id
        ORDER  BY a.id
    """)
    rows = cursor.fetchall()
    print(f"\n{'ID':<4} {'Name':<12} {'Age':<4} {'Kind':<15} {'Kg':<8} {'Nocturnal':<10} {'Habitat':<12}")
    print("─" * 68)
    for r in rows:
        kg = f"{r['weight_kg']:.1f}" if r['weight_kg'] else "—"
        print(f"{r['id']:<4} {r['name']:<12} {r['age']:<4} {r['kind']:<15} {kg:<8} {r['nocturnal']:<10} {r['habitat']:<12}")


def birthday_update(conn, animal_id):
    """DML: UPDATE one animal's age."""
    conn.execute("UPDATE animals SET age = age + 1 WHERE id = ?", (animal_id,))
    conn.commit()
    row = conn.execute("SELECT name, age FROM animals WHERE id = ?", (animal_id,)).fetchone()
    print(f"\n✔ Happy birthday {row['name']}! Now {row['age']} years old.")


def habitat_summary(conn):
    """DQL: GROUP BY aggregate."""
    cursor = conn.execute("""
        SELECT h.name, h.climate, COUNT(a.id) AS residents
        FROM   habitats h
        LEFT JOIN animals a ON a.habitat_id = h.id
        GROUP  BY h.id
        ORDER  BY residents DESC
    """)
    print(f"\n{'Habitat':<14} {'Climate':<16} {'Residents':<10}")
    print("─" * 42)
    for r in cursor.fetchall():
        print(f"{r['name']:<14} {r['climate']:<16} {r[2]:<10}")


def rename_and_restore(conn):
    """DDL: ALTER TABLE rename demo."""
    conn.execute("ALTER TABLE animals RENAME COLUMN kind TO species")
    conn.commit()
    print("\n✔ Column 'kind' renamed to 'species'")

    row = conn.execute("SELECT name, species FROM animals WHERE id = 1").fetchone()
    print(f"  Simba's species: {row['species']}")

    conn.execute("ALTER TABLE animals RENAME COLUMN species TO kind")
    conn.commit()
    print("✔ Column renamed back to 'kind'")


def delete_demo(conn):
    """DML: DELETE with preview."""
    cursor = conn.execute("SELECT id, name, kind FROM animals WHERE age < ?", (3,))
    young = cursor.fetchall()
    if young:
        print(f"\nDeleting {len(young)} animal(s) under age 3:")
        for a in young:
            print(f"  ID={a['id']} {a['name']} ({a['kind']})")
        conn.execute("DELETE FROM animals WHERE age < ?", (3,))
        conn.commit()
    else:
        print("\nNo animals under age 3 to delete.")


def main():
    print("=" * 68)
    print("  ZOO DATABASE MANAGER — Full SQLite Demo")
    print("=" * 68)

    conn = get_connection()

    setup_schema(conn)
    seed_data(conn)
    read_all_animals(conn)
    birthday_update(conn, animal_id=8)   # Koko's birthday
    habitat_summary(conn)
    rename_and_restore(conn)
    delete_demo(conn)

    print("\n✔ All operations complete!")
    conn.close()


if __name__ == "__main__":
    main()
```

---

### Quick Reference Card

```
SQL SUBLANGUAGES USED IN THIS GUIDE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DDL (Data Definition Language) — Structure
  CREATE TABLE IF NOT EXISTS ...         Create a new table
  ALTER TABLE t RENAME TO new_name       Rename a table
  ALTER TABLE t RENAME COLUMN c TO new   Rename a column
  ALTER TABLE t ADD COLUMN c TYPE        Add a column

DML (Data Manipulation Language) — Write
  INSERT INTO t (cols) VALUES (?, ?)     Insert one row
  executemany(sql, list_of_tuples)       Insert many rows
  UPDATE t SET col = ? WHERE ...         Modify rows
  DELETE FROM t WHERE ...                Remove rows

DQL (Data Query Language) — Read
  SELECT * FROM t                        All rows/columns
  SELECT col FROM t WHERE cond           Filtered rows
  SELECT col FROM t ORDER BY col DESC    Sorted results
  SELECT col FROM t LIMIT n OFFSET m    Paginated results
  SELECT COUNT(*), AVG(col), MAX(col)    Aggregates
  SELECT ... FROM a JOIN b ON a.x = b.y  Combined tables
  SELECT col, COUNT(*) GROUP BY col      Grouped results

KEY CONCEPTS
  PRIMARY KEY       Unique row identifier (AUTOINCREMENT)
  FOREIGN KEY       References another table's primary key
  PRAGMA foreign_keys = ON    Enable FK enforcement in SQLite
  ON DELETE SET NULL / CASCADE / RESTRICT

PYTHON PATTERNS
  cursor.execute(sql, (val,))            Parameterized query (SAFE)
  cursor.executemany(sql, list)          Bulk insert
  cursor.fetchone()                      One row
  cursor.fetchall()                      All rows
  cursor.rowcount                        Rows affected by last write
  cursor.lastrowid                       ID of last inserted row
  conn.row_factory = sqlite3.Row         Access columns by name
  conn.commit()                          Save changes (TCL: COMMIT)
  conn.rollback()                        Undo changes (TCL: ROLLBACK)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

*Next steps: explore SQL indexes (`CREATE INDEX`) to speed up queries, learn about SQL transactions for safe multi-step operations, and practice writing subqueries and CTEs (Common Table Expressions) for more complex data analysis.*
