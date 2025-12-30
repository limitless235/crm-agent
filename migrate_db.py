import psycopg2
import os

# Database connection parameters from environment or defaults
DB_HOST = os.getenv("POSTGRES_SERVER", "localhost")
DB_NAME = os.getenv("POSTGRES_DB", "support_db")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "postgres")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")

def migrate():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            port=DB_PORT
        )
        conn.autocommit = True
        cur = conn.cursor()

        print(f"Connecting to database {DB_NAME} at {DB_HOST}...")

        # Add columns if they don't exist
        columns_to_add = [
            ("draft_response", "TEXT"),
            ("extracted_fields", "JSONB"),
            ("predicted_csat", "INTEGER"),
            ("is_chronic", "BOOLEAN DEFAULT FALSE")
        ]

        for col_name, col_type in columns_to_add:
            try:
                cur.execute(f"ALTER TABLE messages ADD COLUMN {col_name} {col_type};")
                print(f"Added column: {col_name}")
            except psycopg2.errors.DuplicateColumn:
                print(f"Column already exists: {col_name}")
            except Exception as e:
                print(f"Error adding column {col_name}: {e}")

        print("Migration completed successfully!")
        cur.close()
        conn.close()

    except Exception as e:
        print(f"Migration failed: {e}")

if __name__ == "__main__":
    migrate()
