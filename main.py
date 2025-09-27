from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8478445732:AAExzCN-vAwxZnnhGfhUjZ5EEZSjFtBYbxc"
WEBHOOK_URL = "https://telegram-bot-1d3c.onrender.com/webhook"

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ البوت يعمل! استخدم /add لإضافة مهمة.")

# أمر /add
async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if args:
        task = " ".join(args)
        await update.message.reply_text(f"📌 تم إضافة المهمة: {task}")
    else:
        await update.message.reply_text("❗ استخدم الأمر بهذا الشكل:\n/add المهمة التي تريد إضافتها")

# تشغيل البوت باستخدام Webhook
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add))
    app.run_webhook(
        listen="0.0.0.0",
        port=8080,
        url_path="webhook",
        webhook_url=WEBHOOK_URL
    )

if __name__ == "__main__":
    main()
