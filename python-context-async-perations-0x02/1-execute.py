import sqlite3

class ExecuteQuery:
    """A reusable context manager for executing parameterized queries"""
    
    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params or ()
        self.connection = None
        self.cursor = None
        self.results = None
    
    def __enter__(self):
        """Enter the runtime context and execute the query"""
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        return self.results
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the runtime context and clean up resources"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        return False

# Example usage
if __name__ == "__main__":
    # Create test data
    with sqlite3.connect("test.db") as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
        cursor.execute("INSERT OR IGNORE INTO users (name, age) VALUES ('Alice', 30), ('Bob', 25), ('Charlie', 35), ('David', 40)")
        conn.commit()
    
    # Use the reusable query context manager
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)
    
    with ExecuteQuery("test.db", query, params) as results:
        print("Users older than 25:")
        for row in results:
            print(row)