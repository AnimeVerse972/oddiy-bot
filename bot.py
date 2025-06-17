import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

TOKEN = os.getenv("BOT_TOKEN")
CHANNELS = ['@AniVerseClip', '@StudioNovaOfficial']

logging.basicConfig(level=logging.INFO)

anime_posts ={
        "1": {"channel": "@AniVerseClip", "message_id": 10},
        "2": {"channel": "@AniVerseClip", "message_id": 23},
        "3": {"channel": "@AniVerseClip", "message_id": 35},
        "4": {"channel": "@AniVerseClip", "message_id": 49},
        "5": {"channel": "@AniVerseClip", "message_id": 76},
        "6": {"channel": "@AniVerseClip", "message_id": 104},
        "7": {"channel": "@AniVerseClip", "message_id": 851},
        "8": {"channel": "@AniVerseClip", "message_id": 127},
        "9": {"channel": "@AniVerseClip", "message_id": 131},
        "10": {"channel": "@AniVerseClip", "message_id": 135},
        "11": {"channel": "@AniVerseClip", "message_id": 148},
        "12": {"channel": "@AniVerseClip", "message_id": 200},
        "13": {"channel": "@AniVerseClip", "message_id": 216},
        "14": {"channel": "@AniVerseClip", "message_id": 222},
        "15": {"channel": "@AniVerseClip", "message_id": 235},
        "16": {"channel": "@AniVerseClip", "message_id": 260},
        "17": {"channel": "@AniVerseClip", "message_id": 360},
        "18": {"channel": "@AniVerseClip", "message_id": 379},
        "19": {"channel": "@AniVerseClip", "message_id": 392},
        "20": {"channel": "@AniVerseClip", "message_id": 405},
        "21": {"channel": "@AniVerseClip", "message_id": 430},
        "22": {"channel": "@AniVerseClip", "message_id": 309},
        "23": {"channel": "@AniVerseClip", "message_id": 343},
        "24": {"channel": "@AniVerseClip", "message_id": 501},
        "25": {"channel": "@AniVerseClip", "message_id": 514},
        "26": {"channel": "@AniVerseClip", "message_id": 462},
        "27": {"channel": "@AniVerseClip", "message_id": 527},
        "28": {"channel": "@AniVerseClip", "message_id": 542},
        "29": {"channel": "@AniVerseClip", "message_id": 555},
        "30": {"channel": "@AniVerseClip", "message_id": 569},
        "31": {"channel": "@AniVerseClip", "message_id": 586},
        "32": {"channel": "@AniVerseClip", "message_id": 624},
        "33": {"channel": "@AniVerseClip", "message_id": 638},
        "34": {"channel": "@AniVerseClip", "message_id": 665},
        "35": {"channel": "@AniVerseClip", "message_id": 696},
        "36": {"channel": "@AniVerseClip", "message_id": 744},
        "37": {"channel": "@AniVerseClip", "message_id": 776},
        "38": {"channel": "@AniVerseClip", "message_id": 789},
        "39": {"channel": "@AniVerseClip", "message_id": 802},
        "40": {"channel": "@AniVerseClip", "message_id": 815},
        "41": {"channel": "@AniVerseClip", "message_id": 835},
        "42": {"channel": "@AniVerseClip", "message_id": 864},
        "43": {"channel": "@AniVerseClip", "message_id": 918},
        "44": {"channel": "@AniVerseClip", "message_id": 931},
        "45": {"channel": "@AniVerseClip", "message_id": 946},
    }

def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    not_subscribed = []

    for channel in CHANNELS:
        try:
            member = context.bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status not in ["member", "administrator", "creator"]:
                not_subscribed.append(channel)
        except:
            not_subscribed.append(channel)

    if not_subscribed:
        keyboard = [[InlineKeyboardButton(f"🔔 {ch}", url=f"https://t.me/{ch.strip('@')}")] for ch in not_subscribed]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("📛 *Botdan foydalanish uchun quyidagi kanallarga obuna bo‘ling:*", reply_markup=reply_markup, parse_mode="Markdown")
        return

    buttons = [[KeyboardButton("📢 Reklama"), KeyboardButton("💼 Homiylik")]]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text("✅ Assalomu alaykum!\nAnime kodini yuboring (masalan: 1, 2, 3, ...)", reply_markup=reply_markup)

def handle_message(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    text = update.message.text.strip()

    for channel in CHANNELS:
        try:
            member = context.bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status not in ['member', 'administrator', 'creator']:
                update.message.reply_text(f"⛔ Iltimos, {channel} kanaliga obuna bo‘ling va qaytadan urinib ko‘ring.")
                return
        except:
            update.message.reply_text(f"⚠️ {channel} kanal tekshiruvida xatolik. Iltimos, keyinroq urinib ko‘ring.")
            return

    if text in anime_posts:
        post = anime_posts[text]
        link = f"https://t.me/{post['channel'].strip('@')}/{post['message_id']}"
        button = InlineKeyboardMarkup([[InlineKeyboardButton("TOMOSHA QILISH", url=link)]])
        context.bot.forward_message(chat_id=user_id, from_chat_id=post['channel'], message_id=post['message_id'])
        update.message.reply_text("🔗 Post link:", reply_markup=button)
    elif text == "📢 Reklama":
        update.message.reply_text("Reklama uchun @DiyorbekPTMA ga murojat qiling.")
    elif text == "💼 Homiylik":
        update.message.reply_text("Homiylik uchun karta 8800904257677885")
    else:
        update.message.reply_text("❌ Bunday kod topilmadi.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
