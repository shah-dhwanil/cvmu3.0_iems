# List of dependencies (migration that must be applied before this one)
dependencies = []

# SQL to apply the migration
apply = [
    """
    --sql
    CREATE TYPE Roles AS ENUM (
        'admin',
        'principal',
        'hod',
        'academic_staff',
        'teacher',
        'student',
        'parents',
        'account_staff',
        'others'
    );
    """,
    """
    --sql
    CREATE TABLE users (
        id UUID DEFAULT gen_random_uuid(),
        username VARCHAR(32) NOT NULL,
        password BYTEA NOT NULL,
        role Roles NOT NULL,
        active BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT pk_users PRIMARY KEY (id),
        CONSTRAINT unique_users_username UNIQUE (username)
    );
    """,
    """
    --sql
    CREATE INDEX idx_users_role ON users (role);
    """,
    """
    --sql
    INSERT INTO users (id, username, password, role) 
    VALUES (
        '0194e92d-32f5-78db-abe3-236fd234d839',
        'admin',
        -- bcrypt hash for 'admin'
        '$argon2id$v=19$m=65536,t=3,p=4$cfsuMRLM9Du3v41KFlZMiw$j6zQv23xtp6aJWRvRYWow5qj1KlXg1QCBEPL2g2MM+M',
        'admin'
    );
    """,
]

# SQL to rollback the migration
rollback = [
    """
    --sql
    DELETE FROM users WHERE username = 'admin';
    """,
    """
    --sql
    DROP TABLE users;
    """,
    """
    --sql
    DROP TYPE Roles;
    """,
]
