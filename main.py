from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ParseMode
import requests
from googletrans import Translator
import random

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
                              "/search_by_rating <التقييم> - للبحث عن أفلام بتقييم أعلى من التقييم المطلوب\n"
                              "/recommend - للحصول على اقتراحات أفلام\n"
                              "/challenge - للحصول على تحدي يومي\n"
                              "/new_movies - للحصول على أحدث الأفلام\n\n"
                              f"لمزيد من المعلومات يمكنك إضافة حسابي على السناب: {SNAPCHAT_LINK}")

# دالة لاستخدام الذكاء الاصطناعي للاقتراحات
def ai_movie_recommendation(update, context):
    user_interests = "Action, Sci-Fi"  # يمكن تعديلها حسب اهتمامات المستخدم
    movies = [
        {'title': 'Inception', 'genre': 'Sci-Fi', 'rating': 8.8},
        {'title': 'The Matrix', 'genre': 'Action', 'rating': 8.7},
        {'title': 'The Dark Knight', 'genre': 'Action', 'rating': 9.0},
        {'title': 'Forrest Gump', 'genre': 'Drama', 'rating': 8.8},
    ]
    
    recommended = [movie for movie in movies if movie['genre'] in user_interests]
    
    if recommended:
        movie = random.choice(recommended)
        update.message.reply_text(f"اقترح لك الفيلم: {movie['title']} (التقييم: {movie['rating']})")
    else:
        update.message.reply_text("لم أتمكن من العثور على اقتراحات بناءً على اهتماماتك.")

# دالة لتقديم تحدي يومي
def daily_challenge(update, context):
    challenge = "تحدي اليوم: شاهد فيلم أكشن وحاول الوصول إلى تقييم 8.0 أو أعلى!"
    update.message.reply_text(challenge)

# دالة لتقديم تحدي أسبوعي
def weekly_challenge(update, context):
    challenge = "تحدي الأسبوع: اختر 3 أفلام في نفس النوع وأرسل لنا آراءك!"
    update.message.reply_text(challenge)

# دالة لإرسال إشعار حول المحتوى الجديد
def new_movie_notifications(update, context):
    url = f"http://www.omdbapi.com/?s=new&apikey={OMDB_API_KEY}"
    response = requests.get(url).json()
    
    if response.get("Response") == "True":
        new_movies = response.get("Search", [])
        movie_list = "\n".join([f"{movie['Title']} ({movie['Year']})" for movie in new_movies])
        update.message.reply_text(f"أحدث الأفلام التي تم إصدارها:\n{movie_list}")
    else:
        update.message.reply_text("لم يتم العثور على أفلام جديدة.")

# دالة للبحث عن الأفلام حسب النوع
def search_by_genre(update, context):
    genre = ' '.join(context.args)
    if not genre:
        update.message.reply_text("يرجى إدخال النوع بعد الأمر مثل: /search_by_genre أكشن")
        return

    url = f"http://www.omdbapi.com/?s=&genre={genre}&apikey={OMDB_API_KEY}"
    response = requests.get(url).json()

    if response.get("Response") == "True":
        movies = response.get("Search", [])
        movie_list = "\n".join([f"{movie['Title']} ({movie['Year']})" for movie in movies])
        update.message.reply_text(f"أفلام في نوع {genre}:\n{movie_list}\n\n"
                                  f"لمزيد من المعلومات يمكنك إضافة حسابي على السناب: {SNAPCHAT_LINK}")
    else:
        update.message.reply_text(f"لم أتمكن من العثور على أفلام من نوع {genre}\n\n"
                                  f"لمزيد من المعلومات يمكنك إضافة حسابي على السناب: {SNAPCHAT_LINK}")

# دالة للبحث عن الأفلام حسب التقييم
def search_by_rating(update, context):
    rating_threshold = float(context.args[0]) if context.args else 8.0
    url = f"http://www.omdbapi.com/?s=&apikey={OMDB_API_KEY}"
    response = requests.get(url).json()

    if response.get("Response") == "True":
        movies = response.get("Search", [])
        top_rated_movies = [movie for movie in movies if float(movie['imdbRating']) >= rating_threshold]
        movie_list = "\n".join([f"{movie['Title']} ({movie['Year']}) - {movie['imdbRating']}" for movie in top_rated_movies])
        update.message.reply_text(f"أفلام بتقييم أعلى من {rating_threshold}:\n{movie_list}\n\n"
                                  f"لمزيد من المعلومات يمكنك إضافة حسابي على السناب: {SNAPCHAT_LINK}")
    else:
        update.message.reply_text("لم أتمكن من العثور على أفلام بناءً على التقييم المحدد.\n\n"
                                  f"لمزيد من المعلومات يمكنك إضافة حسابي على السناب: {SNAPCHAT_LINK}")

# دالة لعرض أفضل الأفلام أو المسلسلات
def top_rated(update, context):
    url = f"http://www.omdbapi.com/?s=&apikey={OMDB_API_KEY}&type=movie,series"
    response = requests.get(url).json()

    if response.get("Response") == "True":
        movies = response.get("Search", [])
        top_movies = sorted(movies, key=lambda x: float(x['imdbRating']) if x['imdbRating'] != "N/A" else 0, reverse=True)[:5]
        
        if top_movies:
            movie_list = "\n".join([f"{movie['Title']} ({movie['Year']}) - {movie['imdbRating']}" for movie in top_movies])
            update.message.reply_text(f"أفضل الأفلام أو المسلسلات:\n{movie_list}\n\n"
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
    dp.add_handler(CommandHandler("recommend", ai_movie_recommendation))  # تعديل هنا
    dp.add_handler(CommandHandler("challenge", daily_challenge))  # إضافة تحدي يومي
    dp.add_handler(CommandHandler("new_movies", new_movie_notifications))  # إضافة إشعارات المحتوى الجديد
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))  # معالج الرسائل

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
