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

# قاعدة بيانات النقاط
user_points = {}
user_hint = {}  # قاعدة بيانات التلميحات

# دالة للبحث عن الأفلام
def search_movie(update, context):
    title = ' '.join(context.args)
    user = update.message.from_user.username
    if not title:
        update.message.reply_text(f"مرحبًا {user}, يرجى إدخال اسم الفيلم أو المسلسل مثل: /m The Dark Knight\n\n"
                                  f"لمزيد من المعلومات يمكنك إضافة حسابي على السناب: {SNAPCHAT_LINK}")
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
        update.message.reply_text(f"لم أتمكن من العثور على هذا الفيلم أو المسلسل. تأكد من الكتابة الصحيحة، {user}.\n\n"
                                  f"لمزيد من المعلومات يمكنك إضافة حسابي على السناب: {SNAPCHAT_LINK}")

# دالة لعرض "فيلم اليوم" مع اقتباس عشوائي
def movie_of_the_day(update, context):
    movie = random.choice(movies_of_the_day)  # اختيار فيلم عشوائي من القائمة
    movie_title = movie["title"]
    movie_quote = movie["quote"]
    user = update.message.from_user.username
    update.message.reply_text(f"مرحبًا {user}, فيلم اليوم هو: *{movie_title}*\n\n"
                              f"اقتباس من الفيلم: \n\n*\"{movie_quote}\"*\n\n"
                              "هل يمكنك تخمين من قال هذا الاقتباس؟ اكتب إجابتك!\n\n"
                              f"لمزيد من المعلومات يمكنك إضافة حسابي على السناب: {SNAPCHAT_LINK}")
    
    # حفظ الفيلم والاقتباس في السياق لمقارنة الإجابة لاحقًا
    context.user_data['movie_of_the_day'] = movie

# دالة لتحقق من الإجابة
def check_answer(update, context):
    user = update.message.from_user.username
    movie = context.user_data.get('movie_of_the_day')
    if movie:
        correct_answer = movie["correct_answer"]
        user_answer = update.message.text.strip()

        if user_answer.lower() == correct_answer.lower():
            # إضافة نقاط للمستخدم عند الإجابة الصحيحة
            user_points[user] = user_points.get(user, 0) + 10
            update.message.reply_text(f"مبروك {user}! لقد أجبت بشكل صحيح! 🎉\n"
                                      "لقد ربحت 10 نقاط! 🏅\n"
                                      f"مجموع نقاطك الآن: {user_points[user]}")
        else:
            # تلميحات
            if user not in user_hint:
                user_hint[user] = {"attempts": 0, "hint": ""}
            
            user_hint[user]["attempts"] += 1
            hint = correct_answer[:user_hint[user]["attempts"]]
            user_hint[user]["hint"] = hint
            update.message.reply_text(f"للأسف، الإجابة خاطئة! التلميح التالي: {hint}\n"
                                      f"تلميحك الحالي: {user_hint[user]['hint']}")

    else:
        update.message.reply_text(f"لم يتم تقديم تحدي الاقتباس بعد. استخدم الأمر /f لتحدي اليوم.")

# دالة لعرض أعلى النقاط
def leaderboard(update, context):
    if not user_points:
        update.message.reply_text("لا توجد نقاط حالياً. ابدأ بتخمين الاقتباسات للحصول على نقاط!")
        return

    sorted_users = sorted(user_points.items(), key=lambda x: x[1], reverse=True)
    leaderboard_message = "*قائمة أعلى النقاط:*\n\n"
    for i, (user, points) in enumerate(sorted_users, 1):
        leaderboard_message += f"{i}. {user} - {points} نقاط\n"

    update.message.reply_text(leaderboard_message)

# دالة لعرض "مشاهدة اليوم"
def watch_today(update, context):
    movie = random.choice(movies_of_the_day)  # اختيار فيلم عشوائي من القائمة
    movie_title = movie["title"]
    user = update.message.from_user.username
    update.message.reply_text(f"مرحبًا {user}, فيلم اليوم هو: *{movie_title}*\n\n"
                              "شاهد الفيلم وشاركنا رأيك بعد المشاهدة! 🎬\n"
                              "اخبرني إذا كنت قد شاهدت الفيلم ماذا كان رأيك؟")

# دالة لبدء البوت
def start(update, context):
    user = update.message.from_user.username
    update.message.reply_text(f"مرحبًا {user}! أنا بوت الأفلام. استخدم الأوامر التالية:\n"
                              "/f - للحصول على فيلم اليوم مع اقتباس لتخمينه.\n"
                              "/w - للحصول على فيلم اليوم لبدء مشاهدته وتقييمه.\n"
                              "/m <اسم الفيلم أو المسلسل> - للبحث عن فيلم أو مسلسل.\n"
                              "/lb - لعرض قائمة أفضل الناس الذين جاوبوا.\n"
                              "/r - لاقتراح أفلام ومسلسلات جديدة.\n\n"
                              "إذا كنت بحاجة للمساعدة أو تريد التواصل معي:\n"
                              f"حسابي على التليجرام: @iLHwk\n"
                              f"حسابي على السناب: {SNAPCHAT_LINK}")

# الوظيفة الرئيسية للبوت
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("f", movie_of_the_day))
    dp.add_handler(CommandHandler("w", watch_today))
    dp.add_handler(CommandHandler("m", search_movie))
    dp.add_handler(CommandHandler("lb", leaderboard))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, check_answer))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
