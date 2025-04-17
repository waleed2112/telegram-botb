from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ParseMode
import requests
from googletrans import Translator

# التوكن الخاص بالبوت
BOT_TOKEN = '7614704758:AAHXU2ZPBrYXIusXuwbFCKFrCCHtoT8n-Do'

# مفتاح OMDb API
OMDB_API_KEY = 'aa7d3da9'

translator = Translator()

# دالة لبدء البوت
def start(update, context):
    update.message.reply_text("أرسل اسم فيلم أو مسلسل، أو استخدم الأوامر التالية:\n"
                              "/top - للحصول على أفضل الأفلام أو المسلسلات\n"
                              "/genre <النوع> - للبحث عن أفلام حسب النوع\n"
                              "/rating <التقييم> - للبحث عن أفلام بتقييم أعلى من التقييم المطلوب\n"
                              "استخدم الأمر /help للحصول على المزيد من التفاصيل.")

# دالة للمساعدة
def help(update, context):
    SNAPCHAT_USERNAME = "XWN_4"
    SNAPCHAT_LINK = f"https://www.snapchat.com/add/{SNAPCHAT_USERNAME}"
    update.message.reply_text(f"لمزيد من المعلومات يمكنك إضافة حسابي على السناب: {SNAPCHAT_LINK}\n"
                              "يمكنك استخدام الأوامر التالية:\n"
                              "/top - للحصول على أفضل الأفلام أو المسلسلات\n"
                              "/genre <النوع> - للبحث عن أفلام حسب النوع\n"
                              "/rating <التقييم> - للبحث عن أفلام بتقييم أعلى من التقييم المطلوب")

# دالة للبحث عن الأفلام حسب النوع
def search_by_genre(update, context):
    genre = ' '.join(context.args)
    if not genre:
        update.message.reply_text("يرجى إدخال النوع بعد الأمر مثل: /genre أكشن")
        return

    url = f"http://www.omdbapi.com/?s=&genre={genre}&apikey={OMDB_API_KEY}"
    response = requests.get(url).json()

    if response.get("Response") == "True":
        movies = response.get("Search", [])
        movie_list = "\n".join([f"{movie['Title']} ({movie['Year']})" for movie in movies])
        update.message.reply_text(f"أفلام في نوع {genre}:\n{movie_list}")
    else:
        update.message.reply_text(f"لم أتمكن من العثور على أفلام من نوع {genre}")

# دالة للبحث عن الأفلام حسب التقييم
def search_by_rating(update, context):
    rating_threshold = float(context.args[0]) if context.args else 8.0
    url = f"http://www.omdbapi.com/?s=&apikey={OMDB_API_KEY}"
    response = requests.get(url).json()

    if response.get("Response") == "True":
        movies = response.get("Search", [])
        top_rated_movies = [movie for movie in movies if float(movie['imdbRating']) >= rating_threshold]
        movie_list = "\n".join([f"{movie['Title']} ({movie['Year']}) - {movie['imdbRating']}" for movie in top_rated_movies])
        update.message.reply_text(f"أفلام بتقييم أعلى من {rating_threshold}:\n{movie_list}")
    else:
        update.message.reply_text("لم أتمكن من العثور على أفلام بناءً على التقييم المحدد.")

# دالة لعرض أفضل الأفلام أو المسلسلات
def top_rated(update, context):
    url = f"http://www.omdbapi.com/?s=&apikey={OMDB_API_KEY}&type=movie,series"
    response = requests.get(url).json()

    if response.get("Response") == "True":
        movies = response.get("Search", [])
        top_movies = sorted(movies, key=lambda x: float(x['imdbRating']) if x['imdbRating'] != "N/A" else 0, reverse=True)[:5]
        
        if top_movies:
            movie_list = "\n".join([f"{movie['Title']} ({movie['Year']}) - {movie['imdbRating']}" for movie in top_movies])
            update.message.reply_text(f"أفضل الأفلام أو المسلسلات:\n{movie_list}")
        else:
            update.message.reply_text("لم أتمكن من العثور على أفضل الأفلام أو المسلسلات.")
    else:
        update.message.reply_text("لم أتمكن من العثور على أفلام أو مسلسلات بناءً على التقييم.")

# دالة لمعالجة الرسائل
def handle_message(update, context):
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
