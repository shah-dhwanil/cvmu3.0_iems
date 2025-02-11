# List of dependencies (migration that must be applied before this one)
dependencies = ["students.202502091505_initial"]

# SQL to apply the migration
apply = [
    """
    --sql
    CREATE TYPE AchievementType AS ENUM (
        'academic',
        'sports',
        'cultural',
        'other'
    );
    """,
    """
    --sql
    CREATE TYPE AchievementRank AS ENUM (
        'participation',
        'first',
        'second', 
        'third',
        'others'
    );
    """,
    """
    --sql
    CREATE TABLE achievements (
        id UUID DEFAULT gen_random_uuid(),
        student_id UUID NOT NULL,
        name VARCHAR(32) NOT NULL,
        type AchievementType NOT NULL,
        pos AchievementRank NOT NULL,
        docs_id UUID,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT pk_achievements PRIMARY KEY (id),
        CONSTRAINT fk_achievements_student FOREIGN KEY (student_id) REFERENCES students(id)
    );
    """,
]

# SQL to rollback the migration
rollback = [
    """
    --sql
    DROP TABLE achievements;
    """,
    """
    --sql
    DROP TYPE AchievementRank;
    """,
    """
    --sql
    DROP TYPE AchievementType;
    """,
]
