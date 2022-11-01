from .sqlit import cheak_traf
from aiogram import types
from misc import dp,bot
from .sqlit import cheak_chat_id

list_channel = cheak_traf()
name_channel_1 = list_channel[0]
name_channel_2 = list_channel[1]
name_channel_3 = list_channel[2]
# name_channel_4 = list_channel[3]

def obnovlenie():
    global name_channel_1,name_channel_2,name_channel_3,name_channel_4
    list_channel = cheak_traf()
    name_channel_1 = list_channel[0]
    name_channel_2 = list_channel[1]
    name_channel_3 = list_channel[2]
    # name_channel_4 = list_channel[3]


def text_pdp():
    text_pdp = f"""<b>Наш чат абсолютно бесплатный, но вам нужно быть подписанными на каналы нашего спонсора</b>
    
<b>Канал 1</b> - {name_channel_1[8:]}
<b>Канал 2</b> - {name_channel_2[8:]}
<b>Канал 3</b> - {name_channel_3[8:]}    
    
<b>Подпишитесь на ВСЕ каналы и нажмите /next для поиска собеседника</b>"""

    return text_pdp



async def proverka(i):
    id_list = cheak_chat_id()
    try: proverka1 = (await bot.get_chat_member(chat_id=id_list[0], user_id= i)).status
    except: proverka1 = 'member'

    try: proverka2 = (await bot.get_chat_member(chat_id=id_list[1], user_id=i)).status
    except: proverka2 = 'member'

    try: proverka3 = (await bot.get_chat_member(chat_id=id_list[2], user_id=i)).status
    except: proverka3 = 'member'

    if (proverka1 == 'member' and proverka2 == 'member' and proverka3 == 'member') or proverka1 == 'creator' or proverka2 == 'creator' or proverka3 == 'creator':
        return True
    else:
        return False



obnovlenie()