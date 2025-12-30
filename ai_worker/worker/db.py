import psycopg2
from psycopg2.extras import RealDictCursor
from worker.settings import settings
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        self.dsn = f"host={settings.POSTGRES_SERVER} port={settings.POSTGRES_PORT} dbname={settings.POSTGRES_DB} user={settings.POSTGRES_USER} password={settings.POSTGRES_PASSWORD}"

    def get_ticket_history(self, ticket_id: str, limit: int = 10):
        try:
            conn = psycopg2.connect(self.dsn)
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                query = """
                    SELECT content, sender_id, is_internal 
                    FROM messages 
                    WHERE ticket_id = %s 
                    ORDER BY created_at ASC 
                    LIMIT %s
                """
                cur.execute(query, (ticket_id, limit))
                results = cur.fetchall()
                
                history = []
                for row in results:
                    history.append({
                        "role": "assistant" if row['is_internal'] else "user",
                        "content": row['content']
                    })
                return history
        except Exception as e:
            logger.error(f"Failed to fetch history: {e}")
            return []
        finally:
            if conn:
                conn.close()

    def get_user_id_from_ticket(self, ticket_id: str):
        conn = None
        try:
            conn = psycopg2.connect(self.dsn)
            with conn.cursor() as cur:
                cur.execute("SELECT user_id FROM tickets WHERE id = %s", (ticket_id,))
                result = cur.fetchone()
                return str(result[0]) if result else None
        except Exception as e:
            logger.error(f"Failed to fetch user_id: {e}")
            return None
        finally:
            if conn:
                conn.close()

    def get_user_ticket_count(self, user_id: str, days: int = 30):
        conn = None
        try:
            conn = psycopg2.connect(self.dsn)
            with conn.cursor() as cur:
                query = """
                    SELECT COUNT(*) 
                    FROM tickets 
                    WHERE user_id = %s 
                    AND created_at > (NOW() - INTERVAL '%s days')
                """
                cur.execute(query, (user_id, days))
                result = cur.fetchone()
                return result[0] if result else 0
        except Exception as e:
            logger.error(f"Failed to fetch ticket count: {e}")
            return 0
        finally:
            if conn:
                conn.close()

db_manager = DatabaseManager()
