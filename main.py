from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ParseMode
import requests
from googletrans import Translator

# التوكن الخاص بالبوت
BOT_TOKEN = '7614704758:AAGGv48BJqrzHJaUGWz4wQ2FL0iePS1HKxA'

# مفتاح OMDb API
OMDB_API_KEY = 'aa7d3da9'

# إعداد الترجمة
translator = Translator()

# دالة البداية
def start(update, context):
    update.message.reply_text("أرسل اسم فيلم أو مسلسل، وسأعطيك التفاصيل مع الترجمة 📽️")

# دالة التعامل مع الرسائل
def handle_message(update, context):
    title = update.message.text  # اسم الفيلم أو المسلسل من الرسالة
    url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}&plot=full&language=en"
    
    # طلب بيانات الفيلم من OMDb API
    response = requests.get(url).json()

    if response["Response"] == "True":
        # إرسال صورة متحركة (GIF) أولاً
        gif_url = "https://media.giphy.com/media/26BRrZv9lTG9NUsKI/giphy.gif"  # يمكنك تعديل الرابط حسب ما ترغب
        update.message.reply_animation(gif_url)

        # ترجمة القصة إلى العربية
        translated_plot = translator.translate(response["Plot"], dest='ar').text

        # إعداد البيانات التي سيتم إرسالها
        reply = f"""
*العنوان:* {response['Title']}
*السنة:* {response['Year']}
*التقييم:* {response['imdbRating']}
*النوع:* {response['Genre']}
*القصة:* {translated_plot}
*المنصات:* {response.get('Website', 'لا توجد بيانات عن المنصات')}
"""
        # إرسال تفاصيل الفيلم مع الترجمة
        update.message.reply_text(reply, parse_mode=ParseMode.MARKDOWN)
    else:
        # في حالة عدم العثور على الفيلم
        update.message.reply_text("لم أتمكن من العثور على هذا العنوان، تأكد من كتابة الاسم بشكل صحيح.")

# الدالة الرئيسية لبدء البوت
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # إضافة المعالجات (Handlers)
    dp.add_handler(CommandHandler("start", start))  # التعامل مع الأمر start
    dp.add_handler(MessageHandler(Filters.text, handle_message))  # التعامل مع الرسائل النصية

    # بدء البوت
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
