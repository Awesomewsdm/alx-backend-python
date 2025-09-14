import sqlite3 
import functools

# Copy the with_db_connection decorator from previous task
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
    return wrapper

# Transactional decorator
def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()  # Commit if no exception
            return result
        except Exception as e:
            conn.rollback()  # Rollback on error
            raise e  # Re-raise the exception
    return wrapper

@with_db_connection 
@transactional 
def update_user_email(conn=None, user_id=None, new_email=None): 
    if conn is None:
        raise ValueError("Database connection not provided")
    cursor = conn.cursor() 
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 

#### Update user's email with automatic transaction handling 
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')