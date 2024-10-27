from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio

# Define your Pyrogram client instance
app_pyrogram = Client("my_bot")

async def ban_member(client, chat_id, user_id):
    while True:
        try:
            await client.ban_chat_member(chat_id=chat_id, user_id=user_id)
            print(f"Kicked {user_id} from {chat_id}")
            break  # Exit the loop if successful
        except Exception as e:
            print(f"Failed to kick {user_id}: {e}")
            if "Flood Wait" in str(e):
                # Extract wait time from the exception message
                wait_time = int(str(e).split(" ")[-1])  # Adjust as per actual message
                print(f"Waiting for {wait_time} seconds due to flood wait...")
                await asyncio.sleep(wait_time)  # Wait before retrying
            else:
                break  # Exit on other errors

@Client.on_message(filters.command(["banall"], ".") & filters.me)
async def banall_command(client, message: Message):
    print(f"Getting members from {message.chat.id}")
    async for member in client.get_chat_members(message.chat.id):
        await ban_member(client, message.chat.id, member.user.id)
    print("Process completed")

async def main():
    await app_pyrogram.start()
    await app_pyrogram.idle()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError as e:
        print(f"Error: {e}")
