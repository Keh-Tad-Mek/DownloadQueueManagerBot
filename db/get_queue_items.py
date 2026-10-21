from db.db_conn import get_connection


def get_queue_items(queue_id):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT item_id, file_id, position, status
                    FROM queue_items
                    WHERE queue_id = %s
                    ORDER BY position ASC
                    """,
                    (queue_id,)
                )
                return cur.fetchall()
    except Exception as e:
        print(str(e))
        return []