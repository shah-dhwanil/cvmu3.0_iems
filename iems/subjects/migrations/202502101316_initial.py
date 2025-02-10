# List of dependencies (migration that must be applied before this one)
dependencies = []

# SQL to apply the migration
apply = [
    """
    --sql
    CREATE TABLE subjects (
        id UUID PRIMARY KEY NOT NULL,
        code VARCHAR(16) NOT NULL,
        name VARCHAR(64) NOT NULL,
        credits SMALLINT NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        active BOOLEAN DEFAULT TRUE
    );
    """
]

# SQL to rollback the migration
rollback = [
    """
    --sql
    DROP TABLE subjects;
    """
]
