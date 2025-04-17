from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests
from googletrans import Translator
from telegram import ParseMode

# التوكن الخاص بالبوت (استبدله بتوكن البوت الذي حصلت عليه من BotFather)
BOT_TOKEN = '7614704758:AAHXU2ZPBrYXIusXuwbFCKFrCCHtoT8n-Do'

# مفتاح OMDb API
OMDB_API_KEY = 'aa7d3da9'

translator = Translator()

# دالة لبدء البوت
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("أرسل اسم فيلم أو مسلسل، أو استخدم الأوامر التالية:\n"
                              "/top_rated - للحصول على أفضل الأفلام أو المسلسلات\n"
                              "/search_by_genre <النوع> - للبحث عن أفلام حسب النوع\n"
                              "/search_by_rating <التقييم> - للبحث عن أفلام بتقييم أعلى من التقييم المطلوب")

# دالة للبحث عن الأفلام حسب النوع
def search_by_genre(update: Update, context: CallbackContext) -> None:
    genre = ' '.join(context.args)
    if not genre:
        update.message.reply_text("يرجى إدخال النوع بعد الأمر مثل: /search_by_genre أكشن")
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
def search_by_rating(update: Update, context: CallbackContext) -> None:
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
def top_rated(update: Update, context: CallbackContext) -> None:
    url = f"http://www.omdbapi.com/?s=&apikey={OMDB_API_KEY}&type=movie,series"
    response = requests.get(url).json()

    if response.get("Response") == "True":
        movies = response.get("Search", [])
        top_movies = sorted(movies, key=lambda x: float(x['imdbRating']) if x['imdbRating'] != "N/A" else 0, reverse=True)[:5]
        
        if top_movies:
            movie_list = "\n".join([f"{movie['Title']} ({movie['Year']}) - {movie['imdbRating']}" for movie in top_movies])
            update.message.reply_text(f"أفضل الأفلام أو المسلسلات:\n{movie_list}")
        else:
            update.message.reply_text_
