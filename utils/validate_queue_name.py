import re

def name_is_valid(queue_name):
    if queue_name == "_":
        return False, "Queue name cannot be just an underscore."

    if len(queue_name) < 5:
        return False, "Queue name cannot be less than 5 characters."

    if len(queue_name) > 20:
        return False, "Queue name cannot be more than 20 characters."

    if re.search(r"[^A-Za-z0-9_]", queue_name):
        return False, "Queue name can only contain letters, numbers, and underscores."

    if not re.search(r"[A-Za-z]", queue_name):
        return False, "Queue name must contain at least one letter."  

    if queue_name[0].isdigit():
        return False, "Queue name cannot start with a number."

    if queue_name[0] == "_" or queue_name[-1] == "_":
        return False, "Queue name cannot start or end with an underscore."


    return True, "Queue name is valid." 