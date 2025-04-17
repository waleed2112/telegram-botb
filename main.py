from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ParseMode
import requests
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

# دالة للحصول على رابط الفيلم من JustWatch
def get_movie_link(title):
    justwatch_url = f"https://api.justwatch.com/search?q={title}"
    response = requests.get(justwatch_url)

    if response.status_code == 200:  # التأكد من أن الاستجابة كانت ناجحة
        try:
            return response.json()
        except ValueError:
            print(f"فشل في تحويل البيانات إلى JSON: {response.text}")
            return None
    else:
        print(f"فشل في الاتصال بـ JustWatch، رمز الاستجابة: {response.status_code}")
        return None

# دالة
