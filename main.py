from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import ParseMode
import requests
from googletrans import Translator

# التوكن الخاص بالبوت
BOT_TOKEN = '7614704758:AAGGv48BJqrzHJaUGWz4wQ2FL0iePS1HKxA'

# مفتاح OMDb API
OMDB_API_KEY = 'aa7d3da9'

translator = Translator()

def start(update, context):
    update.message.reply_text("أرسل اسم فيلم أو مسلسل، وسأعطيك التفاصيل مع الترجمة 📽️")

def handle_message(update, context):
    title = update.message.text
    url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}&plot=full&language=en"
    response = requests.get(url).json()

    if response["Response"] == "True":
        # الترجمة
        translated_plot = translator.translate(response["Plot"], dest='ar').text
        
        # استخراج المنصات (إذا كانت موجودة)
        platforms = response.get('Website', 'غير متوفر')
        
        # الحصول على رابط البوستر
        poster_url = response.get("Poster", "")

        # إنشاء الرد مع المنصات والصورة
        reply = f"""
*العنوان:* {response['Title']}
*السنة:* {response['Year']}
*التقييم:* {response['imdbRating']}
*النوع:* {response['Genre']}
*القصة:* {translated_plot}
*المنصات:* {platforms}
"""
        update.message.reply_text(reply, parse_mode=ParseMode.MARKDOWN)

        # إرسال الصورة (بوستر الفيلم)
        if poster_url:
            update.message.reply_photo(poster_url)
        else:
            update.message.reply_text("لم أتمكن من العثور على صورة البوستر.")

    else:
        update.message.reply_text("لم أتمكن من العثور على هذا العنوان، تأكد من كتابة الاسم بشكل صحيح.")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
