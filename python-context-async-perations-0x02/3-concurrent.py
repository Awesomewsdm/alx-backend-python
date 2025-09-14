import asyncio
import aiosqlite

async def async_fetch_users():
    """Fetch all users from the database"""
    async with aiosqlite.connect("test.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            results = await cursor.fetchall()
            print("All users:")
            for row in results:
                print(row)
            return results

async def async_fetch_older_users():
    """Fetch users older than 40 from the database"""
    async with aiosqlite.connect("test.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            results = await cursor.fetchall()
            print("Users older than 40:")
            for row in results:
                print(row)
            return results

async def fetch_concurrently():
    """Run both queries concurrently using asyncio.gather"""
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    return results

async def setup_test_database():
    """Set up test database with sample data"""
    async with aiosqlite.connect("test.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT,
                age INTEGER
            )
        """)
        await db.execute("DELETE FROM users")  # Clear existing data
        await db.executemany(
            "INSERT INTO users (name, age) VALUES (?, ?)",
            [('Alice', 30), ('Bob', 25), ('Charlie', 35), ('David', 40), ('Eve', 45)]
        )
        await db.commit()

async def main():
    """Main function to run the concurrent queries"""
    # Set up test database first
    await setup_test_database()
    
    # Run concurrent queries
    results = await fetch_concurrently()
    return results

if __name__ == "__main__":
    # Run the main async function
    asyncio.run(main())