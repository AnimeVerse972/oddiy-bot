import os
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Tokenni olish (.env yoki Render'dan)
API_TOKEN = os.environ.get('BOT_TOKEN')

# Obuna bo'lishi kerak bo'lgan kanallar
CHANNELS = ['@AniVerseClip', '@StudioNovaOfficial']

# Adminlar ro‘yxati (ID lar)
ADMINS = ['6486825926', '7575041003']

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, parse_mode="Markdown")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

valid_statuses = ['member', 'administrator', 'creator']

async def is_user_subscribed(channel, user_id):
    try:
        member = await bot.get_chat_member(channel, user_id)
        return member.status in valid_statuses
    except Exception as e:
        print(f"[Xatolik] {channel} kanal: {e}")
        return False

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    not_subscribed = []

    for channel in CHANNELS:
        if not await is_user_subscribed(channel, user_id):
            not_subscribed.append(channel)

    if not_subscribed:
        keyboard = InlineKeyboardMarkup(row_width=1)
        for ch in not_subscribed:
            keyboard.add(InlineKeyboardButton(f"🔔 {ch}", url=f"https://t.me/{ch.strip('@')}"))
        await message.answer("📛 *Botdan foydalanish uchun quyidagi kanallarga obuna bo‘ling:*", reply_markup=keyboard)
        return

    # Bosh menyu
    buttons = [[KeyboardButton("📢 Reklama"), KeyboardButton("💼 Homiylik")]]
    reply_markup = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)
    await message.answer("✅ Assalomu alaykum!\nAnime kodini yuboring (masalan: 1, 2, 3, ...)", reply_markup=reply_markup)

@dp.message_handler()
async def handle_code(message: types.Message):
    user_id = message.from_user.id

    # Obuna tekshiruvi
    for channel in CHANNELS:
        if not await is_user_subscribed(channel, user_id):
            await message.answer(f"⛔ Iltimos, {channel} kanaliga obuna bo‘ling va qaytadan urinib ko‘ring.")
            return

    # Kod asosida xabarlar
    anime_posts = {
        "1": {"channel": "@AniVerseClip", "message_id": 10},
        "2": {"channel": "@AniVerseClip", "message_id": 23},
        "3": {"channel": "@AniVerseClip", "message_id": 35},
        "12": {"channel": "@AniVerseClip", "message_id": 200},
        # Yana boshqa kodlar ham shu yerga qo‘shiladi...
    }

    text = message.text.strip()

    if text in anime_posts:
        info = anime_posts[text]
        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton("TOMOSHA QILISH", url=f"https://t.me/{info['channel'].strip('@')}/{info['message_id']}")
        )
        await bot.copy_message(chat_id=user_id, from_chat_id=info['channel'], message_id=info['message_id'], reply_markup=keyboard)

    elif text == "📢 Reklama":
        await message.answer("📢 Reklama uchun @DiyorbekPTMA ga murojaat qiling.")
    elif text == "💼 Homiylik":
        await message.answer("💼 Homiylik uchun karta raqami: 8800904257677885")
    else:
        await message.answer("❌ Bunday kod topilmadi. Iltimos, to‘g‘ri anime kodini yuboring.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
