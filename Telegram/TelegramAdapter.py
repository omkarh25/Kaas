from telethon import TelegramClient
from telethon.tl.types import InputPeerChannel, PeerChannel
import asyncio

class TelegramAdapter:
    def __init__(self, api_id, api_hash, phone_number):
        self.client = TelegramClient('session_name', api_id, api_hash)
        self.phone_number = phone_number

    async def start(self):
        await self.client.start(phone=self.phone_number)
        print("Client Started")

    async def stop(self):
        await self.client.disconnect()
        print("Client Stopped")

    async def send_message(self, channel_id, message, thread_id=None):
        peer_channel = PeerChannel(channel_id)
        if thread_id:
            await self.client.send_message(peer_channel, message, reply_to=thread_id)
        else:
            await self.client.send_message(peer_channel, message)
        print(f"Message sent to channel {channel_id}")

    async def get_messages(self, channel_id, limit=10, thread_id=None):
        peer_channel = PeerChannel(channel_id)
        if thread_id:
            messages = await self.client.get_messages(peer_channel, limit=limit, reply_to=thread_id)
        else:
            messages = await self.client.get_messages(peer_channel, limit=limit)
        return messages

    async def print_messages(self, channel_id, limit=10, thread_id=None):
        messages = await self.get_messages(channel_id, limit, thread_id)
        for msg in messages:
            sender = await msg.get_sender()
            sender_name = sender.first_name if sender else "Unknown"
            print(f"[{msg.id}] {sender_name}: {msg.text}")

async def main():
    # Use your own values from my.telegram.org
    api_id = '22353756'
    api_hash = '351041b3c3951a0a116652896d55d9a2'
    phone_number = '+919902106162'
    message = "what about the pot itself? can you get the rates from kiran and add it as well please?"

    adapter = TelegramAdapter(api_id, api_hash, phone_number)
    await adapter.start()

    try:
        # Example usage
        channel_id = 1677058465  # Replace with your channel ID
        thread_id = 1446  # Replace with your thread ID

        # Send a message to a specific thread
        # await adapter.send_message(channel_id, message, thread_id)

        # Print recent messages from the specific thread in the channel
        await adapter.print_messages(channel_id, limit=10, thread_id=thread_id)

        # Print recent messages from the entire channel
        print("\nMessages from the entire channel:")
        # await adapter.print_messages(channel_id, limit=10)

    finally:
        await adapter.stop()

if __name__ == "__main__":
    asyncio.run(main())
