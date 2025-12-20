from app.services.analytics import analytics_engine

def get_ticket_status_distribution():
    query = """
    SELECT status, count(*) as count 
    FROM tickets 
    GROUP BY status
    """
    return analytics_engine.run_query(query)

def get_average_messages_per_ticket():
    query = """
    SELECT avg(msg_count) as avg_messages 
    FROM (
        SELECT ticket_id, count(*) as msg_count 
        FROM messages 
        GROUP BY ticket_id
    )
    """
    return analytics_engine.run_query(query)

def get_peak_activity_hours():
    query = """
    SELECT hour(created_at) as hour, count(*) as count 
    FROM messages 
    GROUP BY hour 
    ORDER BY count DESC
    """
    return analytics_engine.run_query(query)
