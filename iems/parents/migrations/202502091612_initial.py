# List of dependencies (migration that must be applied before this one)
dependencies = ["users.202502080929_initial", "students.202502091505_initial"]

# SQL to apply the migration
apply = [
    """--sql
    CREATE TABLE parents (
        id UUID REFERENCES users(id),
        student_id UUID NOT NULL REFERENCES students(id),
        father_name VARCHAR(32) NOT NULL,
        mother_name VARCHAR(32) NOT NULL,
        contact_no VARCHAR(16) NOT NULL,
        email_id VARCHAR(32) NOT NULL,
        active BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT pk_parents PRIMARY KEY (id),
        CONSTRAINT unique_parents_student_id UNIQUE (student_id)
    );
    """
]

# SQL to rollback the migration
rollback = [
    """--sql
    DROP TABLE parents;
    """
]
