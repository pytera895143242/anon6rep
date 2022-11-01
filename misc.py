import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import json


TOKEN = ('5126196895:AAFaKCWX9lI5GPfkg2vW55fJa_U9y8-Lrfo')

memory_storage = MemoryStorage()
bot = Bot(token=TOKEN, parse_mode='html', disable_web_page_preview=True)
dp = Dispatcher(bot,storage=memory_storage)
logging.basicConfig(level=logging.INFO)