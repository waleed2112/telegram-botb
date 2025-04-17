from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ParseMode
import random
import requests

# التوكن الخاص بالبوت
BOT_TOKEN = '7614704758:AAHXU2ZPBrYXIusXuwbFCKFrCCHtoT8n-Do'

# مفتاح OMDb API
OMDB_API_KEY = 'aa7d3da9'

# حساب السناب
SNAPCHAT_USERNAME = "xwn_4"
SNAPCHAT_LINK = f"https://www.snapchat.com/add/{SNAPCHAT_USERNAME}"

# قائمة أفلام "فيلم اليوم" مع اقتباسات
movies_of_the_day = [
    {
        "title": "The Dark Knight",
        "quote": "Why so serious?",
        "correct_answer": "The Joker"
    },
    {
        "title": "Forrest Gump",
        "quote": "Life is like a box of chocolates.",
        "correct_answer": "Forrest Gump"
    },
    {
        "title": "The Godfather",
        "quote": "I'm gonna make him an offer he can't refuse.",
        "correct_answer": "Don Vito Corleone"
    },
    {
        "title": "Inception",
        "quote": "You mustn't be afraid to dream a little bigger, darling.",
        "correct_answer": "Eames"
    },
    {
        "title": "Star Wars: Episode V - The Empire Strikes Back",
        "quote": "No, I am your father.",
        "correct_answer": "Darth Vader"
    }
]

# دالة للبحث عن الأفلام
def search_movie(update, context):
    title = ' '.join(context.args)
    if not title:
        update.message.reply_text("يرجى إدخال اسم الفيلم أو المسلسل مثل: /m The Dark Knight")
        return

    url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}&plot=full&language=en"
    response = requests.get(url).json()

    if response["Response"] == "True":
        movie_info = f"""
        *العنوان:* {response['Title']}
        *السنة:* {response['Year']}
        *التقييم:* {response['imdbRating']}
        *النوع:* {response['Genre']}
        *القصة:* {response['Plot']}
        """
        poster_url = response.get("Poster", "")
        if poster_url and poster_url != "N/A":
            update.message.reply_photo(photo=poster_url, caption=movie_info, parse_mode=ParseMode.MARKDOWN)
        else:
            update.message.reply_text(movie_info, parse_mode=ParseMode.MARKDOWN)
    else:
        update.message.reply_text("لم أتمكن من العثور على هذا الفيلم أو المسلسل. تأكد من الكتابة الصحيحة.")

# دالة لعرض "فيلم اليوم" مع اقتباس عشوائي
def movie_of_the_day(update, context):
    movie = random.choice(movies_of_the_day)  # اختيار فيلم عشوائي من القائمة
    movie_title = movie["title"]
    movie_quote = movie["quote"]
    update.message.reply_text(f"فيلم اليوم هو: *{movie_title}*\n\n"
                              f"اقتباس من الفيلم: \n\n*\"{movie_quote}\"*\n\n"
                              "هل يمكنك تخمين من قال هذا الاقتباس؟ اكتب إجابتك!\n\n"
                              f"لمزيد من المعلومات يمكنك إضافة حسابي على السناب: {SNAPCHAT_LINK}")
    
    # حفظ الفيلم والاقتباس في السياق لمقارنة الإجابة لاحقًا
    context.user_data['movie_of_the_day'] = movie

# دالة لتحقق من الإجابة
def check_answer(update, context):
    movie = context.user_data.get('movie_of_the_day')
    if movie:
        correct_answer = movie["correct_answer"]
        user_answer = update.message.text.strip()

        if user_answer.lower() == correct_answer.lower():
            update.message.reply_text("مبروك! لقد أجبت بشكل صحيح! 🎉\n"
                                      "لقد ربحت 10 نقاط! 🏅")
            # هنا يمكن إضافة كود لحساب النقاط في قاعدة بيانات خاصة بك
        else:
            update.message.reply_text(f"للأسف، الإجابة خاطئة! الإجابة الصحيحة هي: {correct_answer}")
    else:
        update.message.reply_text("لم يتم تقديم تحدي الاقتباس بعد. استخدم الأمر /f لتحدي اليوم.")

# دالة لعرض "مشاهدة اليوم"
def watch_today(update, context):
    movie = random.choice(movies_of_the_day)  # اختيار فيلم عشوائي من القائمة
    movie_title = movie["title"]
    update.message.reply_text(f"فيلم اليوم هو: *{movie_title}*\n\n"
                              "شاهد الفيلم وشاركنا رأيك بعد المشاهدة! 🎬\n"
                              "اخبرني إذا كنت قد شاهدت الفيلم ماذا كان رأيك؟")

# دالة لبدء البوت
def start(update, context):
    update.message.reply_text("مرحبًا! أنا بوت الأفلام. استخدم الأوامر التالية:\n"
                              "/f - للحصول على فيلم اليوم مع اقتباس لتخمينه.\n"
                              "/w - للحصول على فيلم اليوم لبدء مشاهدته وتقييمه.\n"
                              "/m <اسم الفيلم أو المسلسل> - للبحث عن فيلم أو مسلسل.")

# الوظيفة الرئيسية للبوت
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("f", movie_of_the_day))
    dp.add_handler(CommandHandler("w", watch_today))
    dp.add_handler(CommandHandler("m", search_movie))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, check_answer))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
