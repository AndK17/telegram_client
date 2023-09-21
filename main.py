import asyncio
from telethon import TelegramClient, events, types
import os
from dotenv import load_dotenv


class ConsoleTelegramClient(TelegramClient):
    def __init__(self, session_user_id, api_id, api_hash):
        print('Initialization...')
        super().__init__(session_user_id, api_id, api_hash, device_model="Linux 5.15.0", system_version="Ubuntu 20.04.6 LTS")
        self.add_event_handler(self.message_handler, events.NewMessage)
        self.input_msg = 'Input command: '
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
            await self.print_dialogs()
            command = (await asyncio.to_thread(input, self.input_msg)).strip()
            if command.startswith('exit'):
                print('Goodbye!')
                await self.disconnect()
                return
            elif command.startswith('help'):
                print('Command list:')
                print('exit - disconnect and close program')
                print('dialogs - output list of dialogs')
            elif command.startswith('dialogs'):
                await self.print_dialogs()
            else:
                print('Use commands please! Input "help" for more information')
                
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
    except Exception:
        await client.disconnect()


if __name__ == '__main__':
    asyncio.run(main())
    

    
    
    
    
# Dialog(name='Андрей', date=datetime.datetime(2023, 9, 21, 12, 25, 33, tzinfo=datetime.timezone.utc), draft=<telethon.tl.custom.draft.Draft object at 0x000001A52F182020>, message=Message(id=3878, peer_id=PeerUser(user_id=936731598), date=datetime.datetime(2023, 9, 21, 12, 25, 33, tzinfo=datetime.timezone.utc), message='bvb bbvbnbnv', out=True, mentioned=False, media_unread=False, silent=False, post=False, from_scheduled=False, legacy=False, edit_hide=False, pinned=False, noforwards=False, from_id=PeerUser(user_id=5541669523), fwd_from=None, via_bot_id=None, reply_to=None, media=None, reply_markup=None, entities=[], views=None, forwards=None, replies=None, edit_date=None, post_author=None, grouped_id=None, reactions=None, restriction_reason=[], ttl_period=None), entity=User(id=936731598, is_self=False, contact=True, mutual_contact=True, deleted=False, bot=False, bot_chat_history=False, bot_nochats=False, verified=False, restricted=False, min=False, bot_inline_geo=False, support=False, scam=False, apply_min_photo=False, fake=False, bot_attach_menu=False, premium=False, attach_menu_enabled=False, bot_can_edit=False, close_friend=False, stories_hidden=False, stories_unavailable=True, access_hash=-6842146241129659732, first_name='Андрей', last_name=None, username='AndK9', phone='79683851812', photo=UserProfilePhoto(photo_id=4023231578996058029, dc_id=2, has_video=False, personal=False, stripped_thumb=b'\x01\x08\x08\xb6.\x10^\xbfs\x90\x82\x8a(\xa1\x88'), status=UserStatusRecently(), bot_info_version=None, restriction_reason=[], bot_inline_placeholder=None, lang_code=None, emoji_status=None, usernames=[], stories_max_id=None))
# Dialog(name='AliTop', date=datetime.datetime(2022, 11, 12, 17, 33, 15, tzinfo=datetime.timezone.utc), draft=<telethon.tl.custom.draft.Draft object at 0x000001A52F183640>, message=Message(id=40, peer_id=PeerChannel(channel_id=1433452130), date=datetime.datetime(2022, 11, 12, 17, 33, 15, tzinfo=datetime.timezone.utc), message='', out=False, mentioned=False, media_unread=False, silent=False, post=True, from_scheduled=False, legacy=False, edit_hide=False, pinned=False, noforwards=False, from_id=None, fwd_from=None, via_bot_id=None, reply_to=None, media=MessageMediaPhoto(spoiler=False, photo=Photo(id=5440707907801955845, access_hash=-7362549977033530447, file_reference=b'\x02Up\xbeb\x00\x00\x00(e\x0cF\x9e\x12Q\x86Fh\xb9L@\x95\xe2d:\xa6\xea\xbb\xda', date=datetime.datetime(2022, 11, 12, 17, 33, 15, tzinfo=datetime.timezone.utc), sizes=[PhotoStrippedSize(type='i', bytes=b"\x01((\xd9\xac\xfdB\xf1\xe1WXN\xd6P\tlg\xbd_f\n\xa4\x9e\x80f\xb0n\x98\xbc\x1b\xd8\xfc\xd2\x13\xfc\xea[\xb0\xd2'\xb6\xdd#-\xc4\xacY\xcfz\xd0\x8e|\xb8F\xeazU\x08\xbfu\n(\xf4\xa7\t\x0f\x9b\x1b\x0e\xc4\xff\x00*\xce\xef~\x85\xd9lj\xd1@9\x19\xa2\xb63+\xdf1\x16\x92m\xeb\x8cV\x1b\xee+\n\x91\xd0\x9c\xd6\xf5\xd0&\xdd\xf6\xf5\x1c\xfeU\x990\x0e\x11\xd4t<\xfbVrz\x97\x1d\x89\n\xe5\xe3\x1f\xec\xd3\x08\xfb\xa3=\t\xfeT+\xb7\x9d\x17\xcb\xf2\xe0\xf3\x9fjYG\xee\xc9\xfa\x1f\xd2\xb3m\xad\n\xb2\xdc\xd0\xb3%\xadc$\xe4\xe2\x8a[Q\x8bt\x18\xc7\x14V\xebc&\xb5&\xaa\x1a\x94`\x05\x98`\x10\xc3w\xbf\xa5\x14P\xd5\xc6\xb7+4\xd1\x02\x84\xba\x8cv\xcdOo\xe4\xdc\x9d\x81\xb3\xc6x\xf6\xa2\x8a\xce0E9hh\x81\x81\x81E\x14V\xa4\x1f"), PhotoSize(type='m', w=320, h=320, size=19313), PhotoSizeProgressive(type='x', w=640, h=640, sizes=[6312, 15029, 23947, 35107, 66353])], dc_id=2, has_stickers=False, video_sizes=[]), ttl_seconds=None), reply_markup=None, entities=[], views=2, forwards=0, replies=None, edit_date=None, post_author=None, grouped_id=13346195163933498, reactions=None, restriction_reason=[], ttl_period=None), entity=Channel(id=1433452130, title='AliTop', photo=ChatPhoto(photo_id=5447268113864307204, dc_id=2, has_video=False, stripped_thumb=b'\x01\x08\x08\xb3$\xf1\xa4Yh\x08\x18\xee\xab\xfe4QE"\x8f'), date=datetime.datetime(2022, 11, 11, 13, 44, 30, tzinfo=datetime.timezone.utc), creator=False, left=False, broadcast=True, verified=False, megagroup=False, restricted=False, signatures=False, min=False, scam=False, has_link=False, has_geo=False, slowmode_enabled=False, call_active=False, call_not_empty=False, fake=False, gigagroup=False, noforwards=False, join_to_send=False, join_request=False, forum=False, access_hash=7616335605273957544, username=None, restriction_reason=[], admin_rights=None, banned_rights=None, default_banned_rights=None, participants_count=2, usernames=[]))


