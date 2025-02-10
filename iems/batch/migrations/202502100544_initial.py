# List of dependencies (migration that must be applied before this one)
dependencies = ["staffs.202502091219_initial"]

# SQL to apply the migration
apply = [
    """--sql
    CREATE TABLE batch (
        id UUID PRIMARY KEY,
        branch VARCHAR(32) NOT NULL,
        year SMALLINT NOT NULL,
        hod_id UUID NOT NULL REFERENCES staff(id),
        counciller_id UUID NOT NULL REFERENCES staff(id),
        active BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
    """
]

# SQL to rollback the migration
rollback = [
    """--sql
    DROP TABLE batch;
    """
]
