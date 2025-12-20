import duckdb
import os
from app.core.config import settings

class AnalyticsEngine:
    def __init__(self):
        self.db_path = "data/analytics.duckdb"
        if not os.path.exists(os.path.dirname(self.db_path)):
            os.makedirs(os.path.dirname(self.db_path))
        
        self.con = duckdb.connect(self.db_path)
        # Install postgres extension for seamless ingestion
        self.con.execute("INSTALL postgres; LOAD postgres;")

    def ingest_from_postgres(self):
        """
        Periodically pull data from Postgres into DuckDB.
        This ensures OLAP queries do not lock the transactional DB.
        """
        pg_conn_str = (
            f"dbname={settings.POSTGRES_DB} "
            f"user={settings.POSTGRES_USER} "
            f"password={settings.POSTGRES_PASSWORD} "
            f"host={settings.POSTGRES_SERVER} "
            f"port={settings.POSTGRES_PORT}"
        )
        
        print("Ingesting data from Postgres to DuckDB...")
        
        # Create denormalized analytic tables
        self.con.execute(f"""
            CREATE OR REPLACE TABLE tickets AS 
            SELECT * FROM postgres_scan('{pg_conn_str}', 'public', 'tickets');
        """)
        
        self.con.execute(f"""
            CREATE OR REPLACE TABLE messages AS 
            SELECT * FROM postgres_scan('{pg_conn_str}', 'public', 'messages');
        """)
        
        print("Ingestion complete.")

    def run_query(self, query: str):
        return self.con.execute(query).fetchdf()

analytics_engine = AnalyticsEngine()
