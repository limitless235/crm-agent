from app.services.analytics import analytics_engine
from app.queries import example_queries
import time

def main():
    print("AntiGravity Analytics Worker Started")
    
    # Perform initial ingestion
    try:
        analytics_engine.ingest_from_postgres()
    except Exception as e:
        print(f"Initial ingestion failed: {e}")

    # Run sample reports
    print("\n--- Ticket Status Distribution ---")
    print(example_queries.get_ticket_status_distribution())
    
    print("\n--- Average Messages Per Ticket ---")
    print(example_queries.get_average_messages_per_ticket())

if __name__ == "__main__":
    main()
