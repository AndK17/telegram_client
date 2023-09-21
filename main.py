import asyncio
from telethon import TelegramClient, events, types
import os
from dotenv import load_dotenv


class ConsoleTelegramClient(TelegramClient):
    def __init__(self, session_user_id, api_id, api_hash):
        print('Initialization...')
        super().__init__(session_user_id, api_id, api_hash, device_model="Linux 5.15.0", system_version="Ubuntu 20.04.6 LTS")
        self.add_event_handler(self.message_handler, events.NewMessage)
        self.input_msg = 'Input command or dialog id: '
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
            
        self.id = (await self.get_me()).id
            

    async def run(self):
        while True:
            dialog_num = None
            while dialog_num == None:
                await self.print_dialogs()
                command = (await asyncio.to_thread(input, self.input_msg)).strip()
                if command.startswith('exit'):
                    print('Goodbye!')
                    await self.disconnect()
                    return
                elif command.startswith('help'):
                    print('Command list:')
                    print('exit - disconnect and close program')
                    print('dialogs - outputs list of dialogs')
                elif command.startswith('dialogs'):
                    await self.print_dialogs()
                elif command.isdigit():
                    dialog_num = int(command)
                else:
                    print('Use commands please! Input "help" for more information')
                    
                await asyncio.sleep(0.1)
            
            
            
            dialog = (await self.get_dialogs())[dialog_num]
            entity = dialog.entity
            print(f'Dialog with {dialog.title}')
            for msg in [i async for i in self.iter_messages(entity, limit=20)][::-1]:
                if msg.from_id and msg.from_id.user_id == self.id:
                    sender = 'me'
                else:
                    sender = dialog.title
                print(f'{sender}[{msg.date.strftime("%Y-%m-%d %H:%M")}]: ', await self.get_message(msg))
                
            while dialog_num != None:
                command = (await asyncio.to_thread(input, 'Input message or command: ')).strip()
                if command.startswith('/exit'):
                    print('Goodbye!')
                    await self.disconnect()
                    return
                elif command.startswith('/back'):
                    dialog_num = None
                elif command.startswith('/help'):
                    print('Command list:')
                    print('/exit - disconnect and close program')
                    print('/back - go to dialogs list')
                else:
                    await self.send_message(entity, command)
                    
                await asyncio.sleep(0.1)
            
    
    async def print_dialogs(self):
        dialogs = await self.get_dialogs()
        for i, dialog in enumerate(dialogs):
            msg = await self.get_message(dialog.message)
            title = dialog.title
            print(f'{i}. {title}: {msg}')

    
    async def get_message(self, message):
        msg = ''
        if message.message:
            msg += message.message.split('\n')[0]
        if message.media:
            if msg:
                msg += ' *media*'
            else:
                msg += '*media*'
        if type(message) == types.MessageService:
            msg = '*service meassage*'
        if msg == '':
            print(type(message), message)
        return msg
    
    
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
        # in message to yourself event.from_id == None
        if event.from_id and event.from_id.user_id != self.id:
            name = await self.get_name_from_event(event)
            msg = await self.get_message(event.message)
            print(f'\n[New messange] {name}: {msg}\n{self.input_msg}', end='')
        
        
async def main():
    load_dotenv()
    session_name = os.getenv('session_name')
    api_id = os.getenv('api_id')
    api_hash = os.getenv('api_hash')
    client = ConsoleTelegramClient(session_name, api_id, api_hash)
    await client.login()
    try:
        await client.run()
    except Exception as e:
        print(e)
        await client.disconnect()


if __name__ == '__main__':
    asyncio.run(main())