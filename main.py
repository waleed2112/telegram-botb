from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ParseMode
import random
import requests
from google.cloud import vision
from google.cloud.vision import types
import io

# التوكن الخاص بالبوت
BOT_TOKEN = '7614704758:AAHXU2ZPBrYXIusXuwbFCKFrCCHtoT8n-Do'

# مفتاح OMDb API
OMDB_API_KEY = 'aa7d3da9'

# مفتاح Google Cloud Vision API
GOOGLE_CLOUD_VISION_API_KEY = 'AIzaSyDL_1GglThd7nEyQhGs3_3XR4wSNcZG8a8'

# حساب السناب
SNAPCHAT_USERNAME = "xwn_4"
SNAPCHAT_LINK = f"https://www.snapchat.com/add/{SNAPCHAT_USERNAME}"

# دالة لتحليل الصورة باستخدام Google Vision API
def analyze_image(image_path):
    client = vision.ImageAnnotatorClient.from_service_account_json('path_to_your_credentials_file.json')

    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        # العودة إلى أول نتيجة (أعلى نص مستخرج)
        return texts[0].description
    return None

# دالة للبحث عن الأفلام بناءً على صورة
def search_movie_from_image(update, context):
    if update.message.photo:
        # تحميل الصورة المرسلة من المستخدم
        photo = update.message.photo[-1].get_file()
        photo.download('user_image.jpg')

        # تحليل الصورة باستخدام Google Vision
        movie_name = analyze_image('user_image.jpg')

        if movie_name:
            # البحث عن الفيلم باستخدام OMDb API
            url = f"http://www.omdbapi.com/?t={movie_name}&apikey={OMDB_API_KEY}&plot=full&language=en"
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
                update.message.reply_text(f"لم أتمكن من العثور على هذا الفيلم. تأكد من صحة النص المستخرج: {movie_name}")
        else:
            update.message.reply_text("لم أتمكن من استخراج نص من الصورة. حاول إرسال صورة واضحة تحتوي على نص.")
    else:
        update.message.reply_text("يرجى إرسال صورة تحتوي على اسم الفيلم.")

# الوظيفة الرئيسية للبوت
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.photo, search_movie_from_image))  # إضافة هذه الدالة لمعالجة الصور

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
