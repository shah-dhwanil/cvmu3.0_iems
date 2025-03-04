# List of dependencies (migration that must be applied before this one)
dependencies = ["students.202502091505_initial", "attendence.202502110419_initial"]

# SQL to apply the migration
apply = [
    """
    --sql
    CREATE TYPE LeaveStatus AS ENUM (
        'submitted',
        'declined_counciller',
        'approved_counciller',
        'declined_hod',
        'approved'
    );
    """,
    """
    --sql
    CREATE TABLE leaves (
        id UUID DEFAULT gen_random_uuid(),
        student_id UUID NOT NULL,
        from_date DATE NOT NULL,
        to_date DATE NOT NULL,
        reason TEXT NOT NULL,
        status LeaveStatus NOT NULL DEFAULT 'submitted',
        document_id UUID,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
        CONSTRAINT pk_leaves PRIMARY KEY (id),
        CONSTRAINT fk_leaves_student FOREIGN KEY (student_id) REFERENCES students (id)
    );
    """,
]

# SQL to rollback the migration
rollback = [
    """
    --sql
    DROP TABLE leaves;
    """,
    """
    --sql
    DROP TYPE LeaveStatus;
    """,
]
