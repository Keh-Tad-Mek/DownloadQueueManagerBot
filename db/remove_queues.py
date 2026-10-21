from db.db_conn import get_connection

def delete_queue(queue_id, user_id):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                # verify ownership
                cur.execute(
                    "SELECT 1 FROM queues WHERE queue_id = %s AND user_id = %s",
                    (queue_id, user_id)
                )
                if not cur.fetchone():
                    return False, "Queue not found."

                # delete items first
                cur.execute(
                    "DELETE FROM queue_items WHERE queue_id = %s",
                    (queue_id,)
                )
                # then the queue
                cur.execute(
                    "DELETE FROM queues WHERE queue_id = %s AND user_id = %s",
                    (queue_id, user_id)
                )
                conn.commit()
                return True, "Queue deleted."
            
    except Exception as e:
        print(str(e))
        return False, "Could not delete the queue."