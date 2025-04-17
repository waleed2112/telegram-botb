import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ParseMode
from googletrans import Translator

# التوكن الخاص بالبوت
BOT_TOKEN = '7614704758:AAHXU2ZPBrYXIusXuwbFCKFrCCHtoT8n-Do'

# مفتاح OMDb API
OMDB_API_KEY = 'aa7d3da9'

# حساب السناب
SNAPCHAT_USERNAME = "XWN_4"
SNAPCHAT_LINK = f"https://www.snapchat.com/add/{SNAPCHAT_USERNAME}"

translator = Translator()

# دالة لبدء البوت
def start(update, context):
    update.message.reply_text("أرسل اسم فيلم أو مسلسل، أو استخدم الأوامر التالية:\n"
                              "/top_rated - للحصول على أفضل الأفلام أو المسلسلات\n"
                              "/search_by_genre <النوع> - للبحث عن أفلام حسب النوع\n"
                              "/search_by_rating <التقييم> - للبحث عن أفلام بتقييم أعلى من التقييم المطلوب\n\n"
                              f"لمزيد من المعلومات يمكنك إضافة حسابي على السناب: {SNAPCHAT_LINK}")

# دالة للبحث عن روابط المشاهدة باستخدام JustWatch API
def get_movie_link(movie_name):
    justwatch_url = f"https://api.justwatch.com/search?q={movie_name}"  # تأكد من صحة الرابط
    response = requests.get(justwatch_url).json()

    # طباعة استجابة JustWatch API
    print("JustWatch API Response:", response)
    
    try:
        link = response['items'][0]['offers'][0]['url']
        return link
    except (IndexError, KeyError):
        return "رابط المشاهدة غير متوفر"

# دالة لمعالجة الرسائل
def handle_message(update, context):
    title = update.message.text
    url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}&plot=full&language=en"
    response = requests.get(url).json()

    # طباعة استجابة OMDb API
    print("OMDb API Response:", response)

    if response["Response"] == "True":
        translated_plot = translator.translate(response["Plot"], dest_
