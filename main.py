import os
import io
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ParseMode

# التوكن الخاص بالبوت
BOT_TOKEN = '7614704758:AAHXU2ZPBrYXIusXuwbFCKFrCCHtoT8n-Do'

# المفتاح API الخاص بـ Google Cloud
API_KEY = "AIzaSyDL_1GglThd7nEyQhGs3_3XR4wSNcZG8a8"

# دالة لتحليل الصورة باستخدام Google Cloud Vision API
def analyze_image(image_path):
    # فتح الصورة
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    # تكوين الطلب باستخدام API key
    url = "https://vision.googleapis.com/v1/images:annotate"
    headers = {'Content-Type': 'application/json'}
    
    # بناء البيانات للطلب
    data = {
        "requests": [
            {
                "image": {
                    "content": content.decode('ISO-8859-1')  # تحويل المحتوى إلى صيغة نصية
                },
                "features": [
                    {
                        "type": "TEXT_DETECTION"
                    }
                ]
            }
        ]
    }

    # إضافة المفتاح API إلى الرابط
    response = requests.post(url, headers=headers, json=data, params={'key': API_KEY})

    # معالجة الاستجابة
    if response.status_code == 200:
        result = response.json()
        texts = result['responses'][0].get('textAnnotations', [])
        
        if texts:
            # إرجاع النص المستخرج من الصورة
            return texts[0]['description']
    else:
        print("خطأ في الاتصال بـ Google Vision API:", response.status_code)
    return None

# دالة للبحث عن الفيلم باستخدام النص المستخرج من الصورة
def search_movie(update, context):
    user = update.message.from_user.username
    # تحميل الصورة من المستخدم
    photo = update.message.photo[-1].get_file()
    photo.download('user_image.jpg')

    # تحليل الصورة باستخدام Google Vision API
    movie_name = analyze_image('user_image.jpg')

    if movie_name:
        # إجراء البحث عن الفيلم باستخدام OMDb API
        url = f"http://www.omdbapi.com/?t={movie_name}&apikey=aa7d3da9&plot=full&language=en"
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
            update.message.reply_text(f"لم أتمكن من العثور على هذا الفيلم أو المسلسل: {movie_name}")
    else:
        update.message.reply_text("لم أتمكن من استخراج النص من الصورة.")

# دالة لبدء التفاعل مع البوت
def start(update, context):
    user = update.message.from_user.username
    update.message.reply_text(f"مرحبًا {user}! أرسل لي صورة تحتوي على نص من فيلم أو مسلسل وسأساعدك في تحديده.")

# الوظيفة الرئيسية للبوت
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.photo, search_movie))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
