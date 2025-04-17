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
                              "/search_by_rating <التقييم> - للبحث عن أفلام بتقييم أعلى من التقييم المطلوب\n"
                              "/compare_movies <اسم الفيلم 1> <اسم الفيلم 2> - لمقارنة فيلمين\n"
                              "/movie_ar <اسم الفيلم> - لتجربة الواقع المعزز لفيلم\n\n"
                              f"لمزيد من المعلومات يمكنك إضافة حسابي على السناب: {SNAPCHAT_LINK}")

# دالة لمقارنة الأفلام
def compare_movies(update, context):
    if len(context.args) < 2:
        update.message.reply_text("يرجى إدخال اسم فيلمين للمقارنة مثل: /compare_movies Inception Avatar")
        return
    
    movie1_title = context.args[0]
    movie2_title = context.args[1]
    
    url1 = f"http://www.omdbapi.com/?t={movie1_title}&apikey={OMDB_API_KEY}"
    url2 = f"http://www.omdbapi.com/?t={movie2_title}&apikey={OMDB_API_KEY}"
    
    response1 = requests.get(url1).json()
    response2 = requests.get(url2).json()
    
    if response1.get("Response") == "False" or response2.get("Response") == "False":
        update.message.reply_text("لم أتمكن من العثور على أحد الأفلام، تأكد من كتابة الاسم بشكل صحيح.")
        return
    
    comparison = f"**مقارنة بين {response1['Title']} و {response2['Title']}**\n\n"
    comparison += f"*{response1['Title']}*: {response1['imdbRating']} | *{response2['Title']}*: {response2['imdbRating']}\n"
    comparison += f"النوع: {response1['Genre']} vs {response2['Genre']}\n"
    comparison += f"السنة: {response1['Year']} vs {response2['Year']}\n"
    
    update.message.reply_text(comparison)

# دالة لتفعيل تجربة AR
def movie_ar(update, context):
    movie_title = ' '.join(context.args)
    
    # استعلام OMDb للحصول على تفاصيل الفيلم
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}&plot=short"
    response = requests.get(url).json()
    
    if response.get("Response") == "False":
        update.message.reply_text(f"لم أتمكن من العثور على الفيلم {movie_title}. تأكد من الاسم.")
        return
    
    movie_details = f"**{response['Title']}** ({response['Year']})\n"
    
    # يمكن أن تكون هناك روابط AR مدمجة هنا (تخيل مثلاً منصة AR متكاملة مع API)
    ar_link = f"https://your-ar-experience-link.com/{response['imdbID']}"  # رابط AR الخاص بالفيلم
    
    update.message.reply_text(f"{movie_details}\nلرؤية الفيلم باستخدام الواقع المعزز، افتح الرابط التالي:\n{ar_link}")

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
        # معالجة تصنيف الأفلام أو المسلسلات حسب التقييم (بترتيب تنازلي)
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
    dp.add_handler(CommandHandler("compare_movies", compare_movies))
    dp.add_handler(CommandHandler("movie_ar", movie_ar))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
