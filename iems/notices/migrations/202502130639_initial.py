
# List of dependencies (migration that must be applied before this one)
dependencies = ["staffs.202502091219_initial","batch.202502100544_initial"]

# SQL to apply the migration
apply = [
    """
    --sql
    CREATE TABLE notices (
        id UUID DEFAULT gen_random_uuid(),
        created_by UUID NOT NULL,
        title VARCHAR(32) NOT NULL,
        description TEXT NOT NULL,
        target_audience VARCHAR(32),
        batch_id UUID,
        docs_id UUID,
        created_at TIMESTAMP DEFAULT NOW(),
        CONSTRAINT pk_notices PRIMARY KEY (id),
        CONSTRAINT fk_notices_created_by FOREIGN KEY (created_by) REFERENCES staff(id),
        CONSTRAINT fk_notices_batch_id FOREIGN KEY (batch_id) REFERENCES batch(id)
    );
    """
]

# SQL to rollback the migration
rollback = [
    """
    --sql
    DROP TABLE notices;
    """
]
