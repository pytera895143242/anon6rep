from .sqlit import info_members,cheak_traf,obnovatrafika1,obnovatrafika2,obnovatrafika3,obnovatrafika4
from aiogram import types
from misc import dp, bot
from .channel_list import obnovlenie
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class reg_trafik(StatesGroup):
    traf1 = State()
    traf2 = State()

class reg_trafik2(StatesGroup):
    traf1 = State()
    traf2 = State()

class reg_trafik3(StatesGroup):
    traf1 = State()
    traf2 = State()

class reg_trafik4(StatesGroup):
    traf1 = State()
    traf2 = State()

# НАСТРОЙКА ТРАФИКА
@dp.callback_query_handler(text='settings')
async def baza12(call: types.callback_query):
    markup_traf = types.InlineKeyboardMarkup()
    bat_a = types.InlineKeyboardButton(text='ИЗМЕНИТЬ 1 КАНАЛ', callback_data='change_trafik')
    bat_a2 = types.InlineKeyboardButton(text='ИЗМЕНИТЬ 2 КАНАЛ', callback_data='change_trafik2')
    bat_a3 = types.InlineKeyboardButton(text='ИЗМЕНИТЬ 3 КАНАЛ', callback_data='change_trafik3')
    bat_a4 = types.InlineKeyboardButton(text='ИЗМЕНИТЬ 4 КАНАЛ', callback_data='change_trafik4')


    bat_b = types.InlineKeyboardButton(text='ИЗМЕНИТЬ ПОСЛЕДНЮЮ ССЫЛКУ⚙️', callback_data='change_link')
    bat_c = types.InlineKeyboardButton(text='ЗАКРЫТЬ', callback_data='otemena')

    markup_traf.add(bat_a)
    markup_traf.add(bat_a2)
    markup_traf.add(bat_a3)

    markup_traf.add(bat_c)

    list = cheak_traf()
    await bot.send_message(call.message.chat.id, text=f'Список активных каналов на данный момент:\n\n'
                                                      f'1. {list[0]}\n'
                                                      f'2. {list[1]}\n'
                                                      f'3. {list[2]}\n'
                                                      f'Для изменения жми кнопку',parse_mode='html',reply_markup=markup_traf,disable_web_page_preview=True)
    await bot.answer_callback_query(callback_query_id=call.id)


@dp.callback_query_handler(text='change_trafik') # Изменение каналов, на которые нужно подписаться
async def baza12342(call: types.callback_query):
    markup = types.InlineKeyboardMarkup()
    bat_a = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
    markup.add(bat_a)

    await bot.send_message(call.message.chat.id, text='Отправь ссылку на новый, первый по счету канал\n',parse_mode='html',reply_markup=markup)
    await reg_trafik.traf1.set()
    await bot.answer_callback_query(callback_query_id=call.id)

@dp.message_handler(state=reg_trafik.traf1, content_types='text')
async def traf_obnovlenie1(message: types.Message, state: FSMContext):
    await state.update_data(link_one = message.text)
    await bot.send_message(chat_id=message.chat.id, text=f'Теперь перешли мне любой пост из этого канала ({message.text})')
    await reg_trafik.traf2.set()



@dp.message_handler(state=reg_trafik.traf2, content_types=['text','photo','video'])
async def traf_obnovlenie(message: types.Message, state: FSMContext):
    link = await state.get_data()

    link_one = link['link_one'] #Ссылка на канал
    id_channel1 = (message.forward_from_chat.id) #ID канала

    try:
        obnovatrafika1(link_one, id_channel1) # Внесение новых каналов в базу данных
        obnovlenie()

        await bot.send_message(chat_id=message.chat.id,text='Обновление успешно')
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        except:
            pass
        await state.finish()

    except:
        await bot.send_message(chat_id=message.chat.id,text='Ошибка! Вы сделали что-то неправильное. Необходимо снова зайти в админ панель и выбрать нужный пункт')
        await state.finish()


# РЕДАКТИРУЕМ ВТОРОЙ КАНАЛ
@dp.callback_query_handler(text='change_trafik2') # Изменение каналов, на которые нужно подписаться
async def baza12342_2(call: types.callback_query):
    markup = types.InlineKeyboardMarkup()
    bat_a = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
    markup.add(bat_a)

    await bot.send_message(call.message.chat.id, text='Отправь ссылку на новый, второй по счету канал\n',parse_mode='html',reply_markup=markup)
    await reg_trafik2.traf1.set()
    await bot.answer_callback_query(callback_query_id=call.id)


