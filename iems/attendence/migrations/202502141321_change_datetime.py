
# List of dependencies (migration that must be applied before this one)
dependencies = ["attendence.202502110419_initial"]

# SQL to apply the migration
apply = [
    """
    --sql
    ALTER TABLE attendence
    ALTER COLUMN class_time TYPE TIMESTAMP;
    """
]

# SQL to rollback the migration
rollback = [
    """
    --sql
    ALTER TABLE attendence
    ALTER COLUMN class_time TYPE TIMESTAMP WITH TIME ZONE;
    """
]
