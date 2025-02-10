# List of dependencies (migration that must be applied before this one)
dependencies = ["batch.202502100544_initial"]

# SQL to apply the migration
apply = [
    """
    --sql
    CREATE TABLE semister (
        id UUID DEFAULT gen_random_uuid(),
        batch_id UUID NOT NULL REFERENCES batch(id),
        sem_no SMALLINT NOT NULL,
        ongoing BOOLEAN NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        active BOOLEAN DEFAULT TRUE,
        CONSTRAINT pk_sem PRIMARY KEY (id),
        CONSTRAINT unique_sem_batch_sem_no UNIQUE (batch_id, sem_no)
    );
    """
]

# SQL to rollback the migration
rollback = [
    """
    --sql
    DROP TABLE semister;
    """
]
