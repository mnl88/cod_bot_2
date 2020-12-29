from loader import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from filters import IsPrivate
import logging


logger = logging.getLogger(__name__)


# Прервать любой их хэндлеров
@dp.message_handler(IsPrivate(), state='*', commands=['cancel', 'отмена'])
@dp.message_handler(IsPrivate(), Text(equals=['cancel', 'отмена'], ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Прерывание любого их хэндлеров
    """
    logger.info(f'Пользователь {message.from_user.full_name} (ID: {message.from_user.id}) нажал команду ОТМЕНА')
    await state.finish()
    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())

