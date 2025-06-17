# oddiy-bot
# Telegram Kod Qidiruvchi Bot

Bu bot foydalanuvchi yuborgan kodga qarab mos xabarni yuboradi. Shuningdek, botdan foydalanish uchun majburiy obuna qo‘yilgan.

## Xususiyatlar
- Majburiy kanal obunasi tekshiradi
- Kod yuborilganda, `codes.json` faylidan topadi va tegishli xabarni chiqaradi
- `python-telegram-bot` kutubxonasi asosida

## Ishlatish

1. `bot.py` faylida `BOT_TOKEN` va `REQUIRED_CHANNELS` ni to‘ldiring.
2. Quyidagi buyruqlar bilan ishga tushiring:

```bash
pip install -r requirements.txt
python bot.py