@dp.message_handler(state=reg_trafik2.traf1, content_types='text')
async def traf_obnovlenie2(message: types.Message, state: FSMContext):
    await state.update_data(link_one = message.text)
    await bot.send_message(chat_id=message.chat.id, text=f'Теперь перешли мне любой пост из этого канала ({message.text})')
    await reg_trafik2.traf2.set()


@dp.message_handler(state=reg_trafik2.traf2, content_types=['text','photo','video'])
async def traf_obnovlenie_2(message: types.Message, state: FSMContext):
    link = await state.get_data()

    link_one = link['link_one'] #Ссылка на канал
    id_channel2 = (message.forward_from_chat.id) #ID канала

    try:
        obnovatrafika2(link_one, id_channel2) # Внесение 2-го новых каналов в базу данных
        obnovlenie()

        await bot.send_message(chat_id=message.chat.id,text='Обновление успешно')
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        except:
            pass
        await state.finish()

    except:
        await bot.send_message(chat_id=message.chat.id,text='Ошибка! Вы сделали что-то неправильное. Необходимо снова зайти в админ панель и выбрать нужный пункт')
        await state.finish()


# РЕДАКТИРУЕМ ТРЕТИЙ КАНАЛ
@dp.callback_query_handler(text='change_trafik3') # Изменение каналов, на которые нужно подписаться
async def baza12342_3(call: types.callback_query):
    markup = types.InlineKeyboardMarkup()
    bat_a = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
    markup.add(bat_a)

    await bot.send_message(call.message.chat.id, text='Отправь ссылку на новый, третий по счету канал\n',parse_mode='html',reply_markup=markup)
    await reg_trafik3.traf1.set()
    await bot.answer_callback_query(callback_query_id=call.id)

@dp.message_handler(state=reg_trafik3.traf1, content_types='text')
async def traf_obnovlenie3(message: types.Message, state: FSMContext):
    await state.update_data(link_one = message.text)
    await bot.send_message(chat_id=message.chat.id, text=f'Теперь перешли мне любой пост из этого канала ({message.text})')
    await reg_trafik3.traf2.set()


@dp.message_handler(state=reg_trafik3.traf2, content_types=['text','photo','video'])
async def traf_obnovlenie_3(message: types.Message, state: FSMContext):
    link = await state.get_data()

    link_one = link['link_one'] #Ссылка на канал
    id_channel3 = (message.forward_from_chat.id) #ID канала

    try:
        obnovatrafika3(link_one, id_channel3) # Внесение 3-го новых каналов в базу данных
        obnovlenie()

        await bot.send_message(chat_id=message.chat.id,text='Обновление успешно')
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        except:
            pass
        await state.finish()

    except:
        await bot.send_message(chat_id=message.chat.id,text='Ошибка! Вы сделали что-то неправильное. Необходимо снова зайти в админ панель и выбрать нужный пункт')
        await state.finish()

# РЕДАКТИРУЕМ ЧЕТВЕРТЫЙ КАНАЛ
@dp.callback_query_handler(text='change_trafik4') # Изменение каналов, на которые нужно подписаться
async def baza12342_4(call: types.callback_query):
    markup = types.InlineKeyboardMarkup()
    bat_a = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
    markup.add(bat_a)

    await bot.send_message(call.message.chat.id, text='Отправь ссылку на новый, четвертый по счету канал\n',parse_mode='html',reply_markup=markup)
    await reg_trafik4.traf1.set()
    await bot.answer_callback_query(callback_query_id=call.id)


@dp.message_handler(state=reg_trafik4.traf1, content_types='text')
async def traf_obnovlenie44(message: types.Message, state: FSMContext):
    await state.update_data(link_one = message.text)
    await bot.send_message(chat_id=message.chat.id, text=f'Теперь перешли мне любой пост из этого канала ({message.text})')
    await reg_trafik4.traf2.set()


@dp.message_handler(state=reg_trafik4.traf2, content_types=['text','photo','video'])
async def traf_obnovlenie_4(message: types.Message, state: FSMContext):
    link = await state.get_data()

    link_one = link['link_one'] #Ссылка на канал
    id_channel4 = (message.forward_from_chat.id) #ID канала

    try:
        obnovatrafika4(link_one, id_channel4) # Внесение 2-го новых каналов в базу данных
        obnovlenie()

        await bot.send_message(chat_id=message.chat.id,text='Обновление успешно')
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        except:
            pass
        await state.finish()

    except:
        await bot.send_message(chat_id=message.chat.id,text='Ошибка! Вы сделали что-то неправильное. Необходимо снова зайти в админ панель и выбрать нужный пункт')
        await state.finish()
#Конец обновлялки каналов