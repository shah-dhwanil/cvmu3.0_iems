
# List of dependencies (migration that must be applied before this one)
dependencies = ["students.202502091505_initial"]

# SQL to apply the migration
apply = [
    """
    --sql
    CREATE TABLE external_exams (
        id UUID DEFAULT gen_random_uuid(),
        student_id UUID NOT NULL REFERENCES students(id),
        name VARCHAR(64) NOT NULL,
        score DECIMAL(4,2) NOT NULL,
        seat_no VARCHAR(64) NOT NULL,
        yoa INT NOT NULL,
        rank INT,
        marksheet_uuid UUID,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        CONSTRAINT pk_external_exams PRIMARY KEY (id)
    );
    """
]

# SQL to rollback the migration
rollback = [
    """
    --sql
    DROP TABLE external_exams;
    """
]
