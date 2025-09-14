import sqlite3
import functools

#### decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the query from keyword arguments
        query = kwargs.get('query')
        if query:
            print(f"Executing query: {query}")
        else:
            # If query is passed as positional argument, try to find it
            for arg in args:
                if isinstance(arg, str) and arg.strip().upper().startswith(('SELECT', 'INSERT', 'UPDATE', 'DELETE')):
                    print(f"Executing query: {arg}")
                    break
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")