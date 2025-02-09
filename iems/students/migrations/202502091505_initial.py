# List of dependencies (migration that must be applied before this one)
dependencies = ["users.202502080929_initial"]

# SQL to apply the migration
apply = [
    """--sql
    CREATE TABLE students (
        id UUID REFERENCES users(id),
        first_name VARCHAR(32) NOT NULL,
        last_name VARCHAR(32) NOT NULL,
        enrollment_id VARCHAR(16) NOT NULL,
        gender CHAR NOT NULL,
        contact_no VARCHAR(16) NOT NULL,
        email_id VARCHAR(32) NOT NULL,
        active BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT pk_students PRIMARY KEY (id),
        CONSTRAINT unique_students_enrollment_id UNIQUE (enrollment_id),
        CONSTRAINT unique_students_contact_no UNIQUE (contact_no),
        CONSTRAINT unique_students_email_id UNIQUE (email_id)
    );
    """
]

# SQL to rollback the migration
rollback = [
    """--sql
    DROP TABLE students;
    """
]
