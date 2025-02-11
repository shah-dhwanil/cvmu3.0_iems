# List of dependencies (migration that must be applied before this one)
dependencies = ["courses.202502101338_initial", "students.202502091505_initial"]

# SQL to apply the migration
apply = [
    """
    --sql
    CREATE TABLE attendence (
        id UUID DEFAULT gen_random_uuid(),
        course_id UUID NOT NULL,
        student_id UUID NOT NULL,
        class_time TIMESTAMP WITH TIME ZONE NOT NULL,
        present BOOLEAN NOT NULL,
        dont_care BOOLEAN DEFAULT FALSE,
        CONSTRAINT pk_attendence PRIMARY KEY (id),
        CONSTRAINT fk_attendence_courses FOREIGN KEY (course_id) REFERENCES courses(id),
        CONSTRAINT fk_attendence_students FOREIGN KEY (student_id) REFERENCES students(id)
    );
    """
]

# SQL to rollback the migration
rollback = [
    """
    --sql
    DROP TABLE attendence;
    """
]
