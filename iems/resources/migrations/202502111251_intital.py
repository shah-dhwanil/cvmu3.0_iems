
# List of dependencies (migration that must be applied before this one)
dependencies = ["subjects.202502101316_initial", "staffs.202502091219_initial"]

# SQL to apply the migration
apply = [
        """
        --sql
        CREATE TYPE ResourceType AS ENUM (
            'lecture_notes',
            'lab_manual',
            'books',
            'reference_material',
            'syllabus',
            'others'
        );
        """,
        """
        --sql
        CREATE TABLE resources (
            id UUID DEFAULT gen_random_uuid(),
            subject_id UUID NOT NULL,
            title varchar(64) NOT NULL,
            shared_at TIMESTAMP WITH TIME ZONE NOT NULL,
            shared_by UUID NOT NULL,
            type ResourceType NOT NULL,
            docs_id UUID NOT NULL,
            CONSTRAINT pk_resources PRIMARY KEY (id),
            CONSTRAINT fk_resources_subject FOREIGN KEY (subject_id) REFERENCES subjects(id),
            CONSTRAINT fk_resources_staff FOREIGN KEY (shared_by) REFERENCES staff(id)
        );
        """,
        """
        --sql
        CREATE INDEX idx_resources_subject ON resources (subject_id);
        """,
]

# SQL to rollback the migration
rollback = [
    """
    --sql
    DROP TABLE resources;
    """,
    """
    --sql
    DROP TYPE ResourceType;
    """,
]
