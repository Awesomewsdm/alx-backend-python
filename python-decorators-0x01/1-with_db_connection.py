import sqlite3 
import functools

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Establish database connection
        conn = sqlite3.connect('users.db')
        try:
            # Inject the connection as a keyword argument (not part of public signature)
            result = func(*args, conn=conn, **kwargs)
            return result
        finally:
            # Ensure connection is closed even if an error occurs
            conn.close()
    return wrapper

@with_db_connection 
def get_user_by_id(user_id, conn=None): 
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,)) 
    return cursor.fetchone() 

#### Fetch user by ID with automatic connection handling 
user_id = 1
user = get_user_by_id(user_id)
print(user)