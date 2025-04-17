from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ParseMode
import requests
from googletrans import Translator

# التوكن الخاص بالبوت
BOT_TOKEN = '7614704758:AAHXU2ZPBrYXIusXuwbFCKFrCCHtoT8n-Do'

# مفتاح TMDb API
TMDB_API_KEY = '746779b16b752d4cbc6f46c42e87dde9'  # ضع هنا مفتاح API الخاص بك

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

# دالة للبحث عن الأفلام حسب النوع
def search_by_genre(update, context):
    genre = ' '.join(context.args)
    if not genre:
        update.message.reply_text("يرجى إدخال النوع بعد الأمر مثل: /search_by_genre أكشن")
        return

    url = f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&with_genres={genre}"
    response = requests.get(url).json()

    if response.get("results"):
        movies = response.get("results", [])
        movie_list = "\n".join([f"{movie['title']} ({movie['release_date'][:4]})" for movie in movies])
        update.message.reply_text(f"أفلام في نوع {genre}:\n{movie_list}\n\n"
                                  f"لمزيد من المعلومات يمكنك إضافة حسابي على السناب: {SNAPCHAT_LINK}")
    else:
        update.message.reply_text(f"لم أتمكن من العثور على أفلام من نوع {genre}\n\n"
                                  f"لمزيد من المعلومات يمكنك إضافة حسابي على السناب: {SNAPCHAT_LINK}")

# دالة للبحث عن الأفلام حسب التقييم
def search_by_rating(update, context):
    rating_threshold = float(context.args[0]) if context.args else 8.0
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&vote_average.gte={rating_threshold}"
    response = requests.get(url).json()

    if response.get("results"):
        movies = response.get("results", [])
        movie_list = "\n".join([f"{movie['title']} ({movie['release_date'][:4]}) - {movie['vote_average']}" for movie in movies])
        update.message.reply_text(f"أفلام بتقييم أعلى من {rating_threshold}:\n{movie_list}\n\n"
                                  f"لمزيد من المعلومات يمكنك إضافة حسابي على السناب: {SNAPCHAT_LINK}")
    else:
        update.message.reply_text("لم أتمكن من العثور على أفلام بناءً على التقييم المحدد.\n\n"
                                  f"لمزيد من المعلومات يمكنك إضافة حسابي على السناب: {SNAPCHAT_LINK}")

# دالة لعرض أفضل الأفلام أو المسلسلات
def top_rated(update, context):
    url = f"https://api.themoviedb.org/3/movie/top_rated?api_key={TMDB_API_KEY}"
    response = requests.get(url).json()

    if response.get("results"):
        movies = response.get("results", [])
        top_movies = sorted(movies, key=lambda x: x['vote_average'], reverse=True)[:5]

        if top_movies:
            movie_list = "\n".join([f"{movie['title']} ({movie['release_date'][:4]}) - {movie['vote_average']}" for movie in top_movies])
            update.message.reply_text(f"أفضل الأفلام:\n{movie_list}\n\n"
                                      f"لمزيد من المعلومات يمكنك إضافة حسابي على السناب: {SNAPCHAT_LINK}")
        else:
            update.message.reply_text("لم أتمكن من العثور على أفضل الأفلام.\n\n"
                                      f"لمزيد من المعلومات يمكنك إضافة حسابي على السناب: {SNAPCHAT_LINK}")
    else:
        update.message.reply_text("لم أتمكن من العثور على أفلام بناءً على التقييم.\n\n"
                                  f"لمزيد من المعلومات يمكنك إضافة حسابي على السناب: {SNAPCHAT_LINK}")

# دالة لمعالجة الرسائل
def handle_message(update, context):
    title = update.message.text
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={title}"
    response = requests.get(url).json()

    if response["results"]:
        movie = response["results"][0]  # نأخذ أول نتيجة فقط
        translated_plot = translator.translate(movie["overview"], dest='ar').text

        reply = f"""
*العنوان:* {movie['title']}
*السنة:* {movie['release_date'][:4]}
*التقييم:* {movie['vote_average']}
*النوع:* {movie['genre_ids']}
*القصة:* {translated_plot}
"""

        poster_url = f"https://image.tmdb.org/t/p/w500{movie.get('poster_path', '')}"

        if poster_url:
            update.message.reply_photo(photo=poster_url, caption=reply, parse_mode=ParseMode.MARKDOWN)
        else:
            update.message.reply_text(reply, parse_mode=ParseMode.MARKDOWN)

        update.message.reply_text(f"\nلمزيد من المعلومات يمكنك إضافة حسابي على السناب: {SNAPCHAT_LINK}")
    else:
        update.message.reply_text("لم أتمكن من العثور على هذا العنوان، تأكد من كتابة الاسم بشكل صحيح.\n\n"
                                  f"لمزيد من المعلومات يمكنك إضافة حسابي على السناب: {SNAPCHAT_LINK}")

# الوظيفة الرئيسية للبوت
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("top_rated", top_rated))
    dp.add_handler(CommandHandler("search_by_genre", search_by_genre))
    dp.add_handler(CommandHandler("search_by_rating", search_by_rating))
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
