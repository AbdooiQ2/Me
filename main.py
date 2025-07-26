import telebot
import yt_dlp
import os
from telebot import types

BOT_TOKEN = '8065711531:AAE_hlo4P9weZ3JDavvamb51-t_kqA7nN8A'
bot = telebot.TeleBot(BOT_TOKEN)

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# اسم القناة المطلوبة (بدون @)
REQUIRED_CHANNEL = "rurnnr"  # 🔁 غيّره بمعرف قناتك

# التحقق من الاشتراك
def is_user_subscribed(user_id):
    try:
        member = bot.get_chat_member(f"@{REQUIRED_CHANNEL}", user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

# أمر /start مع زر المطور (رابط مباشر)
@bot.message_handler(commands=['start'])
def start_msg(message):
    chat_id = message.chat.id

    # زر المطور كرابط
    markup = types.InlineKeyboardMarkup()
    dev_button = types.InlineKeyboardButton(" المطور", url="https://t.me/unrrrn")  # 👈 عدّل معرفك هنا
    markup.add(dev_button)

    bot.send_message(chat_id, " أرسل رابط فيديو من YouTube, TikTok, أو Instagram وسأحمله لك!", reply_markup=markup)

# التعامل مع روابط الفيديو
@bot.message_handler(func=lambda msg: msg.text.startswith("http"))
def handle_link(message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    # تحقق من الاشتراك
    if not is_user_subscribed(user_id):
        bot.send_message(chat_id, f" يجب عليك الاشتراك في قناة الدعم أولاً:\n\n@{REQUIRED_CHANNEL}")
        return

    loading_msg = bot.send_message(chat_id, " جاري تحميل الفيديو، انتظر لحظة...")

    try:
        ydl_opts = {
            'format': 'mp4',
            'outtmpl': f'{DOWNLOAD_DIR}/%(title).70s.%(ext)s',
            'quiet': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(message.text, download=True)
            video_path = ydl.prepare_filename(info)

        with open(video_path, 'rb') as video:
            bot.send_video(chat_id, video)

        bot.delete_message(chat_id, loading_msg.message_id)
        os.remove(video_path)

    except Exception as e:
        bot.send_message(chat_id, f" فشل التحميل")

# تشغيل البوت
bot.polling()
