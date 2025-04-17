from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ParseMode
import requests
from googletrans import Translator

# التوكن الخاص بالبوت
BOT_TOKEN = '7614704758:AAGGv48BJqrzHJaUGWz4wQ2FL0iePS1HKxA'

# مفتاح OMDb API
OMDB_API_KEY = 'aa7d3da9'

translator = Translator()

def start(update, context):
    update.message.reply_text("مرحباً! أرسل لي اسم فيلم أو مسلسل أو استخدم الأوامر المتاحة.")

# دالة للرد فقط على الرسائل من المستخدمين
def handle_message(update, context):
    # التحقق من أن المرسل ليس بوت
    if update.message.from_user.is_bot:
        return

    title = update.message.text
    url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}&plot=full&language=en"
    response = requests.get(url).json()

    if response["Response"] == "True":
        translated_plot = translator.translate(response["Plot"], dest='ar').text

        reply = f"""
        *العنوان:* {response['Title']}
        *السنة:* {response['Year']}
        *التقييم:* {response['imdbRating']}
        *النوع:* {response['Genre']}
        *القصة:* {translated_plot}
        """

        poster_url = response.get("Poster", "")

        if poster_url and poster_url != "N/A":
            update.message.reply_photo(photo=poster_url, caption=reply, parse_mode=ParseMode.MARKDOWN)
        else:
            update.message.reply_text(reply, parse_mode=ParseMode.MARKDOWN)
    else:
        update.message.reply_text("لم أتمكن من العثور على هذا العنوان، تأكد من كتابة الاسم بشكل صحيح.")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))  # عدم الرد على البوتات

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
