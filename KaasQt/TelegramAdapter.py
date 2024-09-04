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

    async def messages_to_markdown(self, channel_id, output_file, limit=10, thread_id=None):
        messages = await self.get_messages(channel_id, limit, thread_id)
        with open(output_file, 'w') as f:
            f.write("# Din\n\n")
            for msg in messages:
                sender = await msg.get_sender()
                sender_name = sender.first_name if sender else "Unknown"
                f.write(f"- [{msg.date}] {sender_name}: {msg.text}\n")
