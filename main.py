import asyncio
from telethon import TelegramClient, events
import os
from dotenv import load_dotenv


class ConsoleTelegramClient(TelegramClient):
    def __init__(self, session_user_id, api_id, api_hash):
        print('Initialization...')
        super().__init__(session_user_id, api_id, api_hash, device_model="Linux 5.15.0", system_version="Ubuntu 20.04.6 LTS")
        self.add_event_handler(self.message_handler, events.NewMessage)
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
            command = (await asyncio.to_thread(input, 'Input command: ')).strip()
            if command.startswith('exit'):
                print('Goodbye!')
                await self.disconnect()
                return
            elif command.startswith('test'):
                await self.send_message('me', 'Hello, myself!')
            elif command.startswith('help'):
                print('Command list:')
                print('exit - disconnect and close program')
                print('dialogs - output list of dialogs')
            elif command.startswith('dialogs'):
                dialogs = await self.get_dialogs()
                for dialog in dialogs:
                    print(f'{dialog.name}: {dialog.message.message}')
            else:
                print('Use commands please! Input "help" for more information')
            await asyncio.sleep(0.1)
    
    async def output_message(self, event):
        if event.media:
            return '*media*'
        else:
            return event.text
    
    async def get_name_from_event(self, event):
        chat = await event.get_chat()
        name = ''
        if chat.first_name:
            name += chat.first_name
        if chat.last_name:
            name += chat.last_name
        if name == '':
            name = chat.username
        return name
    
    
    async def message_handler(self, event):
        print(f'\n[New messange] {await self.get_name_from_event(event)}: {await self.output_message(event)}', '\nInput command: ', end='')
        
        
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