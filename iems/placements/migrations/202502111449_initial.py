# List of dependencies (migration that must be applied before this one)
dependencies = ["students.202502091505_initial"]

# SQL to apply the migration
apply = [
    """
    --sql
    CREATE TYPE PlacementStatus AS ENUM (
        'offered',
        'accepted',
        'rejected'
    );
    """,
    """
    --sql
    CREATE TABLE placement (
        id UUID DEFAULT gen_random_uuid(),
        student_id UUID NOT NULL,
        company_name VARCHAR(64) NOT NULL,
        role VARCHAR(64) NOT NULL,
        package DECIMAL(6,2) NOT NULL,
        status PlacementStatus NOT NULL DEFAULT 'offered',
        letter_uid UUID,
        created_at TIMESTAMPTZ DEFAULT now(),
        CONSTRAINT pk_placement PRIMARY KEY (id),
        CONSTRAINT fk_placement_student FOREIGN KEY (student_id) REFERENCES students(id)
    );
    """,
    """
    --sql
    CREATE INDEX idx_placement_student_id ON placement (student_id);
    """,
]

# SQL to rollback the migration
rollback = [
    """
    --sql
    DROP TABLE placement;
    """,
    """
    --sql
    DROP TYPE PlacementStatus;
    """,
]
