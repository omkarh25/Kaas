from telethon import TelegramClient
import asyncio

class TelegramAdapter:
    def __init__(self, api_id, api_hash, phone_number, channel_id, thread_id):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone_number = phone_number
        self.channel_id = channel_id
        self.thread_id = thread_id
        self.loop = asyncio.get_event_loop()
        self.client = TelegramClient('anon', self.api_id, self.api_hash, loop=self.loop)
        self.is_connected = False

    async def start(self):
        await self.client.start(phone=self.phone_number)
        self.is_connected = True
        print("Client Started")

    async def stop(self):
        if self.is_connected:
            await self.client.disconnect()
            self.is_connected = False
            print("Client Stopped")

    async def ensure_connected(self):
        if not self.is_connected:
            await self.start()

    async def send_message(self, message):
        await self.ensure_connected()
        if self.channel_id is None:
            raise ValueError("Channel ID is not set. Please set a channel first.")
        await self.client.send_message(self.channel_id, message)

    async def get_messages(self, limit=10):
        await self.ensure_connected()
        if self.channel_id is None:
            return []
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

    def set_channel(self, channel_id):
        self.channel_id = channel_id

    async def get_dialogs(self):
        await self.ensure_connected()
        dialogs = await self.client.get_dialogs()
        return [(d.id, d.name) for d in dialogs if d.is_channel]

    def __del__(self):
        if hasattr(self, 'loop') and self.is_connected:
            self.loop.run_until_complete(self.stop())
