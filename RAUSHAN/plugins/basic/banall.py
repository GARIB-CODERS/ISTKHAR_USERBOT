from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio

# Define your Pyrogram client instance
app_pyrogram = Client("my_bot")

async def ban_member(client, chat_id, user_id):
    try:
        await client.ban_chat_member(chat_id=chat_id, user_id=user_id)
        print(f"Kicked {user_id} from {chat_id}")
    except Exception as e:
        print(f"Failed to kick {user_id}: {e}")
        if "Flood Wait" in str(e):
            # Extract wait time from the exception message
            wait_time = int(str(e).split(" ")[-1])  # Adjust based on actual message
            print(f"Waiting for {wait_time} seconds due to flood wait...")
            await asyncio.sleep(wait_time)

@Client.on_message(filters.command(["banall"], ".") & filters.me)
async def banall_command(client, message: Message):
    print(f"Getting members from {message.chat.id}")
    members = [member.user.id async for member in client.get_chat_members(message.chat.id)]

    for user_id in members:
        await ban_member(client, message.chat.id, user_id)
        await asyncio.sleep(1)  # Wait for 1 second between bans to avoid Flood Wait

    print("Process completed")

async def main():
    await app_pyrogram.start()
    await app_pyrogram.idle()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError as e:
        print(f"Error: {e}")
