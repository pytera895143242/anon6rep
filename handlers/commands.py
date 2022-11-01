from aiogram import types
from misc import dp,bot
import sqlite3
from .sqlit import reg_bd,reg_in_users,cheak_traf,cheak_chat_id
reg_bd()

list_channel = cheak_traf()
name_channel_1 = list_channel[0]
name_channel_2 = list_channel[1]
name_channel_3 = list_channel[2]

def obnovlenie():
    global name_channel_1,name_channel_2,name_channel_3
    list_channel = cheak_traf()
    name_channel_1 = list_channel[0]
    name_channel_2 = list_channel[1]
    name_channel_3 = list_channel[2]


def markup_find():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bat1 = types.InlineKeyboardButton(text="🔎 ПАРЕНЬ")
    bat2 = types.InlineKeyboardButton(text="🔎 ДЕВУШКА")
    bat3 = types.InlineKeyboardButton(text="🎲 СЛУЧАЙНЫ ПОЛ 🎲")
    markup.add(bat1,bat2)
    markup.add(bat3)
    return markup

def markup_gender():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bat1 = types.InlineKeyboardButton(text="🚹 Я парень")
    bat2 = types.InlineKeyboardButton(text="🚺 Я девушка")
    markup.add(bat1,bat2)
    return markup

def markup_stop():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bat1 = types.InlineKeyboardButton(text="❌ Остановить поиск")
    markup.add(bat1)
    return markup

def markup_stop_dialog():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bat1 = types.InlineKeyboardButton(text="❌ Остановить диалог")
    markup.add(bat1)
    return markup

def markup_channels():
    markup = types.InlineKeyboardMarkup()
    channel1 = types.InlineKeyboardButton(text='1️⃣ Первый канал', url=f'{name_channel_1}')
    channel2 = types.InlineKeyboardButton(text='2️⃣ Второй канал', url=f'{name_channel_2}')
    channel3 = types.InlineKeyboardButton(text='3️⃣ Третий канал', url=f'{name_channel_3}')
    bat_cheack = types.InlineKeyboardButton(text='Проверить подписку 🔐', callback_data='check')

    markup.add(channel1)
    markup.add(channel2)
    markup.add(channel3)
    markup.add(bat_cheack)

    return markup


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    try:
        first_name = message.from_user.first_name
    except:
        first_name = 'anonim'
    if message.text[6:] == '':
        reg_in_users(chat_id=message.chat.id,first_name=first_name,ref= '1')
    else:
        reg_in_users(chat_id=message.chat.id, first_name=first_name, ref=message.text[6:])

    await message.answer(text=f"""<b>Привет {message.from_user.first_name} 😻

💚Наш бот абсолютно бесплатный, но работает только после подписки на каналы спонсоров 👇</b>""",reply_markup=markup_channels())


@dp.callback_query_handler(text_startswith='check')  # Нажал кнопку Я ПОДПИСАЛСЯ. ДЕЛАЕМ ПРОВЕРКУ
async def check(call: types.callback_query):
    id_list = cheak_chat_id()

    try:
        proverka1 = (await bot.get_chat_member(chat_id=id_list[0], user_id=call.message.chat.id)).status
    except:
        proverka1 = 'member'

    try:
        proverka2 = (await bot.get_chat_member(chat_id=id_list[1], user_id=call.message.chat.id)).status
    except:
        proverka2 = 'member'

    try:
        proverka3 = (await bot.get_chat_member(chat_id=id_list[2], user_id=call.message.chat.id)).status
    except:
        proverka3 = 'member'


    if (proverka1 != 'left' and proverka2 != 'left' and proverka3 != 'left'):
        await bot.send_message(chat_id=call.message.chat.id,
                               text=f'Спасибо за подписку ❤️\n'
                                    f'<b>Теперь укажите свой пол 👇</b>',
                               reply_markup=markup_gender())


    else:
        await call.message.answer(text=f"""<b>Вы не подписались на каналы спонсоров ❌
        
Подпишись и повтори попытку 👇</b>""",reply_markup=markup_channels())


    await bot.answer_callback_query(callback_query_id = call.id)