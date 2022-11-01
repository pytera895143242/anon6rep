from aiogram import types
from misc import dp,bot
from .sqlit import cheack_another_chat_id,reg_gender,cheack_session
from .sqlit import next_plues_one
from .channel_list import text_pdp,proverka


from aiogram.dispatcher.filters.state import State, StatesGroup

content_channel = '-1001589342789'
link = 'https://www1.tracklyfast.com/click?pid=44953&offer_id=25'


class progrev(StatesGroup):
    step1 = State()
    step2 = State()
    step3 = State()
    step4 = State()
    step5 = State()
    step_ignor = State()


text_hello = """ Спасибо, что указали свой пол ❤️
Напиши /next чтобы начать поиск собеседника"""

@dp.message_handler(content_types=['text','photo','voice','video','video_note'])
async def all_other_messages(message: types.message):
    if message.chat.type == 'private':
        # ЧЕЛОВЕК УКАЗАЛ СВОЙ ПОЛ 👇👇👇
        if message.text == '🚹 Я парень' and cheack_session(message.chat.id) == '1':
            await bot.send_message(chat_id=message.chat.id, text=text_hello, reply_markup=types.ReplyKeyboardRemove())
            s = reg_gender(chat_id=message.chat.id,first_name= message.from_user.first_name, gender='man')

        elif message.text == '🚺 Я девушка' and cheack_session(message.chat.id) == '1':
            await bot.send_message(chat_id=message.chat.id, text=text_hello, reply_markup=types.ReplyKeyboardRemove())
            s = reg_gender(chat_id=message.chat.id, first_name=message.from_user.first_name, gender='woman')


        else:
            if (next_plues_one(message.chat.id, 0) > 5) and (await proverka(message.chat.id) == False):
                await message.answer(text_pdp())
            else:
                """Проверяем есть ли у человека действующая сессия"""
                an_id = cheack_another_chat_id(message.chat.id)
                if an_id == '1':
                    await bot.send_message(text = 'У вас нет активного чата.\nНажмите /next чтобы найти нового',chat_id=message.chat.id,reply_markup = types.ReplyKeyboardRemove())
                else:
                    if (('t.me' in message.text) or ('https' in message.text) or ('http' in message.text) or ('@' in message.text)):
                        await bot.send_message(chat_id=message.chat.id,text= f'Ваше сообщение: <code>{message.text}</code>\n'
                                                                             f'<b>Не было отправлено. Не используй в боте сcылки и <code>символ "@"</code></b>',parse_mode='html')
                    else:
                        await bot.copy_message(chat_id=an_id, from_chat_id=message.chat.id,message_id=message.message_id)