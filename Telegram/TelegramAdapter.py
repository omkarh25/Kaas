from telethon import TelegramClient
from telethon.tl.types import InputPeerChannel, InputPeerUser, PeerChannel, PeerChat
from telethon.tl.patched import Message
import asyncio
# Use your own values from my.telegram.org
api_id = '22353756'
api_hash = '351041b3c3951a0a116652896d55d9a2'
phone_number = '+919902106162'
channel_id = -1001677058465  # Replace with your channel ID
thread_id = 2984
message = "Nice"

client = TelegramClient('session_name', api_id, api_hash)

# Initialize the client
client = TelegramClient('session_name', api_id, api_hash)

async def main():
    # Start the client
    await client.start(phone=phone_number)
    
    # Create the peer channel object
    peer_channel = PeerChannel(channel_id)
    
    # Send the message to the specific thread in the channel
    await client.send_message(peer_channel, message, reply_to=thread_id)
    print(f"Message sent to thread {thread_id} in the channel")

# Run the client
with client:
    client.loop.run_until_complete(main())
