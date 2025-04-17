import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ParseMode

# رابط API لـ IPTV وبيانات الاعتماد
IPTV_API_URL = "http://u-max.co:2095/player_api.php"
IPTV_USERNAME = "966550170674"
IPTV_PASSWORD = "37946180"

# التوكن الخاص بالبوت
BOT_TOKEN = '7614704758:AAHXU2ZPBrYXIusXuwbFCKFrCCHtoT8n-Do'

# دالة لسحب الأفلام والمسلسلات من IPTV
def fetch_movies_and_series():
    # إعداد معلمات الطلب باستخدام بيانات الاعتماد
    params = {
        'username': IPTV_USERNAME,
        'password': IPTV_PASSWORD
    }
    
    try:
        # إرسال الطلب إلى خدمة IPTV مع المعلمات
        response = requests.get(IPTV_API_URL, params=params)
        data = response.json()
        
        # التحقق من وجود بيانات الأفلام والمسلسلات
        if 'movie_data' in data:
            movies = data['movie_data']  # استخراج الأفلام والمسلسلات
            return movies
        else:
            print("لم يتم العثور على بيانات الأفلام أو المسلسلات.")
            return None
    
    except requests.exceptions.RequestException as e:
        print(f"خطأ في الاتصال بخدمة IPTV: {e}")
        return None

# دالة لعرض قائمة الأفلام والمسلسلات للمستخدم
def show_movies(update, context):
    # استدعاء دالة fetch_movies_and_series لسحب الأفلام والمسلسلات
    movies = fetch_movies_and_series()
    
    if movies:
        movie_list = "\n".join([f"{movie['name']} - {movie.get('year', 'غير متوفر')}\n"
                                f"رابط البث: {movie['stream_url']}" for movie in movies])
        update.message.reply_text(f"إليك قائمة الأفلام والمسلسلات:\n{movie_list}")
    else:
        update.message.reply_text("لم أتمكن من العثور على أي أفلام أو مسلسلات.")

# دالة لبدء البوت
def start(update, context):
    update.message.reply_text("أرسل /movies لعرض قائمة الأفلام والمسلسلات.")

# الوظيفة الرئيسية للبوت
def main():
    # إعداد البوت
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    
    # إضافة الأوامر والمستمعين
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("movies", show_movies))  # أمر لعرض الأفلام والمسلسلات
    
    # بدء البوت
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
