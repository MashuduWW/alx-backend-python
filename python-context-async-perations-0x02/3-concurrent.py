import aiosqlite
import asyncio

DB_NAME = "airbnb.db"

async def asyncfetchusers():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            return users

async def asyncfetcholder_users():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            older_users = await cursor.fetchall()
            return older_users

async def fetch_concurrently():
    results = await asyncio.gather(
        asyncfetchusers(),
        asyncfetcholder_users()
    )

    users, older_users = results

    print("All Users:")
    for user in users:
        print(user)

    print("\nUsers Older Than 40:")
    for user in older_users:
        print(user)

# Run the concurrent fetch
asyncio.run(fetch_concurrently())
