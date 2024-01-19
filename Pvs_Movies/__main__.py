from Pvs_Movies import app
from pyrogram import Client, idle
import asyncio

async def main():
    try:
        await app.start()
        print("[Bot] - Movies Bot Started")
    except Exception as e:
        print(f"{e}")
    await idle()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
