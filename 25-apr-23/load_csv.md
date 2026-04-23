### Step 1 — Generate the CSV

Copy `generate_animals_csv.py` into your project root (next to `manage.py`) and run it once:

```bash
python generate_animals_csv.py
# ✓  Written 100 animals to 'animals_data.csv'
```

This creates `animals_data.csv` with realistic species, ages, weights, captivity flags, and dates spread across 2018–2025.

---

### Step 2 — Add the management command

Copy `import_animals_csv.py` into the management command path Django expects. You also need two `__init__.py` files to make the directories proper Python packages:

```bash
mkdir -p animals/management/commands
touch animals/management/__init__.py
touch animals/management/commands/__init__.py
cp import_animals_csv.py animals/management/commands/import_animals_csv.py
```

Your `animals/` directory should then contain:

```
animals/
└── management/
    ├── __init__.py
    └── commands/
        ├── __init__.py
        └── import_animals_csv.py
```

---

### Step 3 — Import the data

```bash
# Import from the default location (animals_data.csv in project root)
python manage.py import_animals_csv

# Or specify a custom path
python manage.py import_animals_csv --file /path/to/animals_data.csv

# Wipe the table first, then import fresh
python manage.py import_animals_csv --clear
```

---

### What each file does

`generate_animals_csv.py` — a standalone script (no Django needed) with a pool of 100 real zoo species, each with realistic age and weight ranges. Repeated species get suffixes (`African Lion II`, etc.). Weights are loosely scaled to age with ±15% noise so the data feels natural. Rows are sorted by `date_added` so the archive views have data spread across multiple years.

`import_animals_csv.py` — a proper Django management command that validates every row (checks types, non-empty name, positive weight, parseable date, valid boolean), skips bad rows with a clear error message rather than crashing, and uses `bulk_create` so all 100 rows land in a single SQL `INSERT` instead of 100 separate queries.