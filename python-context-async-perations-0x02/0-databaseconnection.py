import sqlite3

class DatabaseConnection:
    """A custom context manager for database connections"""
    
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        self.cursor = None
    
    def __enter__(self):
        """Enter the runtime context and return the connection"""
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        return self.cursor
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the runtime context and close the connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        # Return False to propagate exceptions, True to suppress them
        return False

# Example usage
if __name__ == "__main__":
    # Create a test database and table
    with sqlite3.connect("test.db") as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
        cursor.execute("INSERT OR IGNORE INTO users (name, age) VALUES ('Alice', 30), ('Bob', 25), ('Charlie', 35)")
        conn.commit()
    
    # Use the context manager
    with DatabaseConnection("test.db") as cursor:
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        print("Users in the database:")
        for row in results:
            print(row)