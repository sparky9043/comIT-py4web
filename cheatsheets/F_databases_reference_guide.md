# 🗄️ Databases: A Comprehensive Reference Guide
### SQL, NoSQL, Graph Databases, Python Integration, ORMs, Schema Design, and Transactions

---

## Table of Contents

1. [What is a Database?](#1-what-is-a-database)
2. [SQL vs NoSQL vs Graph](#2-sql-vs-nosql-vs-graph)
3. [Database Specifications & Python Connections](#3-database-specifications--python-connections)
   - SQLite
   - MySQL
   - PostgreSQL
   - Redis
   - MongoDB
   - Firestore
   - Neo4j (Graph)
4. [Python Packages for Database Connectivity](#4-python-packages-for-database-connectivity)
5. [SQL Language Sublanguages](#5-sql-language-sublanguages)
   - Schema
   - DDL — Data Definition Language
   - DML — Data Manipulation Language
   - DQL — Data Query Language
   - DCL — Data Control Language
   - TCL — Transaction Control Language
   - Sublanguage Comparison Table
6. [ACID Transactions](#6-acid-transactions)
7. [UML and Database Diagrams](#7-uml-and-database-diagrams)
8. [ORM — Object Relational Mapping](#8-orm--object-relational-mapping)
9. [Django ORM in Practice](#9-django-orm-in-practice)

---

## 1. What is a Database?

A **database** is an organized collection of structured information or data, stored electronically and managed by a **Database Management System (DBMS)**. Databases allow applications to persistently store, retrieve, update, and delete data efficiently.

**Main applications of databases:**
- Web applications (user accounts, content, sessions)
- E-commerce platforms (products, orders, inventory)
- Banking and finance (transactions, accounts)
- Healthcare (patient records, prescriptions)
- Analytics and reporting (data warehouses, dashboards)
- Caching and real-time messaging
- Social networks and recommendation engines (graph relationships)

---

## 2. SQL vs NoSQL vs Graph

### SQL (Relational Databases)

**SQL (Structured Query Language)** databases store data in **tables** with rows and columns, much like a spreadsheet. Relationships between tables are defined using **foreign keys**, and the database enforces a fixed **schema** — meaning the structure of the data must be defined before data is inserted.

**Key characteristics:**
- Structured, tabular data
- Fixed schema (must define columns and types upfront)
- Supports complex queries with JOINs
- Full ACID transactions (Atomicity, Consistency, Isolation, Durability)
- Vertically scalable (more powerful hardware)

**Main applications:**
- Financial systems (where data integrity is critical)
- ERP and CRM software
- Applications with complex relationships between data
- Reporting and analytics with structured data

**Examples:** SQLite, MySQL, PostgreSQL, Microsoft SQL Server, Oracle

---

### NoSQL (Non-Relational Databases)

**NoSQL databases** store data in formats other than relational tables — such as documents, key-value pairs, graphs, or wide columns. They are designed for flexibility, scale, and speed, and typically do **not** require a fixed schema.

**Key characteristics:**
- Flexible or schema-less data models
- Designed for horizontal scaling (many servers)
- Optimized for specific data access patterns
- Eventual consistency (in many implementations)
- Better suited for unstructured or semi-structured data

**Main applications:**
- Real-time applications (chat, gaming, live feeds)
- Big data and high-throughput workloads
- Content management with variable structure
- Caching and session storage
- Mobile and IoT applications

**Examples:** MongoDB (document), Redis (key-value), Firestore (document), Cassandra (wide-column), Neo4j (graph)

---

### Graph Databases

**Graph databases** are a specialized category of NoSQL database that store data as a network of **nodes** (entities) and **edges** (relationships). Unlike relational databases that model relationships via foreign keys and JOINs, graph databases make relationships first-class citizens of the data model — they are stored directly alongside the data, making traversal of deep, complex relationship chains extremely fast regardless of dataset size.

**Core concepts:**
- **Node** — an entity (e.g., a Person, a Movie, a Product)
- **Edge** (also called a **relationship**) — a named, directional connection between two nodes (e.g., `FOLLOWS`, `PURCHASED`, `KNOWS`)
- **Property** — key-value pairs attached to both nodes and edges (e.g., `name: "Alice"`, `since: 2021`)
- **Label** — a category tag assigned to a node (e.g., `:User`, `:Post`, `:Product`)

**Key characteristics:**
- Relationships are stored explicitly — no need for costly JOIN operations
- Optimized for traversal queries: "find all friends of friends," "shortest path between X and Y"
- Highly performant for deeply connected data (performance does not degrade as the graph grows)
- Schema-optional (most graph DBs allow flexible properties)
- Query languages like **Cypher** (Neo4j) or **Gremlin** (Apache TinkerPop)

**Main applications:**
- Social networks (friend recommendations, connection graphs)
- Fraud detection (identifying unusual patterns of connections between accounts)
- Knowledge graphs (Wikipedia, Google's Knowledge Panel)
- Recommendation engines (Amazon, Netflix — "people who bought X also bought Y")
- Network and IT operations management
- Supply chain and logistics mapping
- Identity and access management (role hierarchies, permission propagation)

**Examples:** Neo4j, Amazon Neptune, ArangoDB, OrientDB, TigerGraph

---

### GraphQL — An Important Distinction

**GraphQL is NOT a graph database.** It is a query language and runtime for APIs, developed by Facebook. GraphQL allows API clients to request exactly the data they need — no more, no less — from any backend data source (which could be a SQL database, a REST API, a graph database, or anything else).

| | GraphQL | Graph Database (e.g., Neo4j) |
|---|---|---|
| **What is it?** | An API query language | A database engine |
| **What does it query?** | Any data source via resolvers | A graph-structured dataset |
| **Where does it live?** | At the API layer | At the storage layer |
| **Data model** | Defines types and fields | Nodes, edges, properties |
| **Use case** | Flexible API for frontend clients | Highly connected data queries |

In practice, GraphQL and a graph database can be used together — you can build a GraphQL API whose resolvers query Neo4j — but they solve different problems at different layers of the stack.

---

### Database Type Comparison

| Feature | SQL | Document NoSQL | Key-Value NoSQL | Graph DB |
|---|---|---|---|---|
| Data model | Tables (rows/columns) | JSON documents | Key → Value | Nodes + Edges |
| Schema | Fixed | Flexible | None | Optional |
| Relationships | Foreign keys + JOINs | Embedding / references | None | Native, first-class |
| Transactions | Full ACID | Varies | Limited | Full ACID (Neo4j) |
| Best for | Structured, relational data | Semi-structured, evolving data | Caching, sessions | Highly connected data |
| Query language | SQL | MQL, etc. | API commands | Cypher, Gremlin |
| Examples | PostgreSQL, MySQL | MongoDB, Firestore | Redis | Neo4j, Amazon Neptune |

---

## 3. Database Specifications & Python Connections

---

### SQLite

**Type:** SQL (Relational)

**Overview:** SQLite is a lightweight, file-based relational database. Unlike most databases, it runs **in-process** with your application — there is no separate server. The entire database is stored in a single `.db` file on disk.

**Key specifications:**
- File-based (no server required)
- Maximum database size: ~140 TB (practical limit usually much lower)
- Supports most SQL features (JOINs, transactions, triggers, views)
- Single writer at a time (WAL mode improves concurrency)
- Zero configuration — works out of the box
- Built into Python's standard library
- Full ACID compliance

**Main applications:**
- Development and testing environments
- Desktop and mobile applications
- Embedded databases in software tools
- Small to medium-sized applications with low concurrency needs
- Django's default database for new projects

**Python package:** `sqlite3` (built-in — no installation needed)

```python
import sqlite3

# Connect to a database file (creates it if it doesn't exist)
connection = sqlite3.connect("myapp.db")
cursor = connection.cursor()

# DDL: Create a table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

# DML: Insert a record
cursor.execute(
    "INSERT INTO users (username, email) VALUES (?, ?)",
    ("alice", "alice@example.com")
)
connection.commit()  # TCL: COMMIT

# DQL: Query records
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
for row in rows:
    print(row)

connection.close()
```

> **Tip:** Always use parameterized queries (`?` placeholders) rather than string formatting to prevent SQL injection attacks.

---

### MySQL

**Type:** SQL (Relational)

**Overview:** MySQL is one of the most widely used open-source relational databases in the world. It powers many of the web's largest platforms and is known for its speed, reliability, and ease of use.

**Key specifications:**
- Client-server architecture (requires a running server)
- Default port: `3306`
- Storage engines: InnoDB (default, full ACID), MyISAM (no transactions), and others
- Maximum table size: 64 TB (with InnoDB)
- Supports replication, clustering, and partitioning
- Strong community and extensive hosting support
- Used by Facebook, Twitter, YouTube, and WordPress

**Main applications:**
- Web applications (especially LAMP stack: Linux, Apache, MySQL, PHP/Python)
- Content management systems
- E-commerce platforms
- SaaS applications

**Python package:** `mysql-connector-python` or `PyMySQL`

```bash
pip install mysql-connector-python
```

```python
import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="yourpassword",
    database="myapp_db"
)

cursor = connection.cursor()

# DDL: Create a table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        price DECIMAL(10, 2) NOT NULL,
        stock INT DEFAULT 0
    )
""")

# DML: Insert a record
sql = "INSERT INTO products (name, price, stock) VALUES (%s, %s, %s)"
cursor.execute(sql, ("Laptop", 999.99, 50))
connection.commit()  # TCL: COMMIT

# DQL: Query records
cursor.execute("SELECT * FROM products WHERE price < %s", (1500,))
for row in cursor.fetchall():
    print(row)

cursor.close()
connection.close()
```

---

### PostgreSQL

**Type:** SQL (Relational)

**Overview:** PostgreSQL (often called "Postgres") is a powerful, open-source object-relational database renowned for its standards compliance, extensibility, and advanced features. It is widely considered the most feature-complete open-source SQL database.

**Key specifications:**
- Client-server architecture
- Default port: `5432`
- Full ACID compliance with configurable transaction isolation levels
- Supports advanced data types: JSON/JSONB, arrays, hstore, geometric types, UUID, and custom types
- Full-text search built-in
- Advanced indexing (B-tree, Hash, GIN, GiST, BRIN)
- Supports stored procedures in multiple languages (PL/pgSQL, Python, JavaScript)
- Maximum table size: 32 TB
- Table partitioning, materialized views, and window functions
- Row-level security (RLS) for fine-grained DCL access control
- Highly extensible via extensions (e.g., PostGIS for geospatial data)

**Main applications:**
- Complex, data-intensive applications
- Applications requiring advanced querying (analytics, reporting)
- Geospatial applications (with PostGIS)
- Applications needing JSON storage alongside relational data
- Financial and scientific systems requiring strong integrity

**Python package:** `psycopg2` (most common) or `psycopg3`

```bash
pip install psycopg2-binary
```

```python
import psycopg2
from psycopg2.extras import RealDictCursor

connection = psycopg2.connect(
    host="localhost", port=5432,
    dbname="myapp_db", user="postgres", password="yourpassword"
)

cursor = connection.cursor(cursor_factory=RealDictCursor)

# DDL: Create a table with PostgreSQL-specific types
cursor.execute("""
    CREATE TABLE IF NOT EXISTS articles (
        id SERIAL PRIMARY KEY,
        title VARCHAR(500) NOT NULL,
        content TEXT,
        tags TEXT[],
        metadata JSONB,
        created_at TIMESTAMPTZ DEFAULT NOW()
    )
""")

# DML: Insert with advanced types
cursor.execute("""
    INSERT INTO articles (title, content, tags, metadata)
    VALUES (%s, %s, %s, %s)
""", (
    "Intro to PostgreSQL",
    "PostgreSQL is a powerful database...",
    ["database", "sql", "postgres"],
    '{"author": "Alice", "views": 0}'
))
connection.commit()  # TCL: COMMIT

# DQL: Query with JSON filtering
cursor.execute("""
    SELECT title, tags FROM articles
    WHERE metadata->>'author' = %s
""", ("Alice",))

for row in cursor.fetchall():
    print(row)  # Returns as dict

cursor.close()
connection.close()
```

---

### Redis

**Type:** NoSQL (Key-Value / In-Memory)

**Overview:** Redis (Remote Dictionary Server) is an ultra-fast, in-memory data structure store. Because data lives primarily in RAM, read and write operations are extremely fast — often completing in under a millisecond.

**Key specifications:**
- In-memory storage (optionally persisted to disk via RDB snapshots or AOF logs)
- Default port: `6379`
- Supports rich data structures: strings, hashes, lists, sets, sorted sets, bitmaps, HyperLogLogs, streams, and geospatial indexes
- Sub-millisecond latency
- Pub/Sub messaging support
- Atomic transactions with MULTI/EXEC (commands execute atomically, but no rollback on logic errors)
- Built-in data expiration (TTL on keys)
- Lua scripting support
- Clustering and replication support

**Main applications:**
- Caching (cache database query results, API responses)
- Session storage for web applications
- Rate limiting
- Real-time leaderboards and counters
- Message queues and Pub/Sub
- Job queues (with libraries like Celery + Redis)

**Python package:** `redis`

```bash
pip install redis
```

```python
import redis
import json

client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

# String key-value
client.set("username:1001", "alice", ex=3600)  # Expires in 1 hour
print(client.get("username:1001"))  # "alice"

# Hash — store object fields
client.hset("user:1001", mapping={"name": "Alice", "email": "alice@example.com", "role": "admin"})
print(client.hgetall("user:1001"))

# Sorted Set — leaderboard
client.zadd("leaderboard", {"alice": 9500, "bob": 8700, "carol": 10200})
print(client.zrevrange("leaderboard", 0, 2, withscores=True))

# Atomic pipeline (MULTI/EXEC) — Redis's form of a transaction
pipe = client.pipeline()
pipe.multi()
pipe.decrby("account:alice:balance", 100)
pipe.incrby("account:bob:balance", 100)
pipe.execute()  # Both execute atomically or neither does

# Caching pattern
cache_key = "article:42"
cached = client.get(cache_key)
if cached:
    article = json.loads(cached)
else:
    article = {"id": 42, "title": "Redis Guide", "views": 1500}
    client.set(cache_key, json.dumps(article), ex=600)
```

---

### MongoDB

**Type:** NoSQL (Document)

**Overview:** MongoDB is a document-oriented database that stores data in **BSON** (Binary JSON) format. Instead of rows in tables, MongoDB stores **documents** in **collections**.

**Key specifications:**
- Default port: `27017`
- Documents stored in BSON (Binary JSON)
- Schema-less (each document in a collection can have different fields)
- Supports embedded documents and arrays
- Powerful aggregation pipeline
- Horizontal scaling via sharding
- Replica sets for high availability
- Full ACID multi-document transactions (since v4.0)
- Maximum document size: 16 MB

**Main applications:**
- Content management systems and blogs
- Product catalogs with variable attributes
- User profiles and activity feeds
- Real-time analytics
- Mobile application backends

**Python package:** `pymongo`

```bash
pip install pymongo
```

```python
from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client["myapp_db"]
collection = db["users"]

# Insert a document
result = collection.insert_one({
    "username": "alice", "email": "alice@example.com", "age": 30,
    "address": {"city": "Toronto", "country": "Canada"},
    "created_at": datetime.utcnow()
})

# Find documents
young_users = collection.find({"age": {"$lt": 31}})
for u in young_users:
    print(u["username"])

# Update
collection.update_one({"username": "alice"}, {"$set": {"age": 31}})

# ACID multi-document transaction (requires replica set)
with client.start_session() as session:
    with session.start_transaction():
        db.accounts.update_one(
            {"username": "alice"}, {"$inc": {"balance": -100}}, session=session
        )
        db.accounts.update_one(
            {"username": "bob"}, {"$inc": {"balance": 100}}, session=session
        )
        # Automatically rolled back if any operation raises an exception

client.close()
```

---

### Firestore

**Type:** NoSQL (Document) — Cloud-native (Google Firebase / Google Cloud)

**Overview:** Cloud Firestore is a fully managed, serverless, NoSQL document database from Google, designed for mobile and web application development with real-time synchronization.

**Key specifications:**
- Fully managed cloud service (no server to maintain)
- Documents organized in **collections** (and sub-collections)
- Real-time listeners — clients receive data updates automatically
- Offline support for mobile and web clients
- Automatic scaling (no capacity planning required)
- Maximum document size: 1 MB
- Atomic transactions across multiple documents
- Integrated with Firebase Authentication and Cloud Functions

**Main applications:**
- Mobile apps (iOS, Android) with real-time sync
- Collaborative tools (documents, chats, shared state)
- User-generated content platforms
- Applications requiring offline-first functionality

**Python package:** `firebase-admin`

```bash
pip install firebase-admin
```

```python
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

cred = credentials.Certificate("path/to/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Add a document
db.collection("users").document("user_1001").set({
    "username": "alice", "email": "alice@example.com", "credits": 100
})

# Atomic transaction — read-then-write
@firestore.transactional
def transfer_credits(transaction, sender_ref, receiver_ref, amount):
    sender = sender_ref.get(transaction=transaction).to_dict()
    if sender["credits"] < amount:
        raise ValueError("Insufficient credits")
    transaction.update(sender_ref, {"credits": sender["credits"] - amount})
    transaction.update(receiver_ref, {"credits": firestore.Increment(amount)})

transaction = db.transaction()
transfer_credits(
    transaction,
    db.collection("users").document("alice"),
    db.collection("users").document("bob"),
    50
)

# Batch write (atomic group of writes, no reads)
batch = db.batch()
batch.set(db.collection("logs").document(), {"action": "transfer", "ts": datetime.utcnow()})
batch.update(db.collection("users").document("alice"), {"last_active": datetime.utcnow()})
batch.commit()
```

---

### Neo4j (Graph Database)

**Type:** Graph Database (NoSQL)

**Overview:** Neo4j is the world's most widely used graph database. It stores data as a network of nodes and relationships, making it incredibly powerful for use cases that involve traversing connections. Neo4j uses a query language called **Cypher**, which reads almost like English and is designed specifically for expressing graph patterns.

**Key specifications:**
- Native graph storage (relationships stored as direct pointers, not computed at query time)
- Default port: `7687` (Bolt protocol), `7474` (HTTP browser UI)
- Query language: **Cypher** (declarative, pattern-based)
- Full ACID transactions
- Supports properties on both nodes and relationships
- Index-free adjacency — traversal speed is independent of total dataset size
- Available as self-hosted or cloud-managed (Neo4j Aura)
- Supports GQL (ISO standard graph query language)

**Main applications:**
- Social networks (friend-of-a-friend, mutual connections)
- Fraud detection (unusual transaction chains between accounts)
- Knowledge graphs
- Real-time recommendation engines
- Network topology and dependency mapping
- Access control and permission hierarchies

**Python package:** `neo4j`

```bash
pip install neo4j
```

```python
from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "yourpassword"))

# Create nodes and relationships
def create_social_graph(tx):
    tx.run("""
        MERGE (alice:Person {name: 'Alice', age: 30})
        MERGE (bob:Person {name: 'Bob', age: 25})
        MERGE (carol:Person {name: 'Carol', age: 35})
        MERGE (django:Technology {name: 'Django', type: 'framework'})
        MERGE (python:Technology {name: 'Python', type: 'language'})

        MERGE (alice)-[:KNOWS {since: 2020}]->(bob)
        MERGE (alice)-[:KNOWS {since: 2019}]->(carol)
        MERGE (bob)-[:KNOWS {since: 2021}]->(carol)
        MERGE (alice)-[:USES]->(django)
        MERGE (alice)-[:USES]->(python)
        MERGE (bob)-[:USES]->(python)
    """)

# Query: friend-of-a-friend recommendations (2 hops)
def friends_of_friends(tx, person_name):
    result = tx.run("""
        MATCH (p:Person {name: $name})-[:KNOWS]->(friend)-[:KNOWS]->(fof)
        WHERE fof <> p AND NOT (p)-[:KNOWS]->(fof)
        RETURN DISTINCT fof.name AS suggestion
    """, name=person_name)
    return [record["suggestion"] for record in result]

# Query: shortest path between two people
def shortest_path(tx, from_name, to_name):
    result = tx.run("""
        MATCH path = shortestPath(
            (a:Person {name: $from_name})-[:KNOWS*]-(b:Person {name: $to_name})
        )
        RETURN [node IN nodes(path) | node.name] AS path_names, length(path) AS hops
    """, from_name=from_name, to_name=to_name)
    return result.single()

with driver.session() as session:
    session.execute_write(create_social_graph)
    print("Friend suggestions for Alice:", session.execute_read(friends_of_friends, "Alice"))
    print("Path:", session.execute_read(shortest_path, "Alice", "Carol"))

driver.close()
```

**Cypher Quick Reference:**

```cypher
-- Create a node
CREATE (p:Person {name: 'Alice', age: 30})

-- Create a relationship
MATCH (a:Person {name: 'Alice'}), (b:Person {name: 'Bob'})
CREATE (a)-[:FOLLOWS {since: 2022}]->(b)

-- Find all persons
MATCH (p:Person) RETURN p

-- Pattern matching: who does Alice follow?
MATCH (alice:Person {name: 'Alice'})-[:FOLLOWS]->(followed)
RETURN followed.name

-- Filter with WHERE
MATCH (p:Person) WHERE p.age > 25 RETURN p.name, p.age

-- Delete a node (must detach relationships first)
MATCH (p:Person {name: 'Alice'}) DETACH DELETE p
```

---

## 4. Python Packages for Database Connectivity

| Database | Package(s) | Install Command |
|---|---|---|
| SQLite | `sqlite3` | Built into Python (no install needed) |
| MySQL | `mysql-connector-python`, `PyMySQL` | `pip install mysql-connector-python` |
| PostgreSQL | `psycopg2`, `psycopg3` | `pip install psycopg2-binary` |
| Redis | `redis` | `pip install redis` |
| MongoDB | `pymongo` | `pip install pymongo` |
| Firestore | `firebase-admin` | `pip install firebase-admin` |
| Neo4j | `neo4j` | `pip install neo4j` |
| Any SQL DB (abstraction) | `SQLAlchemy` | `pip install sqlalchemy` |
| Django ORM | Built into Django | `pip install django` |

### Using Environment Variables for Connection Strings

Never hardcode credentials. Use environment variables or a `.env` file:

```bash
pip install python-dotenv
```

```python
# .env file
# DATABASE_URL=postgresql://user:password@localhost:5432/mydb
# NEO4J_URI=bolt://localhost:7687
# NEO4J_PASSWORD=yourpassword

import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()
connection = psycopg2.connect(os.environ["DATABASE_URL"])
```

---

## 5. SQL Language Sublanguages

SQL is not a single monolithic language — it is organized into several distinct **sublanguages**, each with a specific purpose. Understanding these sublanguages helps you reason clearly about what category of operation you're performing at any given time.

```
SQL Sublanguages
├── DDL  — Data Definition Language     (structure:    CREATE, ALTER, DROP)
├── DML  — Data Manipulation Language   (content:      INSERT, UPDATE, DELETE)
├── DQL  — Data Query Language          (reading:      SELECT)
├── DCL  — Data Control Language        (access:       GRANT, REVOKE)
└── TCL  — Transaction Control Language (integrity:    COMMIT, ROLLBACK, SAVEPOINT)
```

---

### What is a Schema?

A **schema** is the **blueprint** of a database. It defines the structure of the data — what tables exist, what columns those tables have, the data types of each column, constraints (like NOT NULL or UNIQUE), and the relationships between tables (via foreign keys).

Think of a schema as the **architecture plan** of a building — it doesn't contain the data itself (the furniture), but it defines all the rooms (tables), their dimensions (column types), and the rules (constraints).

**Example schema concept:**

```
Table: users
  - id          INTEGER  PRIMARY KEY
  - username    TEXT     NOT NULL UNIQUE
  - email       TEXT     NOT NULL
  - created_at  TIMESTAMP

Table: posts
  - id          INTEGER  PRIMARY KEY
  - user_id     INTEGER  FOREIGN KEY → users(id)
  - title       TEXT     NOT NULL
  - body        TEXT
  - published   BOOLEAN  DEFAULT FALSE
```

In NoSQL databases, the concept of a schema is more flexible — documents in a collection don't need to share the same structure. However, many NoSQL systems (including MongoDB with Mongoose and Firestore with security rules) encourage defining a **logical schema** even if the database doesn't enforce it at the storage level.

---

### DDL — Data Definition Language

**DDL** is the subset of SQL used to **define and modify the structure** of a database. DDL statements describe the schema — they create, alter, or remove database objects such as tables, indexes, views, and schemas.

DDL changes the **shape** of the database, not the data inside it.

**Main DDL commands:**

| Command | Purpose |
|---|---|
| `CREATE` | Create a new table, index, view, or database |
| `ALTER` | Modify an existing table (add/remove/rename columns) |
| `DROP` | Permanently delete a table or database |
| `TRUNCATE` | Remove all rows from a table (but keep the structure) |
| `RENAME` | Rename a table or column |

**DDL Examples:**

```sql
-- CREATE: Define a new table
CREATE TABLE customers (
    id          SERIAL PRIMARY KEY,
    full_name   VARCHAR(255) NOT NULL,
    email       VARCHAR(255) NOT NULL UNIQUE,
    is_active   BOOLEAN DEFAULT TRUE,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- ALTER: Add a new column
ALTER TABLE customers ADD COLUMN phone VARCHAR(20);

-- ALTER: Rename a column
ALTER TABLE customers RENAME COLUMN full_name TO name;

-- ALTER: Change a column's data type
ALTER TABLE customers ALTER COLUMN phone TYPE TEXT;

-- DROP: Permanently remove a table (and all its data!)
DROP TABLE customers;

-- TRUNCATE: Remove all rows but keep the structure
TRUNCATE TABLE customers;

-- CREATE INDEX: Speed up queries on a column
CREATE INDEX idx_customers_email ON customers(email);

-- CREATE VIEW: A saved query treated like a virtual table
CREATE VIEW active_customers AS
    SELECT id, name, email FROM customers WHERE is_active = TRUE;
```

> **Important:** Most DDL commands auto-commit and cannot be rolled back in most databases. Always back up data before running DDL in production.

---

### DML — Data Manipulation Language

**DML** is the subset of SQL used to **manipulate the data** stored in the database. DML statements insert, update, or delete the rows inside tables.

DML changes the **content** of the database, not the structure. DML operations are **transactional** — they can be wrapped in a transaction and rolled back if something goes wrong.

**Main DML commands:**

| Command | Purpose |
|---|---|
| `INSERT` | Add new rows to a table |
| `UPDATE` | Modify existing rows in a table |
| `DELETE` | Remove specific rows from a table |
| `MERGE` | Upsert — insert if not exists, update if it does |

**DML Examples:**

```sql
-- INSERT: Add a new row
INSERT INTO customers (full_name, email)
VALUES ('Alice Smith', 'alice@example.com');

-- INSERT multiple rows at once
INSERT INTO customers (full_name, email) VALUES
    ('Bob Jones', 'bob@example.com'),
    ('Carol Lee', 'carol@example.com');

-- UPDATE: Modify existing data
UPDATE customers
SET is_active = FALSE
WHERE email = 'bob@example.com';

-- DELETE: Remove specific rows
DELETE FROM customers WHERE is_active = FALSE;

-- UPSERT (PostgreSQL): insert or update on conflict
INSERT INTO customers (email, full_name)
VALUES ('alice@example.com', 'Alice Smith')
ON CONFLICT (email)
DO UPDATE SET full_name = EXCLUDED.full_name;
```

---

### DQL — Data Query Language

**DQL** is increasingly treated as its own sublanguage because it serves a fundamentally different purpose from DML: **reading data without modifying it**. It is composed almost entirely of the `SELECT` statement and its many clauses.

DQL is the most commonly used part of SQL in day-to-day application development — virtually every page load or API response involves at least one `SELECT`.

**Main DQL command:** `SELECT`

**DQL Examples:**

```sql
-- Basic SELECT
SELECT id, full_name, email FROM customers;

-- SELECT with WHERE filter
SELECT * FROM customers WHERE is_active = TRUE;

-- SELECT with ORDER BY and LIMIT (pagination)
SELECT full_name, email
FROM customers
ORDER BY full_name ASC
LIMIT 10 OFFSET 20;  -- Page 3 (10 items per page)

-- INNER JOIN: combine data from multiple tables
SELECT
    c.full_name          AS customer,
    o.id                 AS order_id,
    o.total_amount,
    o.created_at         AS order_date
FROM customers c
INNER JOIN orders o ON c.id = o.customer_id
WHERE o.total_amount > 100
ORDER BY o.created_at DESC;

-- LEFT JOIN: include customers even if they have no orders
SELECT c.full_name, COUNT(o.id) AS order_count
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
GROUP BY c.id, c.full_name
ORDER BY order_count DESC;

-- Aggregate functions
SELECT
    COUNT(*)                              AS total_customers,
    COUNT(*) FILTER (WHERE is_active)     AS active_customers,
    AVG(o.total_amount)                   AS avg_order_value,
    MAX(o.total_amount)                   AS largest_order
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id;

-- Subquery
SELECT full_name, email
FROM customers
WHERE id IN (
    SELECT DISTINCT customer_id FROM orders WHERE total_amount > 500
);

-- Common Table Expression (CTE) — named subquery for readability
WITH high_value_customers AS (
    SELECT customer_id, SUM(total_amount) AS lifetime_value
    FROM orders
    GROUP BY customer_id
    HAVING SUM(total_amount) > 1000
)
SELECT c.full_name, hvc.lifetime_value
FROM customers c
JOIN high_value_customers hvc ON c.id = hvc.customer_id
ORDER BY hvc.lifetime_value DESC;

-- Window function: rank without collapsing rows
SELECT
    full_name,
    total_amount,
    RANK() OVER (ORDER BY total_amount DESC) AS spend_rank
FROM customers c
JOIN orders o ON c.id = o.customer_id;
```

> **Note:** Some databases and textbooks classify `SELECT` under DML rather than as a separate DQL category. The practical distinction is that DQL operations are **read-only** and never modify data, while DML (INSERT, UPDATE, DELETE) always modifies data.

---

### DCL — Data Control Language

**DCL** is the subset of SQL used to **control access permissions** to the database and its objects. It defines who can do what — which users or roles can read, write, or modify specific tables, views, or schemas.

DCL is the **security layer** of SQL. In production systems, it enforces the **principle of least privilege** — each user or application service gets only the minimum permissions needed to do its job, reducing the blast radius of a compromised credential.

**Main DCL commands:**

| Command | Purpose |
|---|---|
| `GRANT` | Give a user or role permission to perform an action |
| `REVOKE` | Remove a previously granted permission |

**Common privileges you can grant:**

| Privilege | Allows |
|---|---|
| `SELECT` | Read data (DQL) |
| `INSERT` | Add new rows (DML) |
| `UPDATE` | Modify rows (DML) |
| `DELETE` | Remove rows (DML) |
| `EXECUTE` | Run stored procedures or functions |
| `CREATE` | Create new database objects (DDL) |
| `ALL PRIVILEGES` | Everything above |

**DCL Examples (PostgreSQL):**

```sql
-- Create application and reporting users
CREATE USER app_user WITH PASSWORD 'securepassword';
CREATE USER reporting_user WITH PASSWORD 'reportpassword';

-- GRANT: give app_user read/write access to specific tables
GRANT SELECT, INSERT, UPDATE, DELETE ON customers TO app_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON orders TO app_user;

-- GRANT: give reporting_user read-only access to all tables
GRANT SELECT ON ALL TABLES IN SCHEMA public TO reporting_user;

-- GRANT on a specific view (not the underlying table)
GRANT SELECT ON active_customers TO reporting_user;

-- Role-based access control (RBAC)
CREATE ROLE read_only_role;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO read_only_role;
GRANT read_only_role TO reporting_user;

-- REVOKE: remove a permission
REVOKE DELETE ON customers FROM app_user;
REVOKE ALL PRIVILEGES ON orders FROM reporting_user;

-- Row-Level Security (RLS) — advanced DCL in PostgreSQL
-- Each user can only see their own posts
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;

CREATE POLICY user_posts_policy ON posts
    USING (author_id = current_user_id());
-- Every SELECT on posts is now automatically filtered to the current user's rows
```

**DCL in a Django application context:**

Django applications connect to the database as a single database user. DCL is applied at the infrastructure level — not inside the Django app itself.

```python
# Best practice: use separate DB users per purpose
# Development:      full access
# Production app:   SELECT, INSERT, UPDATE, DELETE only (no DDL)
# Migration user:   full DDL + DML (used only during deployments)
# Read replica:     SELECT only (for analytics/reporting queries)

# settings.py
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "myapp_db",
        "USER": "app_user",            # DML only — principle of least privilege
        "PASSWORD": os.environ["DB_PASSWORD"],
        "HOST": "db.example.com",
    },
    "readonly": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "myapp_db",
        "USER": "reporting_user",      # SELECT only
        "PASSWORD": os.environ["DB_REPORTING_PASSWORD"],
        "HOST": "read-replica.example.com",
    }
}
```

---

### TCL — Transaction Control Language

**TCL** is the subset of SQL used to **manage transactions** — groups of one or more SQL statements that must execute together as a single, atomic unit of work.

TCL commands control whether a set of DML operations are permanently saved (`COMMIT`) or completely undone (`ROLLBACK`). TCL is the mechanism that makes ACID guarantees possible, and it is especially critical in any application where partial updates would leave data in an inconsistent state.

**Main TCL commands:**

| Command | Purpose |
|---|---|
| `BEGIN` / `START TRANSACTION` | Start a new transaction |
| `COMMIT` | Permanently save all changes made in the current transaction |
| `ROLLBACK` | Undo all changes made in the current transaction |
| `SAVEPOINT` | Create a named restore point within a transaction |
| `ROLLBACK TO SAVEPOINT` | Undo back to a savepoint (partial rollback) |
| `RELEASE SAVEPOINT` | Remove a savepoint (keeps changes, removes the marker) |
| `SET TRANSACTION` | Configure isolation level for the current transaction |

**TCL Examples:**

```sql
-- Basic transaction: bank transfer
BEGIN;
    UPDATE accounts SET balance = balance - 500 WHERE user_id = 1;
    UPDATE accounts SET balance = balance + 500 WHERE user_id = 2;
COMMIT;  -- Both committed, or:
-- ROLLBACK;  -- Neither committed (undo everything)
```

```sql
-- SAVEPOINT: partial rollback within a transaction
BEGIN;

    INSERT INTO audit_log (action) VALUES ('batch import started');

    SAVEPOINT before_inserts;

    INSERT INTO products (name, price) VALUES ('Widget A', 9.99);
    INSERT INTO products (name, price) VALUES ('Widget B', -1.00);  -- Invalid!

    -- Roll back only the inserts, keep the audit log entry
    ROLLBACK TO SAVEPOINT before_inserts;

    -- Retry with only valid data
    INSERT INTO products (name, price) VALUES ('Widget A', 9.99);

COMMIT;  -- Audit log + Widget A committed; Widget B never happened
```

**TCL in Python (psycopg2):**

```python
import psycopg2

connection = psycopg2.connect("postgresql://postgres:pass@localhost/myapp_db")
# psycopg2 starts transactions automatically (autocommit=False by default)

try:
    with connection.cursor() as cursor:
        cursor.execute(
            "UPDATE accounts SET balance = balance - %s WHERE username = %s",
            (500, "alice")
        )
        cursor.execute(
            "UPDATE accounts SET balance = balance + %s WHERE username = %s",
            (500, "bob")
        )
        # Verify no negative balances
        cursor.execute("SELECT balance FROM accounts WHERE username = 'alice'")
        if cursor.fetchone()[0] < 0:
            raise ValueError("Insufficient funds")

    connection.commit()   # TCL: COMMIT — persist changes
    print("Transfer successful")

except Exception as e:
    connection.rollback() # TCL: ROLLBACK — undo everything
    print(f"Transfer failed, rolled back: {e}")

finally:
    connection.close()
```

**TCL with a context manager (recommended pattern):**

```python
from contextlib import contextmanager

@contextmanager
def transaction(connection):
    """Commits on success, rolls back on any exception."""
    try:
        yield connection
        connection.commit()    # TCL: COMMIT
    except Exception:
        connection.rollback()  # TCL: ROLLBACK
        raise

connection = psycopg2.connect("postgresql://postgres:pass@localhost/myapp_db")

with transaction(connection):
    with connection.cursor() as cursor:
        cursor.execute("UPDATE accounts SET balance = balance - 100 WHERE username = 'alice'")
        cursor.execute("UPDATE accounts SET balance = balance + 100 WHERE username = 'bob'")
# Auto-commits on success, auto-rollbacks on exception
```

---

### Sublanguage Comparison Table

| Sublanguage | Full Name | Purpose | Commands | Transactional? |
|---|---|---|---|---|
| **DDL** | Data Definition Language | Define/modify database structure | CREATE, ALTER, DROP, TRUNCATE | Usually auto-commits; hard to roll back |
| **DML** | Data Manipulation Language | Insert, update, delete data | INSERT, UPDATE, DELETE, MERGE | Yes — can be rolled back with TCL |
| **DQL** | Data Query Language | Read/query data | SELECT | Read-only — no modification |
| **DCL** | Data Control Language | Manage permissions and access | GRANT, REVOKE | Auto-commits in most databases |
| **TCL** | Transaction Control Language | Manage transactions | BEGIN, COMMIT, ROLLBACK, SAVEPOINT | Is the mechanism that makes transactions work |

---

## 6. ACID Transactions

### What is ACID?

**ACID** is an acronym for four fundamental properties that guarantee database transactions are processed reliably, even in the face of errors, crashes, or concurrent access. ACID compliance is the gold standard for systems where data integrity is non-negotiable — financial services, healthcare, e-commerce, and any application where a half-applied change would cause serious harm.

---

### A — Atomicity

**"All or nothing."**

A transaction is treated as a single, indivisible unit. Either **all** of its operations succeed and are committed, or **none** of them are applied. There is no partial state.

**Why it matters:** Without atomicity, a crash mid-transaction could leave data in a corrupt, half-updated state.

**Classic example — bank transfer:**

```
Transfer $500 from Alice to Bob requires two steps:
  Step 1: Debit  Alice's account by $500  ← happens
  Step 2: Credit Bob's account by $500    ← system crashes before this

Without atomicity: $500 disappears from Alice but never arrives in Bob's account.

With atomicity:    The debit to Alice is automatically rolled back.
                   Neither account is changed. No money is lost.
```

```python
# Atomicity in Python
try:
    with connection.cursor() as cursor:
        cursor.execute("UPDATE accounts SET balance = balance - 500 WHERE id = 1")
        cursor.execute("UPDATE accounts SET balance = balance + 500 WHERE id = 2")
    connection.commit()     # Both committed atomically
except Exception:
    connection.rollback()   # Neither committed — atomicity preserved
```

---

### C — Consistency

**"The database goes from one valid state to another valid state."**

Every transaction must leave the database in a consistent state. Any data written must satisfy all defined rules: constraints, cascades, triggers, and foreign keys. A transaction that would violate these rules is rejected entirely.

**Why it matters:** Consistency prevents invalid data from ever being stored, regardless of how the application behaves.

```sql
-- Constraint: balance can never go negative
ALTER TABLE accounts ADD CONSTRAINT positive_balance CHECK (balance >= 0);

-- This transaction is rejected — consistency is preserved:
BEGIN;
    UPDATE accounts SET balance = balance - 10000 WHERE id = 1;  -- Would go negative
COMMIT;
-- ERROR: new row violates check constraint "positive_balance"
-- Transaction is automatically rolled back
```

```python
# Django enforces consistency at the model level
from django.core.exceptions import ValidationError

class Account(models.Model):
    balance = models.DecimalField(max_digits=12, decimal_places=2)

    def clean(self):
        if self.balance < 0:
            raise ValidationError("Balance cannot be negative.")
```

---

### I — Isolation

**"Concurrent transactions don't interfere with each other."**

Transactions executing at the same time are isolated from one another — each behaves as if it is the only transaction running. Changes made by a transaction in progress are invisible to other transactions until that transaction commits.

**Why it matters:** Without isolation, one transaction could read partial, uncommitted data written by another transaction — leading to incorrect results or logic errors.

**Isolation levels** (from weakest to strongest):

| Level | Dirty Reads | Non-Repeatable Reads | Phantom Reads | Performance |
|---|---|---|---|---|
| `READ UNCOMMITTED` | Possible | Possible | Possible | Fastest |
| `READ COMMITTED` | Prevented | Possible | Possible | Fast (default in PostgreSQL, MySQL) |
| `REPEATABLE READ` | Prevented | Prevented | Possible | Moderate |
| `SERIALIZABLE` | Prevented | Prevented | Prevented | Slowest, safest |

- **Dirty read:** Reading uncommitted data from another transaction (which might be rolled back).
- **Non-repeatable read:** Reading the same row twice and getting different values because another transaction modified it between your two reads.
- **Phantom read:** Running the same query twice and getting different rows because another transaction inserted or deleted rows in between.

```python
# Set isolation level in psycopg2
import psycopg2
from psycopg2 import extensions

connection = psycopg2.connect("postgresql://...")
connection.set_isolation_level(extensions.ISOLATION_LEVEL_SERIALIZABLE)
# Or: ISOLATION_LEVEL_READ_COMMITTED (default, good for most apps)
```

```python
# Django: configure isolation level per database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "OPTIONS": {
            "isolation_level": "serializable",
            # Options: "read committed", "repeatable read", "serializable"
        },
    }
}
```

---

### D — Durability

**"Committed transactions survive system failures."**

Once a transaction commits, it is permanently saved — even if the server crashes, loses power, or experiences hardware failure immediately afterward. Databases achieve durability by writing to a **write-ahead log (WAL)** on disk before acknowledging the commit to the application.

**Why it matters:** Without durability, a "successful" transaction could silently disappear after a crash, causing data loss with no indication to the application.

```
Timeline showing durability in action:
  T=0:00  Transaction begins — UPDATE accounts...
  T=0:01  Changes written to WAL (write-ahead log) on disk
  T=0:02  COMMIT acknowledged to application ✓
  T=0:03  Server crashes — power failure!
  T=0:05  Server restarts
  T=0:10  Database replays the WAL and restores the committed state ✓
          — No data loss, even though the server crashed after COMMIT
```

---

### ACID in Different Databases

| Database | ACID Support | Notes |
|---|---|---|
| **PostgreSQL** | Full ACID | Industry-leading compliance; configurable isolation levels; WAL by default |
| **MySQL (InnoDB)** | Full ACID | InnoDB engine only — MyISAM does NOT support transactions |
| **SQLite** | Full ACID | Serialized writes; WAL mode available; excellent for embedded use |
| **MongoDB** | Full ACID (v4.0+) | Multi-document transactions require a replica set (even single-node) |
| **Redis** | Partial | MULTI/EXEC is atomic but no rollback on logic errors; no durability by default |
| **Firestore** | Atomic transactions | Supports atomic multi-document reads/writes; strong consistency per document |
| **Neo4j** | Full ACID | Full ACID compliance including multi-node graph transactions |
| **Cassandra** | Eventual consistency | Prioritizes availability over strict consistency (CAP theorem trade-off) |

---

### ACID Transactions in Django

Django integrates ACID transaction management directly into the framework via TCL-backed tools.

```python
# settings.py — wrap every HTTP request in a transaction automatically (TCL)
DATABASES = {
    "default": {
        "ATOMIC_REQUESTS": True,  # BEGIN on request, COMMIT on success, ROLLBACK on exception
    }
}
```

```python
# services.py — explicit atomic blocks

from django.db import transaction
from myapp.models import Account, TransactionLog

# @transaction.atomic wraps the function in BEGIN...COMMIT / ROLLBACK
@transaction.atomic
def transfer_funds(sender_id, receiver_id, amount):
    # select_for_update() issues a SELECT ... FOR UPDATE, locking these rows
    # until the transaction ends — prevents race conditions (lost updates)
    sender   = Account.objects.select_for_update().get(id=sender_id)
    receiver = Account.objects.select_for_update().get(id=receiver_id)

    if sender.balance < amount:
        raise ValueError(f"Insufficient funds: balance is {sender.balance}")

    sender.balance   -= amount
    receiver.balance += amount

    sender.save()
    receiver.save()

    TransactionLog.objects.create(sender=sender, receiver=receiver, amount=amount)
    # Returns normally → Django COMMITs
    # Raises exception → Django ROLLBACKs — all three writes are undone


# transaction.atomic() as context manager
def process_order(order_data):
    with transaction.atomic():          # TCL: BEGIN
        order = Order.objects.create(**order_data)
        for item in order_data["items"]:
            product = Product.objects.select_for_update().get(id=item["product_id"])
            if product.stock < item["quantity"]:
                raise ValueError(f"Not enough stock for {product.name}")
            product.stock -= item["quantity"]
            product.save()
            OrderItem.objects.create(order=order, product=product, quantity=item["quantity"])
    # All changes COMMITted here, or all ROLLBACKed on any ValueError


# SAVEPOINT via nested atomic blocks
def import_products(product_list):
    with transaction.atomic():          # Outer transaction (BEGIN)
        imported, failed = 0, 0
        for product_data in product_list:
            try:
                with transaction.atomic():    # Creates a SAVEPOINT
                    Product.objects.create(**product_data)
                    imported += 1
            except Exception as e:
                failed += 1                   # ROLLBACK TO SAVEPOINT (this product only)
                print(f"Skipped {product_data['name']}: {e}")
        print(f"Imported {imported}, failed {failed}")
    # Outer COMMIT — all successfully imported products are saved


# transaction.on_commit() — run side effects ONLY after the transaction commits
# Essential for sending emails, firing webhooks, or queuing background jobs
def create_user_and_notify(user_data):
    with transaction.atomic():
        user = User.objects.create(**user_data)
        # This callback runs only if/when the transaction commits
        # If the transaction rolls back (e.g., duplicate email), no email is sent
        transaction.on_commit(lambda: send_welcome_email.delay(user.id))
```

---

## 7. UML and Database Diagrams

### What is UML?

**UML (Unified Modeling Language)** is a standardized visual language for designing and documenting software systems. In the context of databases, UML is used to create visual diagrams that show how data entities relate to each other — before you write any SQL or code.

The most relevant UML diagram type for databases is the **Entity-Relationship Diagram (ERD)**, sometimes also called a **Class Diagram** when used in an object-oriented context.

---

### Entity-Relationship Diagram (ERD)

An ERD shows:
- **Entities** (tables) — represented as rectangles
- **Attributes** (columns) — listed inside the rectangle
- **Relationships** — lines connecting entities, labeled with cardinality

**Cardinality notation:**
- `1` — exactly one
- `N` or `*` — many
- `0..1` — zero or one (optional)
- `1..*` — one or more

**Example: Blog Application ERD**

```
┌─────────────────┐         ┌──────────────────┐
│    users         │         │      posts        │
├─────────────────┤         ├──────────────────┤
│ PK id           │──1───N──│ PK id            │
│    username     │         │ FK user_id       │
│    email        │         │    title         │
│    password     │         │    body          │
│    created_at   │         │    published     │
└─────────────────┘         │    created_at    │
                            └──────────────────┘
                                      │ 1
                                      │
                                      N
                            ┌──────────────────┐
                            │    comments       │
                            ├──────────────────┤
                            │ PK id            │
                            │ FK post_id       │
                            │ FK user_id       │
                            │    body          │
                            │    created_at    │
                            └──────────────────┘

┌─────────────────┐         ┌──────────────────┐
│      posts      │──N───N──│      tags         │
├─────────────────┤         ├──────────────────┤
│ PK id           │         │ PK id            │
│    title        │         │    name          │
└─────────────────┘         └──────────────────┘
         │                           │
         └────────────┬──────────────┘
                      │
              ┌───────────────┐
              │  post_tags    │  ← Junction table (Many-to-Many)
              ├───────────────┤
              │ FK post_id    │
              │ FK tag_id     │
              └───────────────┘
```

---

### Graph Database Diagram (Property Graph Model)

For graph databases, the equivalent visual is a **property graph diagram** — showing nodes with labels and properties, and named, directed edges connecting them.

```
                ┌──────────────────────────┐
                │  :Person                 │
                │  name: "Alice"           │
                │  age: 30                 │
                └──────────┬───────────────┘
                           │
              ┌────────────┼───────────────────┐
    KNOWS     │            │ USES              │ MANAGES
    since:2020│            │                   │
              ▼            ▼                   ▼
  ┌──────────────────┐  ┌──────────────┐  ┌──────────────────┐
  │  :Person         │  │ :Technology  │  │  :Team           │
  │  name: "Bob"     │  │ name: "Django│  │  name: "Backend" │
  │  age: 25         │  │ type: "fw"   │  │  size: 5         │
  └──────────────────┘  └──────────────┘  └──────────────────┘
              │
    KNOWS     │ since:2021
              ▼
  ┌──────────────────┐
  │  :Person         │
  │  name: "Carol"   │
  │  age: 35         │
  └──────────────────┘
```

This diagram maps directly to Cypher:

```cypher
MERGE (alice:Person {name: 'Alice', age: 30})
MERGE (bob:Person {name: 'Bob', age: 25})
MERGE (carol:Person {name: 'Carol', age: 35})
MERGE (django:Technology {name: 'Django', type: 'framework'})
MERGE (backend:Team {name: 'Backend', size: 5})

MERGE (alice)-[:KNOWS {since: 2020}]->(bob)
MERGE (bob)-[:KNOWS {since: 2021}]->(carol)
MERGE (alice)-[:USES]->(django)
MERGE (alice)-[:MANAGES]->(backend)
```

---

### Relationship Types with Examples

**One-to-One (1:1)** — Each user has exactly one profile.
```
users ──1────1── profiles
```

**One-to-Many (1:N)** — One user can write many posts.
```
users ──1────N── posts
```

**Many-to-Many (N:N)** — Posts can have many tags; tags can be on many posts.
```
posts ──N────N── tags   (via post_tags junction table)
```

---

### Translating an ERD to SQL

```sql
CREATE TABLE users (
    id         SERIAL PRIMARY KEY,
    username   VARCHAR(100) NOT NULL UNIQUE,
    email      VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE posts (
    id         SERIAL PRIMARY KEY,
    user_id    INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title      VARCHAR(500) NOT NULL,
    body       TEXT,
    published  BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE tags (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

-- Junction table for Many-to-Many
CREATE TABLE post_tags (
    post_id INTEGER REFERENCES posts(id) ON DELETE CASCADE,
    tag_id  INTEGER REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (post_id, tag_id)
);
```

---

## 8. ORM — Object Relational Mapping

### What is an ORM?

An **ORM (Object Relational Mapper)** is a programming technique — and the library that implements it — that allows you to interact with a database using your programming language's objects and syntax instead of writing raw SQL.

With an ORM, each database table is mapped to a **class** (called a **model**), and each row in that table becomes an **instance** of that class. Columns map to **attributes** of the class.

**Without ORM (raw SQL in Python):**
```python
cursor.execute(
    "SELECT id, username, email FROM users WHERE is_active = TRUE AND email LIKE %s",
    ("%@example.com",)
)
rows = cursor.fetchall()
users = [{"id": r[0], "username": r[1], "email": r[2]} for r in rows]
```

**With ORM (Django):**
```python
users = User.objects.filter(is_active=True, email__endswith="@example.com")
```

The ORM translates the Python expression into the appropriate SQL query automatically, using the correct dialect for whichever database backend is configured.

---

### How ORMs Help

**1. Productivity:** You write Python instead of SQL — less context switching, fewer typos in query strings.

**2. Database abstraction:** Switching from SQLite to PostgreSQL often requires little to no change in your model code — the ORM handles dialect differences.

**3. Security:** ORMs use parameterized queries by default, preventing SQL injection.

**4. Maintainability:** Models are defined in one place. Schema changes update the model class and generate a migration automatically.

**5. Relationships made easy:** Navigating relationships becomes natural Python attribute access rather than manual JOIN queries.

**6. Transaction integration:** ORMs integrate directly with TCL — in Django, `@transaction.atomic` wraps ORM operations in a full ACID transaction.

**7. Migrations as DDL:** Most ORMs generate and apply DDL from your model definitions, giving you a version-controlled history of schema changes.

---

### Popular Python ORMs

| ORM | Best For | SQL Databases Supported |
|---|---|---|
| **Django ORM** | Django web apps, rapid development | SQLite, MySQL, PostgreSQL, Oracle |
| **SQLAlchemy** | Complex queries, full control, non-Django apps | SQLite, MySQL, PostgreSQL, Oracle, MS SQL, and more |
| **Peewee** | Small to medium apps, simplicity | SQLite, MySQL, PostgreSQL |
| **Tortoise ORM** | Async applications (FastAPI, etc.) | SQLite, MySQL, PostgreSQL |
| **PonyORM** | Readable query syntax | SQLite, MySQL, PostgreSQL, Oracle |

> **Note:** ORMs are primarily for relational (SQL) databases. For MongoDB, the equivalent is an **ODM (Object Document Mapper)**, such as **MongoEngine** or **Beanie** (async). For Neo4j, the Python equivalent is **neomodel**, which maps Cypher nodes to Python classes.

---

## 9. Django ORM in Practice

Django comes with a built-in, fully featured ORM. You define your database schema by writing Python model classes, and Django handles the SQL — covering all five sublanguages: DDL (via migrations), DML, DQL, DCL (via settings), and TCL (via transaction management).

---

### Setting Up Django with a Database

**`settings.py` — configure your database:**

```python
# SQLite (default, great for development)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# PostgreSQL (recommended for production)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "myapp_db",
        "USER": "app_user",           # DCL: restricted DB user
        "PASSWORD": os.environ["DB_PASSWORD"],
        "HOST": "localhost",
        "PORT": "5432",
        "ATOMIC_REQUESTS": True,      # TCL: wrap every view in a transaction
        "OPTIONS": {
            "isolation_level": "read committed",  # TCL: isolation level
        },
    },
    "readonly": {                     # DCL: separate read-only connection
        "ENGINE": "django.db.backends.postgresql",
        "USER": "reporting_user",     # SELECT only
        "HOST": "read-replica.example.com",
    }
}

# MySQL
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "myapp_db",
        "USER": "root",
        "PASSWORD": "yourpassword",
        "HOST": "localhost",
        "PORT": "3306",
    }
}
```

---

### Defining Models (DDL via Python Classes)

```python
# myapp/models.py
from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS_DRAFT = "draft"
    STATUS_PUBLISHED = "published"
    STATUS_CHOICES = [
        (STATUS_DRAFT, "Draft"),
        (STATUS_PUBLISHED, "Published"),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="posts"
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name="posts")

    title      = models.CharField(max_length=500)
    slug       = models.SlugField(max_length=500, unique=True)
    body       = models.TextField()
    status     = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    view_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Comment(models.Model):
    post       = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author     = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    body       = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"
```

---

### Migrations — DDL via the ORM

```bash
# Generate migration files (DDL described as Python)
python manage.py makemigrations

# Apply migrations (executes the DDL SQL)
python manage.py migrate

# Preview the SQL without running it
python manage.py sqlmigrate myapp 0001
```

Django translates your model into SQL like this:
```sql
CREATE TABLE "myapp_post" (
    "id"         SERIAL PRIMARY KEY,
    "author_id"  INTEGER NOT NULL REFERENCES "auth_user"("id"),
    "title"      VARCHAR(500) NOT NULL,
    "slug"       VARCHAR(500) NOT NULL UNIQUE,
    "body"       TEXT NOT NULL,
    "status"     VARCHAR(20) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL,
    "updated_at" TIMESTAMPTZ NOT NULL
);
```

---

### Querying with the Django ORM (DQL + DML via Python)

The Django ORM provides a **QuerySet** API. QuerySets are **lazy** — they don't hit the database until the data is actually accessed.

```python
from myapp.models import Post, Category, Tag
from django.contrib.auth.models import User
from django.db.models import Count, Q, Avg
from django.utils import timezone

# ─── CREATE (DML) ─────────────────────────────────────────────────────────

post = Post.objects.create(
    author=User.objects.get(username="alice"),
    title="Getting Started with Django",
    slug="getting-started-django",
    body="Django is a high-level Python web framework...",
    status=Post.STATUS_PUBLISHED
)

python_tag = Tag.objects.get_or_create(name="python")[0]
django_tag = Tag.objects.get_or_create(name="django")[0]
post.tags.add(python_tag, django_tag)


# ─── READ (DQL) ────────────────────────────────────────────────────────────

all_posts    = Post.objects.all()
published    = Post.objects.filter(status="published")
not_draft    = Post.objects.exclude(status="draft")
post         = Post.objects.get(slug="getting-started-django")

# Field lookups (double underscore syntax)
posts = Post.objects.filter(
    title__icontains="django",          # ILIKE '%django%'
    created_at__year=2024,              # YEAR(created_at) = 2024
    view_count__gte=100,                # view_count >= 100
    category__name__startswith="Tech"   # JOIN + WHERE
)

# Complex OR/AND with Q objects
complex_query = Post.objects.filter(
    Q(status="published") & (Q(view_count__gte=100) | Q(author__username="alice"))
)

# Avoid N+1 queries: load related objects efficiently
posts = (Post.objects
         .select_related("author", "category")    # JOIN (FK, OneToOne)
         .prefetch_related("tags", "comments")    # Separate query (M2M, reverse FK)
         .all())


# ─── UPDATE (DML) ──────────────────────────────────────────────────────────

post = Post.objects.get(slug="getting-started-django")
post.view_count += 1
post.save(update_fields=["view_count"])   # Only updates this column

Post.objects.filter(status="draft").update(status="published")  # Bulk update


# ─── DELETE (DML) ──────────────────────────────────────────────────────────

Post.objects.get(slug="old-post").delete()
Post.objects.filter(created_at__lt=timezone.now() - timezone.timedelta(days=365)).delete()


# ─── AGGREGATION (DQL) ─────────────────────────────────────────────────────

from django.db.models import Count, Avg, Sum

total      = Post.objects.filter(status="published").count()
avg_views  = Post.objects.aggregate(Avg("view_count"))  # {'view_count__avg': 342.5}

authors_with_counts = (User.objects
    .annotate(post_count=Count("posts"))
    .filter(post_count__gt=0)
    .order_by("-post_count"))

category_stats = (Category.objects
    .annotate(post_count=Count("posts"), avg_views=Avg("posts__view_count"))
    .order_by("-post_count"))
```

---

### Raw SQL When You Need It

```python
# Raw SQL query (returns model instances) — useful for DQL with complex logic
posts = Post.objects.raw("""
    SELECT p.*, COUNT(c.id) AS comment_count
    FROM myapp_post p
    LEFT JOIN myapp_comment c ON c.post_id = p.id
    WHERE p.status = 'published'
    GROUP BY p.id
    ORDER BY comment_count DESC
    LIMIT 10
""")

# Direct cursor access — useful for raw DQL, DCL, or complex DDL
from django.db import connection

with connection.cursor() as cursor:
    # Custom aggregate query (DQL)
    cursor.execute("""
        SELECT DATE_TRUNC('month', created_at) AS month, COUNT(*) AS post_count
        FROM myapp_post
        WHERE status = 'published'
        GROUP BY 1 ORDER BY 1 DESC
    """)
    monthly_stats = cursor.fetchall()

    # DCL: grant permissions programmatically (run during deployment)
    cursor.execute("GRANT SELECT ON myapp_post TO reporting_user")
```

---

### Django ORM Field Reference

| Field Type | Python Type | SQL Type |
|---|---|---|
| `CharField` | `str` | `VARCHAR` |
| `TextField` | `str` | `TEXT` |
| `IntegerField` | `int` | `INTEGER` |
| `FloatField` | `float` | `FLOAT` |
| `DecimalField` | `Decimal` | `DECIMAL` |
| `BooleanField` | `bool` | `BOOLEAN` |
| `DateField` | `date` | `DATE` |
| `DateTimeField` | `datetime` | `TIMESTAMP` |
| `JSONField` | `dict`/`list` | `JSONB` (Postgres) / `JSON` |
| `ForeignKey` | Model instance | `INTEGER` + FK constraint |
| `ManyToManyField` | QuerySet | Junction table |
| `OneToOneField` | Model instance | `INTEGER` + UNIQUE FK |
| `UUIDField` | `UUID` | `UUID` |
| `ImageField` | `str` (path) | `VARCHAR` |

---

### Summary: The Full Database Stack in a Django App

```
┌────────────────────────────────────────────────────────────────┐
│                       Your Python Code                         │
│             (views.py, services.py, tasks.py)                  │
└──────────┬──────────────┬───────────────────┬──────────────────┘
           │              │                   │
     DQL/DML          TCL via             DCL via
     via ORM      transaction.atomic    raw SQL / DB admin
     (QuerySet)   or ATOMIC_REQUESTS    (GRANT, REVOKE, RLS)
           │              │                   │
┌──────────▼──────────────▼───────────────────▼──────────────────┐
│                        Django ORM                              │
│                   (models.py, QuerySet)                        │
│         DDL ← python manage.py makemigrations / migrate        │
└──────────────────────────────┬─────────────────────────────────┘
                               │  SQL queries
┌──────────────────────────────▼─────────────────────────────────┐
│                       Database Driver                          │
│            (psycopg2, mysql-connector, neo4j, etc.)            │
└──────────────────────────────┬─────────────────────────────────┘
                               │  TCP / file / Bolt
┌──────────────────────────────▼─────────────────────────────────┐
│                  Database Server / Engine                      │
│    PostgreSQL · MySQL · SQLite · MongoDB · Neo4j · Redis       │
│                                                                │
│   DDL   →  Schema structure  (CREATE, ALTER, DROP)            │
│   DML   →  Data changes      (INSERT, UPDATE, DELETE)         │
│   DQL   →  Data reads        (SELECT)                         │
│   DCL   →  Permissions       (GRANT, REVOKE, RLS)             │
│   TCL   →  Transactions      (BEGIN, COMMIT, ROLLBACK)        │
│   ACID  →  Guarantees        (Atomicity, Consistency,         │
│                               Isolation, Durability)           │
└────────────────────────────────────────────────────────────────┘
```

---

*This guide covers the core concepts needed to work confidently with databases in Python and Django. As a next step, explore database indexing strategies, query optimization with `EXPLAIN ANALYZE`, connection pooling (pgBouncer for PostgreSQL), database replication for read scaling, and the CAP theorem for a deeper understanding of distributed database trade-offs.*
