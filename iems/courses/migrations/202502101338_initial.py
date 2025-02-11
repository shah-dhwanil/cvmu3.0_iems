# List of dependencies (migration that must be applied before this one)
dependencies = [
    "semister.202502100623_initial",
    "subjects.202502101316_initial",
    "staffs.202502091219_initial",
]

# SQL to apply the migration
apply = [
    """
    --sql
    CREATE TABLE courses (
        id UUID DEFAULT gen_random_uuid(),
        sem_id UUID NOT NULL,
        subject_id UUID NOT NULL,
        taught_by UUID NOT NULL,
        active BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT pk_courses PRIMARY KEY (id),
        CONSTRAINT fk_courses_sem FOREIGN KEY (sem_id) REFERENCES semister(id),
        CONSTRAINT fk_courses_subject FOREIGN KEY (subject_id) REFERENCES subjects(id),
        CONSTRAINT fk_courses_staff FOREIGN KEY (taught_by) REFERENCES staff(id)
    );
    """
]

# SQL to rollback the migration
rollback = [
    """
    --sql
    DROP TABLE courses;
    """
]
