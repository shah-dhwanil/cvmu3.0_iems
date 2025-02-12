
# List of dependencies (migration that must be applied before this one)
dependencies = []

# SQL to apply the migration
apply = [
    """
    CREATE TABLE files (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        file_name VARCHAR(128) NOT NULL,
        file_type VARCHAR(64) NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    )
    """
]

# SQL to rollback the migration
rollback = [
    """
    DROP TABLE files
    """
]
