from db.db_conn import get_connection

conn = None
cursor = None
def register_queue(queue_name, user_id):
    if not queue_name or not user_id:
        return False, "Queue name and user ID are required."
    
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                # Check if the queue already exists for the user
                cursor.execute("SELECT * FROM queues WHERE queue_name = %s AND user_id = %s", (queue_name, user_id))
                existing_queue = cursor.fetchone()

                if existing_queue:
                    return False, "Queue already exists."

                # Insert the new queue into the database
                cursor.execute("INSERT INTO queues (queue_name, user_id) VALUES (%s, %s)", (queue_name, user_id))
                conn.commit()

                return True, "Queue created successfully."
    
    except Exception as e:
        print(str(e))
        return False, "An error occured while creating the queue. Please try again."

   
