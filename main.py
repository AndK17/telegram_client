import asyncio
from telethon import TelegramClient, events, types
import os
from dotenv import load_dotenv
from PIL import Image

class ConsoleTelegramClient(TelegramClient):
    def __init__(self, session_user_id, api_id, api_hash, page_size=15):
        print('Initialization...')
        super().__init__(session_user_id, api_id, api_hash, device_model="Linux 5.15.0", system_version="Ubuntu 20.04.6 LTS")
        
        self.page_size = page_size
        self.input_msg = 'Input command or dialog id: '
        
        self.add_event_handler(self.message_handler, events.NewMessage(incoming=True))
        self.add_event_handler(self.update_dialogs_list, events.ChatAction)
        
        if not os.path.exists('download'):
            os.mkdir('download')
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
        
            
    async def print_main_menu(self):
        print('---------------------------------')
        print('Command list:')
        print('/np - next page of dialogs')
        print('/pp - previous page of dialogs')
        print('"chat id" - open chat by id')
        print('/e - disconnect and close program')
        print('/log_out - log_out your account')
        print('/h - command list')
        print('---------------------------------')
        
    
    async def print_chat_menu(self):
        print('---------------------------------')
        print('Command list:')
        print('/p "photo id" - open photo by id')
        print('/sf "file name" - send file from /download by name. Example: "/sf hello.jpg"')
        print('/b - go to dialogs list')
        print('/e - disconnect and close program')
        print('/h - command list')
        print('---------------------------------')
        
        
    async def run(self):
        await self.update_dialogs_list()
        dialog_num = None
        dialogs_page = 0
        while True:
            await self.print_main_menu()
            while dialog_num == None:
                await self.print_dialogs(dialogs_page)
                command = (await asyncio.to_thread(input, self.input_msg)).strip()
                if command.startswith('/e'):
                    await self.disconnect()
                    return
                elif command.startswith('/h'):
                    await self.print_main_menu()
                elif command.isdigit():
                    dialog_num = int(command)
                elif command.startswith('/log_out'):
                    await self.log_out()
                    return
                elif command.startswith('/np'):
                    dialogs_num = (len(self.dialogs_list)+self.page_size-1)//self.page_size - 1
                    if dialogs_page < dialogs_num:
                        dialogs_page += 1
                elif command.startswith('/pp'):
                    if dialogs_page > 0:
                        dialogs_page -= 1
                else:
                    print('Use commands please! Input "help" for more information')
                    
                await asyncio.sleep(0.1)
            
            
            
            dialog = self.dialogs_list[dialog_num]
            entity = dialog.entity
            await self.print_chat_menu()
            print(f'Dialog with {dialog.title}')
            await self.print_messages(entity, dialog)
                
            while dialog_num != None:
                command = (await asyncio.to_thread(input, 'Input message or command: ')).strip()
                if command.startswith('/e'):
                    await self.disconnect()
                    return
                elif command.startswith('/b'):
                    dialog_num = None
                elif command.startswith('/h'):
                    await self.print_chat_menu()
                elif command.startswith('/p'):
                    img_path = f'download/{command.split()[1]}.jpg'
                    if os.path.exists(img_path):
                        Image.open(img_path).show()
                    else:
                        print('incorrect image id')
                elif command.startswith('/sf'):
                    img_path = f'download/{command.split()[1]}'
                    if os.path.exists(img_path):
                        await self.send_file(entity, img_path)
                    else:
                        print('incorrect image name')
                else:
                    await self.send_message(entity, command)
                    
                await asyncio.sleep(0.1)
            
    
    async def print_messages(self, entity, dialog):
        for msg in [i async for i in self.iter_messages(entity, limit=self.page_size)][::-1]:
            if msg.from_id and msg.from_id.user_id == self.id:
                sender = 'me'
            else:
                sender = dialog.title
            print(f'{sender}[{msg.date.strftime("%Y-%m-%d %H:%M")}]: ', await self.get_message(msg))
    
    
    async def print_dialogs(self, dialogs_page):
        dialogs = self.dialogs_list
        for i, dialog in enumerate(dialogs[self.page_size*dialogs_page:self.page_size*(dialogs_page+1)]):
            msg = await self.get_message(dialog.message)
            title = dialog.title
            print(f'{self.page_size*dialogs_page+i}. {title}: {msg}')

    
    async def get_message(self, message):
        msg = ''
        if message.message:
            msg += message.message.split('\n')[0]
        if message.media:
            if type(message.media) == types.MessageMediaPhoto:
                if not os.path.exists(f'download/{message.media.photo.id}.jpg'):
                    await self.download_media(message, f'download/{message.media.photo.id}.jpg')
                if msg:
                    msg += f' *photo({message.media.photo.id})*'
                else:
                    msg += f'*photo({message.media.photo.id})*'
            else:
                if msg:
                    msg += ' *anower media*'
                else:
                    msg += '*anower media*'
        if type(message) == types.MessageService:
            msg = '*service meassage*'
        if msg == '':
            print(type(message), message)
        return msg
    
    
    async def get_name_from_event(self, event):
        chat = await event.get_chat()
        name = ''
        if type(chat) == types.User:
            if chat.first_name:
                name += chat.first_name
            if chat.last_name:
                name += chat.last_name
            if name == '':
                name = chat.username
        else:
            name = chat.title
        return name
    
    
    async def message_handler(self, event):
        name = await self.get_name_from_event(event)
        msg = await self.get_message(event.message)
        print(f'\n[New messange] {name}: {msg}\nKeep input: ', end='')
        
    
    async def update_dialogs_list(self, event=None):
        self.dialogs_list = await self.get_dialogs()
        
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
    print('Goodbye!')


if __name__ == '__main__':
    asyncio.run(main())