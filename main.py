import asyncio
from telethon.sync import TelegramClient
import os
from dotenv import load_dotenv


class ConsoleTelegramClient(TelegramClient):
    def __init__(self, session_user_id, api_id, api_hash):
        print('Initialization...')
        super().__init__(session_user_id, api_id, api_hash, device_model="Linux 5.15.0", system_version="Ubuntu 20.04.6 LTS")
        print('Initialization complited')
        

    async def login(self):
        print('Connecting to Telegram servers...')
        try:
            await self.connect()
        except IOError:
            print('Initial connection failed. Retrying...')
            await self.connect()
        print('Connect successfully')
        
        if not await self.is_user_authorized():
            await self.start()
            

    async def run(self):
        while True:
            command = input('Input command: ').strip()
            if command.startswith('exit'):
                print('Goodbye!')
                await self.disconnect()
                return
            elif command.startswith('test'):
                await self.send_message('me', 'Hello, myself!')
            elif command.startswith('help'):
                print('Command list:')
                print('exit - disconnect and close program')
            else:
                print('Use commands please! Input "help" for more information')
        

async def main():
    load_dotenv()
    session_name = os.getenv('session_name')
    api_id = os.getenv('api_id')
    api_hash = os.getenv('api_hash')
    client = ConsoleTelegramClient(session_name, api_id, api_hash)
    await client.login()
    try:
        await client.run()
    except Exception:
        await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())