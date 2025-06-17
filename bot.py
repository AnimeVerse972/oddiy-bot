from telegram import Update, ChatMember
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import json

BOT_TOKEN = "7802093581:AAG5kMAgx5SpWENWGlyxBTyqh2OF0ihmeVc"

# Majburiy obuna qilish uchun kanallar
REQUIRED_CHANNELS = ["@AniVerseClip", "@StudioNovaOfficial"]

# Kodlar faylini ochish
with open("codes.json", "r") as f:
    codes = json.load(f)

# Obuna tekshiruvi
async def is_subscribed(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    for channel in REQUIRED_CHANNELS:
        try:
            member = await context.bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status in [ChatMember.LEFT, ChatMember.KICKED]:
                return False
        except:
            return False
    return True

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! Kodni yuboring va unga mos xabarni oling.")

# Kodni tekshirish
async def handle_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not await is_subscribed(user_id, context):
        msg = "❌ Botdan foydalanish uchun quyidagi kanallarga obuna bo‘ling:\n"
        msg += "\n".join(REQUIRED_CHANNELS)
        await update.message.reply_text(msg)
        return

    user_code = update.message.text.strip()
    if user_code in codes:
        await update.message.reply_text(f"✅ Kod topildi:\n\n{codes[user_code]}")
    else:
        await update.message.reply_text("❌ Bunday kod topilmadi.")

# Botni ishga tushurish
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_code))
    app.run_polling()

if __name__ == "__main__":
    main()
