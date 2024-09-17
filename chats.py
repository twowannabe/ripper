from telethon.tl.types import PeerChannel, PeerChat

async def get_chat_id():
    async for dialog in client.iter_dialogs():
        if isinstance(dialog.entity, PeerChannel) or isinstance(dialog.entity, PeerChat):
            print(f'Название: {dialog.name}, ID: {dialog.id}')

with client:
    client.loop.run_until_complete(get_chat_id())
