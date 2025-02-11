# List of dependencies (migration that must be applied before this one)
dependencies = ["students.202502091505_initial"]

# SQL to apply the migration
apply = [
    """
    --sql
    CREATE TYPE PaymentType AS ENUM (
        'cheque',
        'upi',
        'neft', 
        'rtgs',
        'others'
    );
    """,
    """
    --sql
    CREATE TYPE FeesType AS ENUM (
        'tution_fees',
        'exam_fees',
        'card_fees',
        'others'
    );
    """,
    """
    --sql
    CREATE TABLE fees (
        id UUID DEFAULT gen_random_uuid(),
        recipt_id SERIAL NOT NULL,
        date DATE NOT NULL,
        student_id UUID NOT NULL,
        type FeesType NOT NULL,
        payment_type PaymentType NOT NULL,
        transaction_id VARCHAR(128) NOT NULL,
        amount FLOAT NOT NULL,
        created_at TIMESTAMP DEFAULT now(),
        CONSTRAINT pk_fees PRIMARY KEY (id),
        CONSTRAINT unique_fees_recipt_id UNIQUE (recipt_id),
        CONSTRAINT fk_fees_student FOREIGN KEY (student_id) REFERENCES students(id)
    );
    """,
    """
    --sql
    CREATE INDEX idx_fees_student ON fees (student_id);
    """,
]

# SQL to rollback the migration
rollback = [
    """
    --sql
    DROP TABLE fees;
    """,
    """
    --sql
    DROP TYPE FeesType;
    """,
    """
    --sql
    DROP TYPE PaymentType;
    """,
]
