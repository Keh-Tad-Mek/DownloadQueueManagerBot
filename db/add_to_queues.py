from db.db_conn import get_connection

conn = None
cur = None

def add_to_queue(queue_id, file_id):
    if not queue_id or not file_id:
        return False, "Queue ID and file ID are required."

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT 1 FROM queue_items WHERE queue_id = %s AND file_id = %s",
                    (queue_id, file_id)
                )
                if cur.fetchone():
                    return False, "This file is already in that queue."

                cur.execute(
                    """
                    INSERT INTO queue_items (queue_id, file_id, position)
                    VALUES (
                        %s,
                        %s,
                        (SELECT COALESCE(MAX(position), 0) + 1
                         FROM queue_items
                         WHERE queue_id = %s)
                    )
                    """,
                    (queue_id, file_id, queue_id)
                )
                conn.commit()
                return True, "File added to queue."
    except Exception as e:
        print(str(e))
        return False, "Could not add the file to the queue."