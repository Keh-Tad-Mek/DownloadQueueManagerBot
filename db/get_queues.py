from db.db_conn import get_connection

def get_user_queues(user_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "select queue_id, queue_name from queues " \
                "where user_id = %s ORDER BY queue_name", 
                (user_id,)
            )
            return cur.fetchall()