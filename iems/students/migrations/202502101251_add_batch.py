# List of dependencies (migration that must be applied before this one)
dependencies = ["students.202502091505_initial", "batch.202502100544_initial"]

# SQL to apply the migration
apply = [
    """--sql 
    ALTER TABLE students ADD COLUMN batch_id UUID REFERENCES batch(id);
    """
]

# SQL to rollback the migration
rollback = [
    """--sql 
    ALTER TABLE students DROP COLUMN batch_id;
    """
]
