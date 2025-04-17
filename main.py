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

# اسم المستخدم في تلجرام
USER_TELEGRAM = "@iLHwk"

# متغيرات اللعبة والتحديات
user_scores = {}  # لتخزين النقاط
quotes = [
    {"quote": "May the Force be with you.", "movie": "Star Wars", "hint": "This is a famous line from a space-themed saga."},
    {"quote": "I'll be back.", "movie": "The Terminator", "hint": "A famous quote from a movie about a cyborg."},
    # أضف هنا المزيد من الاقتباسات حسب رغبتك
]
quote_today = random.choice(quotes)  # اقتباس اليوم

translator = Translator()

# دالة لبدء البوت
def start(update, context):
    update.message.reply_text(f"أرسل اسم فيلم أو مسلسل للبحث، أو استخدم الأوامر التالية:\n"
                              "/top - للحصول على أفضل الأفلام أو المسلسلات\n"
                              "/genre <النوع> - للبحث عن أفلام حسب النوع\n"
                              "/rating <التقييم> - للبحث عن أفلام بتقييم أعلى من التقييم المطلوب\n"
                              f"/help - لمساعدتك\n\n"
                              f"لمزيد من المعلومات يمكنك إضافة حسابي على السناب: {SNAPCHAT_LINK}")

# دالة لعرض /help مع اليوزر
def help(update, context):
    update.message.reply_text(f"لأي استفسار تواصل مع {USER_TELEGRAM}.\n"
                              "يمكنك إرسال اسم فيلم أو مسلسل للبحث عنه أو استخدم الأوامر كما ذكرنا.\n"
                              f"أرسل اقتباسات من الأفلام كل يوم مع تحدي جديد.\n\n"
                              f"لمزيد من المعلومات يمكنك إضافة حسابي على السناب: {SNAPCHAT_LINK}")

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
        update.message.reply_text(f"لم أتمكن من العثور على أفلام من نوع {genre}.\n\n"
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
            update.message.reply_text(f"أفضل الأفلام أو المسلسلات:\n{movie_list}")
        else:
            update.message.reply_text("لم أتمكن من العثور على أفضل الأفلام أو المسلسلات.")
    else:
        update.message.reply_text("لم أتمكن من العثور على أفلام أو مسلسلات بناءً على التقييم.")

# دالة لمعالجة الرسائل (البحث عن الفيلم أو المسلسل)
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
    else:
        update.message.reply_text("لم أتمكن من العثور على هذا العنوان، تأكد من كتابة الاسم بشكل صحيح.")

# دالة لتحدي الاقتباس
def quote_challenge(update, context):
    user_id = update.message.from_user.id
    if user_id not in user_scores:
        user_scores[user_id] = 0

    update.message.reply_text(f"تحدي اليوم: \n" 
                              f"ما هو الفيلم الذي جاء منه هذا الاقتباس: \n\n"
                              f"*'{quote_today['quote']}'* \n\n"
                              f"إذا أجبت بشكل صحيح، ستحصل على نقاط!")

# دالة لمعالجة الإجابات
def check_answer(update, context):
    user_answer = update.message.text.lower()
    correct_answer = quote_today['movie'].lower()

    user_id = update.message.from_user.id
    if user_id not in user_scores:
        user_scores[user_id] = 0

    if user_answer == correct_answer:
        user_scores[user_id] += 10
        update.message.reply_text(f"إجابة صحيحة! نقاطك: {user_scores[user_id]}")
    else:
        hint = quote_today['hint']
        user_scores[user_id] = max(0, user_scores[user_id] - 2)  # خصم نقطتين على كل تلميح
        update.message.reply_text(f"إجابة خاطئة! تلميح: {hint} \nنقاطك: {user_scores[user_id]}")

# دالة لعرض أفضل اللاعبين في التحدي
def top_scorers(update, context):
    sorted_scores = sorted(user_scores.items(), key=lambda x: x[1], reverse=True)[:5]
    top_users = "\n".join([f"{update.message.bot.get_chat(user_id).username}: {score}" for user_id, score in sorted_scores])
    update.message.reply_text(f"أفضل 5 لاعبين في التحدي:\n{top_users}")

# الوظيفة الرئيسية للبوت
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("top", top_rated))
    dp.add_handler(CommandHandler("genre", search_by_genre))
    dp.add_handler(CommandHandler("rating", top_rated))
    dp.add_handler(CommandHandler("quote", quote_challenge))  # إضافة لتحدي الاقتباس
    dp.add_handler(CommandHandler("top_scores", top_scorers))  # إضافة لعرض أفضل اللاعبين
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
