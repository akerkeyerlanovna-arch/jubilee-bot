import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())
class GuestForm(StatesGroup):
    waiting_for_name = State()
    waiting_for_photo = State()
@dp.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    await message.answer(
    "Добро пожаловать 🤍\n\n"
    "Совсем скоро состоится юбилей,\n"
    "и мы собираем фотографии гостей,\n"
    "которые станут частью этого особенного вечера.\n\n"
    "Пожалуйста, напишите ваше имя и имя вашей супруги✨.\n\n"
    "(Пример: Жанат-Гульсим)"
)
    await state.set_state(GuestForm.waiting_for_name)
@dp.message(GuestForm.waiting_for_name)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(
    f"Спасибо, {message.text} 🤍\n\n"
    "Теперь отправьте ваше совместное фото 📸"
)
    await state.set_state(GuestForm.waiting_for_photo)
@dp.message(GuestForm.waiting_for_photo)
async def get_photo(message: types.Message, state: FSMContext):
    if not message.photo:
        await message.answer("Пожалуйста, отправьте именно фото 📸")
        return
    data = await state.get_data()
    name = data.get("name", "Без имени")
    photo = message.photo[-1]
    await bot.send_message(
        ADMIN_ID,
        f"Новый гость 👇\n\nИмя: {name}"
    )
    await bot.send_photo(
        ADMIN_ID,
        photo.file_id,
        caption=f"Фото от: {name}"
    )
    await bot.send_photo(
    CHANNEL_ID,
    photo.file_id,
    caption=f"Гость: {name}"
)
    await message.answer(
        "Спасибо 🤍\n\n"
        "Ваше фото сохранено ✨"
    )
    await state.clear()
async def main():
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())