# stiker NewMessage.Event(original_update=UpdateNewMessage(message=Message(id=3904, peer_id=PeerUser(user_id=936731598), date=datetime.datetime(2023, 9, 21, 15, 15, 35, tzinfo=datetime.timezone.utc), message='', out=False, mentioned=False, media_unread=False, silent=False, post=False, from_scheduled=False, legacy=False, edit_hide=False, pinned=False, noforwards=False, from_id=None, fwd_from=None, via_bot_id=None, reply_to=None, media=MessageMediaDocument(nopremium=False, spoiler=False, document=Document(id=3873772089643106367, access_hash=-5391427025148918754, file_reference=b'\x01\x00\x00\x0f@e\x0c^\x17\xb2\x96@\xa1\x13\x88\xb5P>7?\x84rk\xef\xd5', date=datetime.datetime(2019, 10, 26, 18, 26, 5, tzinfo=datetime.timezone.utc), mime_type='image/webp', size=30618, dc_id=2, attributes=[DocumentAttributeImageSize(w=512, h=512), DocumentAttributeSticker(alt='🎊', stickerset=InputStickerSetID(id=3873772089643106305, access_hash=7333288218265211047), mask=False, mask_coords=None), DocumentAttributeFilename(file_name='sticker.webp')], thumbs=[PhotoPathSize(type='j', bytes=b'\x19\x06\xb3\x02\xe1Y\x06\xe5\x00Y\x06\x80Y\x06\xe1\x19\x06\x99\x06\xef\x19\x06\x99\x06\xe1Y\x06'), PhotoSize(type='m', w=320, h=320, size=11626)], video_thumbs=[]), alt_document=None, ttl_seconds=None), reply_markup=None, entities=[], views=None, forwards=None, replies=None, edit_date=None, post_author=None, grouped_id=None, reactions=None, restriction_reason=[], ttl_period=None), pts=10724, pts_count=1), pattern_match=None, message=Message(id=3904, peer_id=PeerUser(user_id=936731598), date=datetime.datetime(2023, 9, 21, 15, 15, 35, tzinfo=datetime.timezone.utc), message='', out=False, mentioned=False, media_unread=False, silent=False, post=False, from_scheduled=False, legacy=False, edit_hide=False, pinned=False, noforwards=False, from_id=None, fwd_from=None, via_bot_id=None, reply_to=None, media=MessageMediaDocument(nopremium=False, spoiler=False, document=Document(id=3873772089643106367, access_hash=-5391427025148918754, file_reference=b'\x01\x00\x00\x0f@e\x0c^\x17\xb2\x96@\xa1\x13\x88\xb5P>7?\x84rk\xef\xd5', date=datetime.datetime(2019, 10, 26, 18, 26, 5, tzinfo=datetime.timezone.utc), mime_type='image/webp', size=30618, dc_id=2, attributes=[DocumentAttributeImageSize(w=512, h=512), DocumentAttributeSticker(alt='�'', stickerset=InputStickerSetID(id=3873772089643106305, access_hash=7333288218265211047), mask=False, mask_coords=None), DocumentAttributeFilename(file_name='sticker.webp')], thumbs=[PhotoPathSize(type='j', bytes=b'\x19\x06\xb3\x02\xe1Y\x06\xe5\x00Y\x06\x80Y\x06\xe1\x19\x06\x99\x06\xef\x19\x06\x99\x06\xe1Y\x06'), PhotoSize(type='m', w=320, h=320, size=11626)], video_thumbs=[]), alt_document=None, ttl_seconds=None), 
#reply_markup=None, entities=[], views=None, forwards=None, replies=None, edit_date=None, post_author=None, grouped_id=None, reactions=None, restriction_reason=[], ttl_period=None))

