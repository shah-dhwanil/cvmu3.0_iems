
# List of dependencies (migration that must be applied before this one)
dependencies = ["fees.202502111402_initial"]

# SQL to apply the migration
apply = [
    "ALTER TABLE fees ADD COLUMN status VARCHAR(255) NOT NULL DEFAULT 'PENDING';",
    "ALTER TABLE fees ADD COLUMN docs_id UUID DEFAULT null;",
]

# SQL to rollback the migration
rollback = [
    "ALTER TABLE fees DROP COLUMN status;",
    "ALTER TABLE fees DROP COLUMN docs_id;",
]
