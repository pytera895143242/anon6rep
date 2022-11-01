from aiogram import types
from misc import dp,bot
from .sqlit import find_any,cheack_another_chat_id,del_session,del_in_queue
from .sqlit import next_plues_one
from .channel_list import text_pdp,proverka

text_repeat_pdp = """Привет {} 😻

💚Наш бот абсолютно бесплатный, нажми /next для поиска собеседника"""


text_okey = """<b>Собеседник найден 👀</b>
/next — следующий диалог
/stop — закончить общение"""


@dp.message_handler(commands=['next'])
async def cmd_next(message: types.Message):
    if (next_plues_one(message.chat.id) > 10) and (await proverka(message.chat.id) == False):
            await message.answer(text_pdp())
    else:
        """Проверяем есть-ли активный диалог"""

        another_chat_id = cheack_another_chat_id(message.chat.id)
        if another_chat_id == '1': #Нету активного диалога
            if 1 == 2: #Человек не подписался на первые 2 канала
                await message.answer(text=text_repeat_pdp)
            else:
                await bot.send_message(chat_id=message.chat.id, text='🔎 Поиск собеседника ...')
                answer = find_any(chat_id=message.chat.id)
                if len(answer) == 2:
                    await bot.send_message(chat_id=answer[0], text=text_okey)
                    await bot.send_message(chat_id=message.chat.id, text = text_okey)

        else:#Есть активный диалог
            another_id = del_session(message.chat.id)
            await bot.send_message(chat_id=message.chat.id, text='⏭ Собеседник отключен.\n🔎 Поиск нового собеседника ...')
            answer = find_any(chat_id=message.chat.id)
            if len(answer) == 2:
                await bot.send_message(chat_id=answer[0], text=text_okey)
                await bot.send_message(chat_id=message.chat.id, text=text_okey)

            await bot.send_message(chat_id=another_id, text='⏭ Собеседник прервал диалог\nнажмите /next чтобы найти нового')


@dp.message_handler(commands=['stop'])
async def cmd_next(message: types.Message):
    try:
        another_id = del_session(message.chat.id) #Удаляем сессию
        await bot.send_message(chat_id=another_id, text='⏭ Собеседник прервал диалог\nнажмите /next чтобы найти нового')
        await bot.send_message(chat_id=message.chat.id, text='⏭ Собеседник отключен.\nнажмите /next чтобы найти нового')
    except:
        try:
            await bot.send_message(chat_id=message.chat.id,text='⏭ Поиск остановлен.\nНажмите /next чтобы найти нового собеседника')
            del_in_queue(message.chat.id) #Удаляем с очереди, если он туда случайно попал
        except:
            pass

