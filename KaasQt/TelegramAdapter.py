from telethon import TelegramClient
from telethon.tl.types import InputPeerChannel, PeerChannel
import asyncio
import time

class TelegramAdapter:
    def __init__(self, api_id, api_hash, phone_number):
        self.client = TelegramClient('session_name', api_id, api_hash)
        self.phone_number = phone_number
        self.channel_id = None
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.start())

    async def start(self):
        await self.client.start(phone=self.phone_number)
        print("Client Started")

    async def stop(self):
        await self.client.disconnect()
        print("Client Stopped")

    def send_message(self, message):
        if self.channel_id is None:
            raise ValueError("Channel ID is not set. Please set a channel first.")
        async def _send_message():
            await self.client.send_message(self.channel_id, message)
        self.loop.run_until_complete(_send_message())

    def get_messages(self, limit=10):
        if self.channel_id is None:
            return []
        async def _get_messages():
            messages = []
            async for message in self.client.iter_messages(self.channel_id, limit=limit):
                msg_dict = {
                    'sender': message.sender.first_name if message.sender else "Unknown",
                    'text': message.text
                }
                if message.photo:
                    msg_dict['image'] = await message.download_media()
                if message.audio:
                    msg_dict['audio'] = await message.download_media()
                if message.entities:
                    for entity in message.entities:
                        if hasattr(entity, 'url'):
                            msg_dict['link'] = entity.url
                messages.append(msg_dict)
            return messages
        return self.loop.run_until_complete(_get_messages())

    def set_channel(self, channel_id):
        self.channel_id = channel_id

    def get_dialogs(self):
        async def _get_dialogs():
            dialogs = await self.client.get_dialogs()
            return [(d.id, d.name) for d in dialogs if d.is_channel]
        return self.loop.run_until_complete(_get_dialogs())

    def __del__(self):
        self.loop.run_until_complete(self.stop())

    async def poll_messages(self, callback, interval=300):  # 300 seconds = 5 minutes
        while True:
            messages = self.get_messages()
            if messages:
                callback(messages)
            await asyncio.sleep(interval)

    def start_polling(self, callback):
        async def _start_polling():
            await self.poll_messages(callback)
        self.loop.create_task(_start_polling())