#message NewMessage.Event(original_update=UpdateShortMessage(id=3905, user_id=936731598, message='E', pts=10725, pts_count=1, date=datetime.datetime(2023, 9, 21, 15, 16, 3, tzinfo=datetime.timezone.utc), out=False, mentioned=False, media_unread=False, silent=False, fwd_from=None, via_bot_id=None, reply_to=None, entities=[], ttl_period=None), pattern_match=None, message=Message(id=3905, peer_id=PeerUser(user_id=936731598), date=datetime.datetime(2023, 9, 21, 15, 16, 3, tzinfo=datetime.timezone.utc), message='E', out=False, mentioned=False, media_unread=False, silent=False, post=None, from_scheduled=None, legacy=None, edit_hide=None, pinned=None, noforwards=None, from_id=PeerUser(user_id=936731598), fwd_from=None, via_bot_id=None, reply_to=None, media=None, reply_markup=None, entities=[], views=None, forwards=None, replies=None, edit_date=None, post_author=None, grouped_id=None, reactions=None, restriction_reason=[], ttl_period=None))

# photo NewMessage.Event(original_update=UpdateNewMessage(message=Message(id=3906, peer_id=PeerUser(user_id=936731598), date=datetime.datetime(2023, 9, 21, 15, 16, 24, tzinfo=datetime.timezone.utc), message='', out=False, mentioned=False, media_unread=False, silent=False, post=False, from_scheduled=False, legacy=False, edit_hide=False, pinned=False, noforwards=False, from_id=None, fwd_from=None, via_bot_id=None, reply_to=None, media=MessageMediaPhoto(spoiler=False, photo=Photo(id=5215617717019725228, access_hash=-4305640869644404706, file_reference=b'\x01\x00\x00\x0fBe\x0c^H\xfb>\x12ag\xa4\xb5\x18\xab\xae\x8af,\xed}?', date=datetime.datetime(2023, 9, 21, 15, 16, 24, tzinfo=datetime.timezone.utc), sizes=[PhotoStrippedSize(type='i', bytes=b'\x01(\x1e\xd1\xe6\x96\x9a\xd2*\x0c\xb1\x02\xa3\x92uE\xdc\x15\x9b=;R(\x9b\x14\x98\xa4\x8d\x83\xa0lc4\xec\xf3\x8a\x00\xc6I\x18\xbew\xe75a\xe4\x92V\x01\x8e@\xaa\xaac\x078$\xd4\xe1\xf0\x80\xfb\xd0\x04\xb2\\K\x06\x15T\x0e;\xd4-}1<m\xfc\xa8w3\xc5\xcf\xf0\xf4>\xd5Y\xc1\xcf\xdd\xdb@\x98\x02\x87\x82\x05?\xcd\x01\xb6\x9a(\xa6\x03\xd5\x80\x0c\xa7\xa3\x0fL\xd5r\x98=\x7fJ(\xa0\x19'), PhotoSize(type='m', w=238, h=320, size=19361), PhotoSize(type='x', w=596, h=800, size=89193), PhotoSizeProgressive(type='y', w=954, h=1280, sizes=[17329, 43650, 66390, 122508, 171133])], dc_id=2, has_stickers=False, video_sizes=[]), ttl_seconds=None), reply_markup=None, entities=[], views=None, forwards=None, replies=None, edit_date=None, post_author=None, grouped_id=None, reactions=None, restriction_reason=[], ttl_period=None), pts=10726, pts_count=1), pattern_match=None, message=Message(id=3906, peer_id=PeerUser(user_id=936731598), date=datetime.datetime(2023, 9, 21, 15, 16, 24, tzinfo=datetime.timezone.utc), message='', out=False, mentioned=False, media_unread=False, silent=False, post=False, from_scheduled=False, legacy=False, edit_hide=False, pinned=False, noforwards=False, from_id=None, fwd_from=None, via_bot_id=None, reply_to=None, media=MessageMediaPhoto(spoiler=False, photo=Photo(id=5215617717019725228, access_hash=-4305640869644404706, file_reference=b'\x01\x00\x00\x0fBe\x0c^H\xfb>\x12ag\xa4\xb5\x18\xab\xae\x8af,\xed}?', date=datetime.datetime(2023, 9, 21, 15, 16, 24, tzinfo=datetime.timezone.utc), sizes=[PhotoStrippedSize(type='i', bytes=b'\x01(\x1e\xd1\xe6\x96\x9a\xd2*\x0c\xb1\x02\xa3\x92uE\xdc\x15\x9b=;R(\x9b\x14\x98\xa4\x8d\x83\xa0lc4\xec\xf3\x8a\x00\xc6I\x18\xbew\xe75a\xe4\x92V\x01\x8e@\xaa\xaac\x078$\xd4\xe1\xf0\x80\xfb\xd0\x04\xb2\\K\x06\x15T\x0e;\xd4-}1<m\xfc\xa8w3\xc5\xcf\xf0\xf4>\xd5Y\xc1\xcf\xdd\xdb@\x98\x02\x87\x82\x05?\xcd\x01\xb6\x9a(\xa6\x03\xd5\x80\x0c\xa7\xa3\x0fL\xd5r\x98=\x7fJ(\xa0\x19'), PhotoSize(type='m', w=238, h=320, size=19361), PhotoSize(type='x', w=596, h=800, size=89193), PhotoSizeProgressive(type='y', w=954, h=1280, sizes=[17329, 43650, 66390, 122508, 171133])], dc_id=2, has_stickers=False, video_sizes=[]), ttl_seconds=None), reply_markup=None, entities=[], views=None, forwards=None, replies=None, edit_date=None, post_author=None, grouped_id=None, reactions=None, restriction_reason=[], ttl_period=None))