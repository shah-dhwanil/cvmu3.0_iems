
# List of dependencies (migration that must be applied before this one)
dependencies = ["students.202502101251_add_batch","semister.202502100623_initial"]

# SQL to apply the migration
apply = [
    """--sql 
    ALTER TABLE students ADD COLUMN current_sem UUID REFERENCES semister(id);
    """
]

# SQL to rollback the migration
rollback = [
    """--sql 
    ALTER TABLE students DROP COLUMN current_sem;
    """
]
