from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp
from utils.misc import rate_limit
from filters import IsPrivate

@rate_limit(5, 'help')
@dp.message_handler(CommandHelp(), IsPrivate())
async def bot_help(message: types.Message):
    text = [
        'Список команд: ',
        '/start - Начать диалог',
        '/me - Отобразить информацию о себе',
        '/help - Получить справку'
    ]
    await message.answer('\n'.join(text))
