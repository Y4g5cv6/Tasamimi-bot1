import logging
import requests
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import io

# إعدادات عامة
BOT_TOKEN = '7055961157:AAGry_2-s4LsGS5q1A-w0-3dwXHl1bSZOGE'
OWNER_ID = 6091303835  # آيديك
MAX_ATTEMPTS = 5
user_attempts = {}

logging.basicConfig(level=logging.INFO)

# توليد صورة ذكاء صناعي
async def generate_image(prompt):
    url = "https://api.dreamlike.art/api/v1/generate"  # مثال وهمي، سنضع رابط فعلي لاحقًا
    headers = {"Authorization": "Bearer YOUR_API_KEY"}
    data = {"prompt": prompt, "steps": 30}
    # placeholder response
    response = requests.get("https://picsum.photos/512")
    return response.content

# أمر البدء
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 أهلاً بك في بوت تصاميمي\nاستخدم /design متبوعًا بجملة لوصف البوستر.\nمثال:\n/design إعلان لعطر رجالي فخم")

# التحقق من المحاولات
def allowed_to_generate(user_id):
    if user_id == OWNER_ID:
        return True
    if user_id not in user_attempts:
        user_attempts[user_id] = 0
    if user_attempts[user_id] < MAX_ATTEMPTS:
        user_attempts[user_id] += 1
        return True
    return False

# أمر تصميم صورة
async def design(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not allowed_to_generate(user_id):
        await update.message.reply_text("🚫 لقد استهلكت محاولاتك المجانية.\nللتواصل: @rzhsyh")
        return

    prompt = ' '.join(context.args)
    if not prompt:
        await update.message.reply_text("✏️ أرسل وصف التصميم بعد الأمر /design")
        return

    await update.message.reply_text("⏳ جارٍ إنشاء الصورة، يرجى الانتظار...")
    try:
        image_bytes = await generate_image(prompt)
        image_file = InputFile(io.BytesIO(image_bytes), filename="design.jpg")
        await update.message.reply_photo(photo=image_file, caption="✨ إليك تصميمك بواسطة الذكاء الاصطناعي!")
    except Exception as e:
        await update.message.reply_text(f"❌ حدث خطأ أثناء إنشاء التصميم.")

# أمر الدعم
async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📞 للدعم والتواصل:\n@rzhsyh")

# إطلاق البوت
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("design", design))
    app.add_handler(CommandHandler("support", support))
    app.run_polling()

if __name__ == '__main__':
    main() 
