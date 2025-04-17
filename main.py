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
                              "/search_by_genre <النوع> - للبحث عن أفلام أو مسلسلات حسب النوع\n"
                              "/search_by_rating <التقييم> - للبحث عن أفلام أو مسلسلات بتقييم أعلى من التقييم المطلوب\n\n"
                              f"لمزيد من المعلومات يمكنك إضافة حسابي على السناب: {SNAPCHAT_LINK}")

# دالة للبحث عن الأفلام والمسلسلات حسب النوع
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
        # إذا لم تكن هناك أفلام، حاول البحث عن المسلسلات
        url = f"https://api.themoviedb.org/3/discover/tv?api_key={TMDB_API_KEY}&with_genres={genre}"
        response = requests.get(url).json()

        if response.get("results"):
            shows = response.get("results", [])
            show_list = "\n".join([f"{show['name']} ({show['first_air_date'][:4]})" for show in shows])
            update.message.reply_text(f"مسلسلات في نوع {genre}:\n{show_list}\n\n"
                                      f"لمزيد من المعلومات يمكنك إضافة حسابي على السناب: {SNAPCHAT_LINK}")
        else:
            update.message.reply_text(f"لم أتمكن من العثور على أفلام أو مسلسلات من نوع {genre}\n\n"
                                      f"لمزيد من المعلومات يمكنك إضافة حسابي على السناب: {SNAPCHAT_LINK}")

# دالة للبحث عن الأفلام والمسلسلات حسب التقييم
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
        # إذا لم تكن هناك أفلام، حاول البحث عن المسلسلات
        url = f"https://api.themoviedb.org/3/discover/tv?api_key={TMDB_API_KEY}&vote_average.gte={rating_threshold}"
        response = requests.get(url).json()

        if response.get("results"):
            shows = response.get("results", [])
            show_list = "\n".join([f"{show['name']} ({show['first_air_date'][:4]}) - {show['vote_average']}" for show in shows])
            update.message.reply_text(f"مسلسلات بتقييم أعلى من {rating_threshold}:\n{show_list}\n\n"
                                      f"لمزيد من المعلومات يمكنك إضافة حسابي على السناب: {SNAPCHAT_LINK}")
        else:
            update.message.reply_text("لم أتمكن من العثور على أفلام أو مسلسلات بناءً على التقييم المحدد.\n\n"
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
            # إذا لم تكن هناك أفلام، حاول البحث عن المسلسلات
            url = f"https://api.themoviedb.org/3/tv/top_rated?api_key={TMDB_API_KEY}"
            response = requests.get(url).json()

            if response.get("results"):
                shows = response.get("results", [])
                top_shows = sorted(shows, key=lambda x: x['vote_average'], reverse=True)[:5]

                show_list = "\n".join([f"{show['name']} ({show['first_air_date'][:4]}) - {show['vote_average']}" for show in top_shows])
                update.message.reply_text(f"أفضل المسلسلات:\n{show_list}\n\n"
                                          f"لمزيد من المعلومات يمكنك إضافة حسابي على السناب: {SNAPCHAT_LINK}")
            else:
                update.message.reply_text("لم أتمكن من العثور على أفضل الأفلام أو المسلسلات.\n\n"
                                          f"لمزيد من المعلومات يمكنك إضافة حسابي على السناب: {SNAPCHAT_LINK}")
    else:
        update.message.reply_text("لم أتمكن من العثور على أفلام أو مسلسلات بناءً على التقييم.\n\n"
                                  f"لمزيد من المعلومات يمكنك إضافة حسابي على السناب: {SNAPCHAT_LINK}")

# دالة لمعالجة الرسائل
def handle_message(update, context):
    title = update.message.text
    url = f"https://api.themoviedb.org/3/search/multi?api_key={TMDB_API_KEY}&query={title}"
    response = requests.get(url).json()

    if response["results"]:
        item = response["results"][0]  # نأخذ أول نتيجة فقط
        translated_plot = translator.translate(item["overview"], dest='ar').text

        reply = f"""
*العنوان:* {item['title'] if 'title' in item else item['name']}
*السنة:* {item['release_date'][:4] if 'release_date' in item else item['first_air_date'][:4]}
*التقييم:* {item['vote_average']}
*القصة:* {translated_plot}
"""

        poster_url = f"https://image.tmdb.org/t/p/w500{item.get('poster_path', '')}"

        if poster_url:
            update.message.reply_photo(photo=poster_url, caption=reply, parse_mode=ParseMode.MARKDOWN)
        else:
            update.message.reply_text(reply, parse_mode=ParseMode.MARKDOWN)

        update.message.reply_text(f"\nلمزيد من المعلومات يمكنك إضافة
