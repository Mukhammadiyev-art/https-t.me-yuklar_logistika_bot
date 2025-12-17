import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from dotenv import load_dotenv

# ===== ENV =====
load_dotenv()

API_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# ===== MENU =====
menu = ReplyKeyboardMarkup(resize_keyboard=True)
menu.add(
    KeyboardButton("📦 Yuk joylash"),
    KeyboardButton("🚛 Mashina joylash")
)

# ===== STATES =====
class LoadForm(StatesGroup):
    route = State()
    info = State()
    phone = State()

class TruckForm(StatesGroup):
    route = State()
    info = State()
    phone = State()

# ===== START =====
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(
        "Assalomu alaykum!\n"
        "Yuk va mashina e’lonlarini joylash uchun tanlang 👇",
        reply_markup=menu
    )

# ===== YUK JOYLASH =====
@dp.message_handler(lambda m: m.text == "📦 Yuk joylash")
async def load_start(message: types.Message):
    await LoadForm.route.set()
    await message.answer("📍 Yo‘nalishni kiriting\nMasalan: Toshkent → Andijon")

@dp.message_handler(state=LoadForm.route)
async def load_route(message: types.Message, state: FSMContext):
    await state.update_data(route=message.text)
    await LoadForm.info.set()
    await message.answer("📦 Yuk ma’lumotlari (tonna, turi, sana)")

@dp.message_handler(state=LoadForm.info)
async def load_info(message: types.Message, state: FSMContext):
    await state.update_data(info=message.text)
    await LoadForm.phone.set()
    await message.answer("📞 Telefon raqamingiz")

@dp.message_handler(state=LoadForm.phone)
async def load_finish(message: types.Message, state: FSMContext):
    data = await state.get_data()
    post = (
        "📦 *YUK BOR*\n\n"
        f"📍 Yo‘nalish: {data['route']}\n"
        f"📦 Yuk: {data['info']}\n"
        f"📞 Aloqa: {message.text}"
    )
    await bot.send_message(CHANNEL_ID, post, parse_mode="Markdown")
    await message.answer("✅ Yuk e’loni kanalga joylandi!", reply_markup=menu)
    await state.finish()

# ===== MASHINA JOYLASH =====
@dp.message_handler(lambda m: m.text == "🚛 Mashina joylash")
async def truck_start(message: types.Message):
    await TruckForm.route.set()
    await message.answer("📍 Yo‘nalishni kiriting\nMasalan: Andijon → Toshkent")

@dp.message_handler(state=TruckForm.route)
async def truck_route(message: types.Message, state: FSMContext):
    await state.update_data(route=message.text)
    await TruckForm.info.set()
    await message.answer("🚛 Mashina ma’lumotlari (turi, tonna, bo‘sh joy)")

@dp.message_handler(state=TruckForm.info)
async def truck_info(message: types.Message, state: FSMContext):
    await state.update_data(info=message.text)
    await TruckForm.phone.set()
    await message.answer("📞 Telefon raqamingiz")

@dp.message_handler(state=TruckForm.phone)
async def truck_finish(message: types.Message, state: FSMContext):
    data = await state.get_data()
    post = (
        "🚛 *MASHINA BOR*\n\n"
        f"📍 Yo‘nalish: {data['route']}\n"
        f"🚛 Mashina: {data['info']}\n"
        f"📞 Aloqa: {message.text}"
    )
    await bot.send_message(CHANNEL_ID, post, parse_mode="Markdown")
    await message.answer("✅ Mashina e’loni kanalga joylandi!", reply_markup=menu)
    await state.finish()

# ===== RUN =====
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
