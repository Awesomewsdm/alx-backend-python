import time
import sqlite3 
import functools

# with_db_connection decorator
def with_db_connection(func):
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
    return wrapper

query_cache = {}

# Cache query decorator
def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        # Use query as cache key
        cache_key = query
        
        # Check if result is in cache
        if cache_key in query_cache:
            print("Using cached result")
            return query_cache[cache_key]
        
        # Execute query and cache result
        print("Executing query and caching result")
        result = func(conn, query, *args, **kwargs)
        query_cache[cache_key] = result
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")