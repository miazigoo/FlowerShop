
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

API_TOKEN = '6264686135:AAFWbJer6vDcPUdnRcafKE0r7cCstGbhO5k'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    itembtn1 = types.KeyboardButton('день рождения')
    itembtn2 = types.KeyboardButton('свадьба')
    markup.add(itembtn1, itembtn2)
    await message.answer('К какому событию готовимся? Выберите один из вариантов, либо укажите свой', reply_markup=markup)

@dp.message_handler()
async def process_message(message: types.Message):
    if message.text == 'день рождения' or message.text == 'свадьба':
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        itembtn1 = types.KeyboardButton('500')
        itembtn2 = types.KeyboardButton('1000')
        itembtn3 = types.KeyboardButton('5000')
        itembtn4 = types.KeyboardButton('не важно')
        markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
        await message.answer('На какую сумму рассчитываете?', reply_markup=markup)
    elif message.text.isdigit() or message.text == 'не важно':
        # Здесь вы можете добавить логику для выбора и отправки фото букета
        await bot.send_photo(chat_id=message.chat.id, photo=open('path_to_photo.jpg', 'rb'),
                             caption='Описание букета\nСтоимость: 1000 руб.\n\n'
                                     'Хотите что-то более специальное? Подберите другой букет из нашей коллекции или закажите личную консультацию')
        markup = types.InlineKeyboardMarkup()
        itembtn1 = types.InlineKeyboardButton('заказать этот букет', callback_data='order_bouquet')
        markup.add(itembtn1)
        await message.answer('Выберите действие:', reply_markup=markup)
    elif message.text == 'заказать консультацию':
        # Здесь вы можете добавить логику для обработки заказа консультации
        await message.answer('Укажите номер телефона, и наш флорист перезвонит вам в течение 20 минут')
    elif message.text == 'посмотреть всю коллекцию':
        # Здесь вы можете добавить логику для показа следующего фото букета
        await bot.send_photo(chat_id=message.chat.id, photo=open('path_to_photo.jpg', 'rb'),
                             caption='Описание букета\nСтоимость: 2000 руб.\n\n'
                                     'Хотите что-то более специальное? Подберите другой букет из нашей коллекции или закажите личную консультацию')
        markup = types.InlineKeyboardMarkup()
        itembtn1 = types.InlineKeyboardButton('заказать этот букет', callback_data='order_bouquet')
        markup.add(itembtn1)
        await message.answer('Выберите действие:', reply_markup=markup)

@dp.callback_query_handler(lambda call: call.data == 'order_bouquet')
async def process_callback(call: types.CallbackQuery):
    # Здесь вы можете добавить логику для обработки заказа букета
    await bot.send_message(chat_id='YOUR_COURIER_ID', text='Заказ букета:\n\nКлиент: {}\nАдрес: {}\nВремя доставки: {}'.format(call.message.chat.first_name, 'адрес', 'время'))

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)